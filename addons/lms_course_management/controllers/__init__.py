
from odoo import http
from odoo.http import request

class CourseCatalogController(http.Controller):

    @http.route('/lms/courses', type='http', auth='public', website=True)
    def course_catalog(self):
        return request.render(
            'lms_course_management.course_catalog_page'
        )
