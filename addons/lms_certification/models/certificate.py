from odoo import fields, models


class Certificate(models.Model):
    _name = "lms.certificate"
    _description = "LMS Certificate"
    _rec_name = "certificate_name"

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

    date_issued = fields.Date(
        string="Date Issued",
        default=fields.Date.today
    )

    certificate_name = fields.Char(
        string="Certificate Name",
        required=True
    )

    _sql_constraints = [
        ('unique_certificate', 'unique(user_id, course_id)', 'Certificate already exists for this course.')
    ]