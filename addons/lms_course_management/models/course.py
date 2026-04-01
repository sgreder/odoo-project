from odoo import fields, models


class Course(models.Model):
    _name = "lms.course"
    _description = "LMS Course"
    _rec_name = "name"

    # -------------------------
    # Basic Fields
    # -------------------------
    name = fields.Char(string="Course Name", required=True)

    description = fields.Text(string="Description")

    # -------------------------
    # Relationships
    # -------------------------
    instructor_id = fields.Many2one(
        comodel_name="res.users",
        string="Instructor",
        ondelete="set null"
    )

    enrollment_ids = fields.One2many(
        comodel_name="lms.enrollment",
        inverse_name="course_id",
        string="Enrollments"
    )