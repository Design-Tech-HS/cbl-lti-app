# -*- coding: utf-8 -*-
"""The app module, containing the app factory function."""
import logging
import sys

# from redis import Redis
# import rq

from flask import Flask, render_template
from flask_migrate import upgrade
from sqlalchemy.exc import ProgrammingError

import app.settings as settings
from app import (
    commands,
    course,
    user,
    public,
    api,
)  # Need to import modules that contain blueprints
from app.extensions import db, ma, migrate


def create_app(config_object="app.settings.configClass"):
    """Create application factory, as explained here: http://flask.pocoo.org/docs/patterns/appfactories/.

    :param config_object: The configuration object to use.
    """
    config_object = settings.configClass
    app = Flask(__name__.split(".")[0])
    app.config.from_object(config_object)
    # app.redis = Redis.from_url(app.config['REDIS_URL'])
    # app.task_queue = rq.Queue('cbl-tasks', connection=app.redis)

    register_errorhandlers(app)
    register_shellcontext(app)
    register_commands(app)
    configure_logger(app)
    register_filters(app)
    register_blueprints(app)
    register_extensions(app)

    # Run db migrations if needed
    if app.config.get("RUN_MIGRATIONS", False):
        with app.app_context():
            run_migrations_if_needed()

    return app


def run_migrations_if_needed():
    """Run database migrations if not yet applied."""
    try:
        result = db.engine.execute("SELECT 1 FROM alembic_version")
    except ProgrammingError as e:
        # Run migrations if alembic_version table is missing
        upgrade()


def register_extensions(app):
    """Register Flask extensions."""

    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db, compare_server_default=True)
    from app.extensions import admin

    admin.init_app(app)

    # Import models
    return None


def register_blueprints(app):
    """Register Flask blueprints."""
    app.register_blueprint(user.views.blueprint)
    app.register_blueprint(course.views.blueprint)
    app.register_blueprint(public.views.blueprint)
    from app.account import blueprint as account_bp

    app.register_blueprint(account_bp)
    app.register_blueprint(api.views.blueprint)
    return None


def register_errorhandlers(app):
    """Register error handlers."""

    def render_error(error):
        """Render error template."""
        # If a HTTPException, pull the `code` attribute; default to 500
        error_code = getattr(error, "code", 500)
        return render_template(f"{error_code}.html"), error_code

    for errcode in [401, 404, 500]:
        app.errorhandler(errcode)(render_error)
    return None


def register_shellcontext(app):
    """Register shell context objects."""
    pass

    def shell_context():
        """Shell context objects."""
        # TODO - move import...
        from app.models import (
            Outcome,
            Course,
            Record,
            Grade,
            User,
            EnrollmentTerm,
            GradeCalculation,
            Alignment,
            OutcomeResult,
            CourseUserLink,
            Task,
        )
        from app.schemas import (
            OutcomeSchema,
            OutcomeResultSchema,
            AlignmentSchema,
            GradeSchema,
            UserSchema,
        )

        return dict(
            db=db,
            Outcome=Outcome,
            Course=Course,
            Record=Record,
            Grade=Grade,
            User=User,
            UserSchema=UserSchema,
            GradeSchema=GradeSchema,
            Alignment=Alignment,
            OutcomeResult=OutcomeResult,
            CourseUserLink=CourseUserLink,
            EnrollmentTerm=EnrollmentTerm,
            GradeCriteria=GradeCalculation,
            OutcomeSchema=OutcomeSchema,
            OutcomeResultSchema=OutcomeResultSchema,
            AlignmentSchema=AlignmentSchema,
            Task=Task,
        )

    app.shell_context_processor(shell_context)


def register_commands(app):
    """Register Click commands."""
    app.cli.add_command(commands.test)
    app.cli.add_command(commands.lint)


def configure_logger(app):
    """Configure loggers."""
    handler = logging.StreamHandler(sys.stdout)
    if not app.logger.handlers:
        app.logger.addHandler(handler)


def register_filters(app):
    @app.template_filter("strftime")
    def datetimeformat(value, format="%m-%d-%Y"):
        return value.strftime(format)
