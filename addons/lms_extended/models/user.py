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
        comodel_name = 'lms.enrollment',
        inverse_name = 'user_id'
    )

    completed_course_ids = fields.Many2many(
        comodel_name = 'lms.course'
    )

    certification_ids = fields.One2many(
        comodel_name = 'lms.certificate',
        inverse_name = 'user_id'
    )

    progress_summary = fields.Float(
        compute="_compute_progress_summary"
    )

    course_id = fields.One2many(
        comodel_name = 'lms.course', 
        inverse_name = 'instructor_id',
        rating = fields.Float()
        )
    
    _sql_constraints = [
        ('unique_login', 'unique(login)', 'Email/login must be unique.'),
        ('unique_name', 'unique(name)', 'Username/name must be unique.'),
        (
            'check_at_least_one_role',
            'CHECK(is_student OR is_instructor OR is_admin)',
            'At least one role must be selected.'
        ),
    ]