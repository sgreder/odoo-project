from odoo import fields, models

class LMScourse(models.Model):
    _name = "lms.course"

    instructor_id = fields.Many2one("res.users")