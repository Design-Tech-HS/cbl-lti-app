from app.extensions import ma
from app.models import (
    OutcomeResult,
)

class CourseSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "enrollment_term_id")


class UserSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "sis_user_id", "login_id")


class GradeSchema(ma.Schema):
    class Meta:
        fields = (
            "id",
            "course_id",
            "grade",
            "record_id",
            "user",
            "threshold",
            "min_score",
        )

    user = ma.Nested(UserSchema)


class OutcomeSchema(ma.ModelSchema):
    class Meta:
        fields = ("title", "id", "display_name")


class AlignmentSchema(ma.ModelSchema):
    class Meta:
        fields = ("id", "name", "do_not_drop")


class GradeCriteriaSchema(ma.ModelSchema):
    class Meta:
        # model = GradeCriteria
        fields = ("grade_rank", "grade", "threshold", "min_score")


class OutcomeResultSchema(ma.ModelSchema):
    class Meta:
        model = OutcomeResult

    outcome = ma.Nested(OutcomeSchema)
    alignment = ma.Nested(AlignmentSchema)
