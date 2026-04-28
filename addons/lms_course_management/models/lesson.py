from odoo import api, fields, models


class Lesson(models.Model):
    _name = "lms.lesson"
    _description = "LMS Lesson"
    _order = "sequence, id"

    name = fields.Char(string="Lesson Name", required=True)

    module_id = fields.Many2one(
        comodel_name="lms.module",
        string="Module",
        required=True,
        ondelete="cascade"
    )

    sequence = fields.Integer(
        string="Sequence"
    )

    content_ids = fields.One2many(
        comodel_name="lms.content",
        inverse_name="lesson_id",
        string="Content"
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get("sequence") and vals.get("module_id"):
                last_lesson = self.search(
                    [("module_id", "=", vals["module_id"])],
                    order="sequence desc",
                    limit=1
                )
                vals["sequence"] = (last_lesson.sequence or 0) + 1

        return super().create(vals_list)

    def get_ordered_content(self):
        self.ensure_one()
        return self.content_ids.sorted(lambda content: (content.sequence, content.id))
