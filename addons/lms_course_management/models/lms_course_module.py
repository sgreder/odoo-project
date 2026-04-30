from odoo import models, fields


class LmsCourseModule(models.Model):
    _name = 'lms.course.module'
    _description = 'LMS Course Module'
    _order = 'sequence, id'

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')
    sequence = fields.Integer(string='Sequence', default=1)
    course_id = fields.Many2one(
        comodel_name='lms.course',
        string='Course',
        required=True,
        ondelete='cascade',
        index=True,
    )
