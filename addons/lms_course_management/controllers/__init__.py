
from odoo import http
from odoo.http import request


class CourseCatalogController(http.Controller):

    @http.route('/lms/courses', type='http', auth='public', website=True)
    def course_catalog(self):
        return request.render(
            'lms_course_management.course_catalog_page'
        )


class CourseSearchController(http.Controller):

    @http.route('/lms/courses/search', type='json', auth='user', methods=['POST'])
    def search_courses(self, query='', category=None, limit=20, **kwargs):
        domain = []

        if query:
            domain += ['|', '|',
                ('name', 'ilike', query),
                ('description', 'ilike', query),
                ('category', 'ilike', query),
            ]

        if category:
            domain += [('category', '=', category)]

        courses = request.env['lms.course'].search(domain, limit=limit)

        return {
            'count': len(courses),
            'courses': courses.read([
                'id',
                'name',
                'description',
                'category'
            ]),
        }
