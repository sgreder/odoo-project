from odoo import fields, models


class Enrollment(models.Model):
    _name = "lms.enrollment"
    _description = "LMS Enrollment"

    # -------------------------
    # Relationships
    # -------------------------
    user_id = fields.Many2one(
        comodel_name="res.users",
        string="Student",
        required=True,
        ondelete="cascade"
    )

    course_id = fields.Many2one(
        comodel_name="lms.course",
        string="Course",
        required=True,
        ondelete="cascade"
    )

    # -------------------------
    # Additional Fields
    # -------------------------
    date_enrolled = fields.Date(
        string="Enrollment Date",
        default=fields.Date.today
    )

    status = fields.Selection(
        [
            ('in_progress', 'In Progress'),
            ('completed', 'Completed'),
            ('dropped', 'Dropped'),
        ],
        string="Status",
        default='in_progress'
    )

    _sql_constraints = [
        ('unique_enrollment', 'unique(user_id, course_id)', 'User is already enrolled in this course.')
    ]