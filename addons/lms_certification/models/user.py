from odoo import models, fields


class ResUsers(models.Model):
    _inherit = 'res.users'

    certification_ids = fields.One2many(
        comodel_name='lms.certificate',
        inverse_name='user_id',
        string="Certificates"
    )