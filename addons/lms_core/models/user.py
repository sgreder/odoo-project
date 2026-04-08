from odoo import api, fields, models
from odoo.exceptions import ValidationError
from odoo.osv import expression


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
    is_student = fields.Boolean(default=True)
    is_instructor = fields.Boolean()
    is_admin = fields.Boolean()

    # -------------------------
    # Computed Fields
    # -------------------------
    progress_summary = fields.Float(
        compute='_compute_progress_summary',
        store=True
    )

    rating = fields.Float(string='Rating', default=0.0)

    rating_count = fields.Integer(string='Rating Count', default=0)

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

    # -------------------------
    # Business Logic
    # -------------------------
    @api.model_create_multi
    def create(self, vals_list):
        """Default new users to student when role is not provided."""
        for vals in vals_list:
            vals.setdefault('is_student', True)
        return super().create(vals_list)

    @api.model
    def _role_field_mapping(self):
        return {
            'student': 'is_student',
            'instructor': 'is_instructor',
            'admin': 'is_admin',
        }

    @api.model
    def _normalize_role_name(self, role_name):
        normalized = (role_name or '').strip().lower()
        if normalized not in self._role_field_mapping():
            raise ValidationError(
                "Invalid role '%s'. Allowed roles: student, instructor, admin."
                % (role_name or '')
            )
        return normalized

    def assign_role(self, role_name):
        """Assign a role flag to each user record."""
        role = self._normalize_role_name(role_name)
        role_field = self._role_field_mapping()[role]
        self.write({role_field: True})
        return True

    @api.model
    def search_users(self, query):
        """Search users by name, email/login, and role."""
        query = (query or '').strip()
        if not query:
            return self.browse()

        domain = expression.OR([
            [('name', 'ilike', query)],
            [('login', 'ilike', query)],
        ])

        role_domains = []
        lowered = query.lower()
        for role, role_field in self._role_field_mapping().items():
            if role.startswith(lowered) or lowered in role:
                role_domains.append([(role_field, '=', True)])

        if role_domains:
            domain = expression.OR([domain] + role_domains)

        return self.search(domain)

    def get_profile_data(self):
        """Return core profile payload with basic info and roles only."""
        self.ensure_one()

        roles = [
            role
            for role, role_field in self._role_field_mapping().items()
            if self[role_field]
        ]

        return {
            'basic_info': {
                'id': self.id,
                'name': self.name,
                'email': self.login,
                'bio': self.bio,
                'experience_level': self.experience_level,
                'rating': self.rating,
            },
            'roles': roles,
        }

    def submit_or_update_rating(self, rating_value):
        """
        Create or update a rating from current user → this user
        """
        self.ensure_one()
        current_user = self.env.user

        """if current_user.id == self.id:
            raise ValidationError("You cannot rate yourself.")"""

        rating_model = self.env['lms.user.rating']

        existing = rating_model.search([
            ('rater_id', '=', current_user.id),
            ('rated_user_id', '=', self.id)
        ], limit=1)

        if existing:
            existing.rating = rating_value

        else:
            rating_model.create({
                'rater_id': current_user.id,
                'rated_user_id': self.id,
                'rating': rating_value,
            })

        # recompute average + count
        ratings = rating_model.search([('rated_user_id', '=', self.id)])
        total = sum(r.rating for r in ratings)
        count = len(ratings)

        self.write({
            'rating': total / count if count else 0,
            'rating_count': count,
        })

        return True