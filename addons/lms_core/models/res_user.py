from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import re

class LmsStudent(models.Model):
    _name = 'lms.student'
    _description = 'LMS Student'

    
    name = fields.Char(string="Name", required=True)
    email = fields.Char(string="Email", required=True)
    user_id = fields.Many2one('res.users', string="Related User", required=True)

    #
    _sql_constraints = [
        ('email_unique', 'unique(email)', 'This email is already registered!'),
    ]

   
    @api.constrains('email')
    def _check_email_format(self):
        for record in self:
            if record.email:
                # Regex for: something @ something . something
                email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
                if not re.match(email_regex, record.email):
                    raise ValidationError(_("Invalid email format: %s") % record.email)