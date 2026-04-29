from odoo import models, fields, api
from odoo.exceptions import ValidationError


class LmsLessonContent(models.Model):
    _name = 'lms.lesson.content'
    _description = 'LMS Lesson Content'
    _order = 'sequence, id'

    CONTENT_TYPE_SELECTION = [
        ('text', 'Text'),
        ('video', 'Video'),
        ('image', 'Image'),
        ('file', 'File'),
        ('link', 'External Link'),
    ]

    lesson_id = fields.Many2one(
        'lms.lesson',
        string='Lesson',
        required=True,
        ondelete='cascade',
    )
    sequence = fields.Integer(string='Sequence', default=1)
    content_type = fields.Selection(
        selection=CONTENT_TYPE_SELECTION,
        string='Content Type',
        required=True,
        default='text',
    )

    # Text payload
    text_content = fields.Text(string='Text Content')

    # File payload (used for image, file, generic uploads)
    file = fields.Binary(string='File', attachment=True)
    file_name = fields.Char(string='File Name')

    # Video payload (separate so users can choose upload OR url)
    video_file = fields.Binary(string='Video File', attachment=True)
    video_filename = fields.Char(string='Video Filename')

    # External link / URL (used for image, video, file, link)
    url = fields.Char(string='URL')

    # ------------------------------------------------------------------
    # Validation: each content_type must have its required payload field
    # ------------------------------------------------------------------
    @api.constrains('content_type', 'text_content', 'file', 'video_file', 'url')
    def _check_content_payload(self):
        for rec in self:
            ct = rec.content_type
            if ct == 'text' and not rec.text_content:
                raise ValidationError("Text content type requires text_content.")
            if ct == 'image' and not (rec.file or rec.url):
                raise ValidationError("Image content type requires either an uploaded file or a URL.")
            if ct == 'video' and not (rec.video_file or rec.url):
                raise ValidationError("Video content type requires either an uploaded video file or a URL.")
            if ct == 'file' and not rec.file:
                raise ValidationError("File content type requires an uploaded file.")
            if ct == 'link' and not rec.url:
                raise ValidationError("External Link content type requires a URL.")
