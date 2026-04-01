from odoo import models, fields


class ResUsers(models.Model):
    _inherit = 'res.users'

    # -------------------------
    # Relationships to courses
    # -------------------------
    enrollment_ids = fields.One2many(
        comodel_name='lms.enrollment',
        inverse_name='user_id',
        string="Enrollments"
    )

    completed_course_ids = fields.Many2many(
        comodel_name='lms.course',
        relation='lms_user_completed_course_rel',
        column1='user_id',
        column2='course_id',
        string="Completed Courses"
    )

    # -------------------------
    # Instructor --> courses they created
    # -------------------------
    course_ids = fields.One2many(
        comodel_name='lms.course',
        inverse_name='instructor_id',
        string="Courses Taught"
    )