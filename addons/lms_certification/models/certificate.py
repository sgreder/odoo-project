from odoo import models, fields

class LMSCertificate(models.Model):
    _name = 'lms.certificate'

    user_id = fields.Many2one('res.users', string = 'User', required = True)
    name = fields.Char()
    issue_date = fields.Date()