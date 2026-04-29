from odoo import models, fields, api


class LmsCourseModule(models.Model):
    _inherit = 'lms.course.module'

    lesson_ids = fields.One2many(
        comodel_name='lms.lesson',
        inverse_name='module_id',
        string='Lessons',
    )
    lesson_count = fields.Integer(
        string='Lessons',
        compute='_compute_lesson_count',
    )

    def _compute_lesson_count(self):
        for rec in self:
            rec.lesson_count = len(rec.lesson_ids)
