from odoo import models, fields, api


class ResUsers(models.Model):
    _inherit = 'res.users'

    # -------------------------
    # Basic Profile Fields
    # -------------------------
    experience_level = fields.Selection([
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced')
    ])

    bio = fields.Text()

    # -------------------------
    # Role Flags
    # -------------------------
    is_student = fields.Boolean()
    is_instructor = fields.Boolean()
    is_admin = fields.Boolean()

    # -------------------------
    # Computed Fields
    # -------------------------
    progress_summary = fields.Float(
        compute='_compute_progress_summary',
        store=True
    )

    rating = fields.Float()

    # -------------------------
    # Constraints
    # -------------------------
    _sql_constraints = [
        ('unique_login', 'unique(login)', 'Email/login must be unique.'),
        ('unique_name', 'unique(name)', 'Username/name must be unique.'),
        (
            'check_at_least_one_role',
            'CHECK(is_student OR is_instructor OR is_admin)',
            'At least one role must be selected.'
        ),
    ]

    # -------------------------
    # Compute Methods
    # -------------------------
    def _compute_progress_summary(self):
        for user in self:
            user.progress_summary = 0.0