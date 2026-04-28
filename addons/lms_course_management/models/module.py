from odoo import api, fields, models


class Module(models.Model):
    _name = "lms.module"
    _description = "LMS Module"
    _order = "sequence, id"

    name = fields.Char(string="Module Name", required=True)

    course_id = fields.Many2one(
        comodel_name="lms.course",
        string="Course",
        required=True,
        ondelete="cascade"
    )

    sequence = fields.Integer(string="Sequence")

    lesson_ids = fields.One2many(
        comodel_name="lms.lesson",
        inverse_name="module_id",
        string="Lessons"
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get("sequence") and vals.get("course_id"):
                last_module = self.search(
                    [("course_id", "=", vals["course_id"])],
                    order="sequence desc",
                    limit=1
                )
                vals["sequence"] = (last_module.sequence or 0) + 1

        return super().create(vals_list)
