from odoo import models, fields

class LMSEnrollment(models.Model):
    _name = "lms.enrollment"

    user_id = fields.Many2one("res.users", string = 'User', required = True)

