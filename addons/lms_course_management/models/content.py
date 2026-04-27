from odoo import api, fields, models
from odoo.exceptions import ValidationError


class Content(models.Model):
    _name = "lms.content"
    _description = "LMS Content"
    _order = "sequence, id"

    name = fields.Char(string="Content Name", required=True)

    lesson_id = fields.Many2one(
        comodel_name="lms.lesson",
        string="Lesson",
        required=True,
        ondelete="cascade"
    )

    sequence = fields.Integer(string="Sequence")

    content_type = fields.Selection(
        selection=[
            ("text", "Text"),
            ("video", "Video"),
            ("image", "Image"),
            ("file", "File"),
            ("link", "Link"),
        ],
        string="Content Type",
        required=True
    )

    text_content = fields.Text(string="Text Content")

    video_file = fields.Binary(string="Video File")

    file = fields.Binary(string="File")

    url = fields.Char(string="URL")

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get("sequence") and vals.get("lesson_id"):
                last_content = self.search(
                    [("lesson_id", "=", vals["lesson_id"])],
                    order="sequence desc",
                    limit=1
                )
                vals["sequence"] = (last_content.sequence or 0) + 1

        return super().create(vals_list)

    @api.constrains(
        "content_type",
        "text_content",
        "video_file",
        "file",
        "url"
    )
    def _validate_content(self):
        for content in self:
            if not content.content_type:
                raise ValidationError("Content type is required.")

            if content.content_type == "text":
                if not content.text_content:
                    raise ValidationError("Text content is required for text type.")

            elif content.content_type == "video":
                if not content.video_file and not content.url:
                    raise ValidationError("Video content requires a video file or URL.")

            elif content.content_type == "image":
                if not content.file and not content.url:
                    raise ValidationError("Image content requires a file or URL.")

            elif content.content_type == "file":
                if not content.file and not content.url:
                    raise ValidationError("File content requires a file or URL.")

            elif content.content_type == "link":
                if not content.url:
                    raise ValidationError("Link content requires a URL.")

    def get_render_type(self):
        self.ensure_one()

        render_map = {
            "text": "text",
            "video": "video",
            "image": "image",
            "file": "file",
            "link": "link",
        }

        return render_map.get(self.content_type)