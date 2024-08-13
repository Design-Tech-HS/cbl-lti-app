import datetime as dt
import json
import jwt
import os
import requests
import time

from canvasapi import Canvas
from flask import (
    Blueprint,
    render_template,
    current_app,
    session,
    url_for,
    request,
    redirect,
    jsonify,
)
from pylti.flask import lti
from sqlalchemy import desc, func, and_

from app.queries import get_enrollment_term
import app.settings as settings
from app.extensions import db
from app.models import (
    Outcome,
    Course,
    Record,
    Grade,
    User,
    OutcomeResult,
    CourseUserLink,
    OutcomeResultSchema,
    OutcomeSchema,
    EnrollmentTerm,
    AssignmentGradeCalculationConfig,
)
from app.queries import get_calculation_dictionaries

from utilities.canvas_api import get_course_users

# from utilities.cbl_calculator import calculation_dictionaries
from utilities.helpers import make_outcome_avg_dicts, format_users, error

# api secret
SECRET_API = os.getenv("SECRET_API")

blueprint = Blueprint("api", __name__, url_prefix="/api/v1")


@blueprint.route("/dragon_time", methods=["GET"])
def dragon_time():
    token = None
    if "x-access-tokens" in request.headers:
        token = request.headers["x-access-tokens"]

    if not token:
        return jsonify({"message": "a valid token is missing"})
    try:
        data = jwt.decode(token, SECRET_API, algorithms="HS256")
    except Exception as e:
        return jsonify({"message": "token is invalid"})

    if data["id"] != os.getenv("DRAGON_TIME_ID"):
        return jsonify({"message": "Invalid id!"})

    enrollment_term = get_enrollment_term()
    stmt = db.text(
        """
        SELECT
            u.sis_user_id
            , g.grade
            , c.sis_course_id
        FROM grades g
            JOIN courses c on c.id = g.course_id
            JOIN users u on u.id = g.user_id
        WHERE c.enrollment_term_id = :enrollment_term_id
        ORDER BY g.id
        """
    ).bindparams(enrollment_term_id=enrollment_term.id)

    results = db.session.execute(stmt)

    return jsonify([dict(row) for row in results])


@blueprint.route("assignments-setup", methods=["GET"])
@lti(error=error, role="instructor", request="session", app=current_app)
def get_assignments_setup(course_id=None, lti=lti):
    if not course_id:
        course_id = session["course_id"]

    subq = (
        db.session.query(
            AssignmentGradeCalculationConfig.canvas_assignment_id,
            func.max(AssignmentGradeCalculationConfig.updated_at).label(
                "max_updated_at"
            ),
        )
        .group_by(AssignmentGradeCalculationConfig.canvas_assignment_id)
        .subquery("t2")
    )

    query = db.session.query(
        AssignmentGradeCalculationConfig.canvas_assignment_id,
        AssignmentGradeCalculationConfig.do_not_drop,
    ).join(
        subq,
        and_(
            AssignmentGradeCalculationConfig.canvas_assignment_id
            == subq.c.canvas_assignment_id,
            AssignmentGradeCalculationConfig.updated_at == subq.c.max_updated_at,
        ),
    )
    
    # Create a dictionary from the query results
    do_not_drop_dict = {assignment.canvas_assignment_id: assignment.do_not_drop for assignment in query}

    canvas = Canvas(
        current_app.config["CANVAS_API_URL"], current_app.config["CANVAS_API_KEY"]
    )
    course = canvas.get_course(course_id)

    assignments = course.get_assignments()

    assignments_list = []
    for assignment in assignments:
        assignments_list.append(
            {
                "id": assignment.id,  # TODO: Maybe call this canvas_assignment_id to conform
                "name": assignment.name,
                "published": assignment.published,
                "due_at": assignment.due_at,
                "do_not_drop": do_not_drop_dict.get(assignment.id, False),
            }
        )

    return json.dumps(assignments_list)


@blueprint.route("assignments-setup", methods=["POST"])
@lti(error=error, role="instructor", request="session", app=current_app)
def post_assignments_setup(course_id=None, lti=lti):
    if not course_id:
        course_id = session["course_id"]

    data = request.json

    # get the user from the canvas api using the users lti 1.1 id from the lti object
    resp = requests.get(
        f"{current_app.config['CANVAS_API_URL']}/api/v1/users/lti_1_1_id:{lti.user_id}",
        headers={"Authorization": f"Bearer {current_app.config['CANVAS_API_KEY']}"},
    )

    if resp.ok:
        canvas_user = resp.json()
    else:
        print("Error")
        # TODO: Add error handling

    for assignment in data:
        assignment_grade_calculation_config = AssignmentGradeCalculationConfig(
            canvas_assignment_id=assignment["assignment_id"],
            do_not_drop=assignment["do_not_drop"],
            canvas_user_id=canvas_user["id"],
            updated_at=dt.datetime.now(dt.timezone.utc),
        )

        db.session.add(assignment_grade_calculation_config)

    db.session.commit()

    return "", 201
