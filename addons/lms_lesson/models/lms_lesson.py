from odoo import models, fields


class LmsLesson(models.Model):
    _name = 'lms.lesson'
    _description = 'LMS Lesson'
    _order = 'sequence, id'

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')
    module_id = fields.Many2one(
        'lms.course.module',
        string='Module',
        required=True,
        ondelete='cascade',
    )
    sequence = fields.Integer(string='Sequence', default=1)
    content_ids = fields.One2many(
        'lms.lesson.content',
        'lesson_id',
        string='Contents',
    )
