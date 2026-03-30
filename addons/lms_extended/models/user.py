from odoo import models, fields, api


class ResUsers(models.Model):
    _inherit = 'res.users'

    experience_level = fields.Selection([
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced')
    ])

    bio = fields.Text()

    is_student = fields.Boolean()
    is_instructor = fields.Boolean()
    is_admin = fields.Boolean()

    enrollment_ids = fields.One2many(
        'lms.enrollment',
        'user_id'
    )

    completed_course_ids = fields.Many2many(
        'lms.course'
    )

    certification_ids = fields.One2many(
        'lms.certificate',
        'user_id'
    )

    progress_summary = fields.Float(
        compute="_compute_progress_summary"
    )

    course_id = fields.One2many('lms.course', 'instructor_id')
    rating = fields.Float()
    
    @api.depends('enrollment_ids.progress')
    def _compute_progress_summary(self):
        for user in self:
            enrollments = user.enrollment_ids
            if enrollments:
                user.progress_summary = sum(enrollments.mapped('progress')) / len(enrollments)
            else:
                user.progress_summary = 0.0