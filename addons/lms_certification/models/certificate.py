<<<<<<< HEAD
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
=======
from odoo import models, fields

class LMSCertificate(models.Model):
    _name = 'lms.certificate'

    user_id = fields.Many2one('res.users', string = 'User', required = True)
    name = fields.Char()
    issue_date = fields.Date()
>>>>>>> fe256f429be59e22996a259e5f38d99235eb777f
