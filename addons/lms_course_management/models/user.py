from odoo import fields, models


class ResUsers(models.Model):
    _inherit = 'res.users'

    # -------------------------
    # Student Relationships
    # -------------------------
    student_course_ids = fields.Many2many(
        'lms.course',
        'lms_course_student_rel',
        'user_id',
        'course_id',
        string='Courses as Student'
    )

    enrollment_ids = fields.One2many(
        comodel_name='lms.enrollment',
        inverse_name='user_id',
        string='Enrollments'
    )

    completed_course_ids = fields.Many2many(
        comodel_name='lms.course',
        relation='lms_user_completed_course_rel',
        column1='user_id',
        column2='course_id',
        string='Completed Courses'
    )

    # -------------------------
    # Instructor Relationships
    # -------------------------
    instructor_course_ids = fields.Many2many(
        comodel_name='lms.course',
        compute='_compute_instructor_course_ids',
        string='Courses as Instructor',
        store=False
    )

    # Optional alias if you still want user.course_ids in old code
    course_ids = fields.Many2many(
        comodel_name='lms.course',
        compute='_compute_instructor_course_ids',
        string='Courses Taught',
        store=False
    )

    def _compute_instructor_course_ids(self):
        for user in self:
            courses = self.env['lms.course'].search([
                ('instructor_id', '=', user.id)
            ])
            user.instructor_course_ids = courses
            user.course_ids = courses

    def get_profile_data(self):
        """Extend core profile data with course/enrollment details."""
        data = super().get_profile_data()
        self.ensure_one()

        data['student_data'] = {
            'courses': self.student_course_ids.mapped('name'),
            'enrollments_count': len(self.enrollment_ids),
            'completed_courses_count': len(self.completed_course_ids),
        }

        data['instructor_data'] = {
            'courses_taught': self.instructor_course_ids.mapped('name'),
            'courses_taught_count': len(self.instructor_course_ids),
        }

        return data
