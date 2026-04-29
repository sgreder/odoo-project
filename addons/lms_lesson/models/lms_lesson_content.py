from odoo import models, fields


class LmsLessonContent(models.Model):
    _name = 'lms.lesson.content'
    _description = 'LMS Lesson Content'
    _order = 'sequence, id'

    CONTENT_TYPE_SELECTION = [
        ('text', 'Text'),
        ('video', 'Video'),
        ('image', 'Image'),
        ('file', 'File'),
        ('link', 'Link'),
    ]

    lesson_id = fields.Many2one(
        'lms.lesson',
        string='Lesson',
        required=True,
        ondelete='cascade',
    )
    sequence = fields.Integer(string='Sequence', default=1)
    type = fields.Selection(
        selection=CONTENT_TYPE_SELECTION,
        string='Content Type',
        required=True,
        default='text',
    )
    text_content = fields.Html(string='Text Content')
    file = fields.Binary(string='File', attachment=True)
    file_name = fields.Char(string='File Name')
    url = fields.Char(string='URL')
