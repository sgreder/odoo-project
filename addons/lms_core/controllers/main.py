from odoo import http
from odoo.http import request


class LMSController(http.Controller):

    # ----------------------
    # LOGIN PAGE
    # ----------------------
    @http.route('/lms/login', type='http', auth='public', website=True)
    def login_page(self, **kwargs):
        return request.render('lms_core.login_template')


    # ----------------------
    # LOGIN SUBMIT
    # ----------------------
    @http.route('/lms/login/submit', type='http', auth='public', website=True, methods=['POST'])
    def login_submit(self, **post):
        login = post.get('login')
        password = post.get('password')

        try:
            uid = request.session.authenticate(request.db, login, password)

            if uid:
                return request.redirect('/lms/dashboard')

        except Exception:
            pass

        return request.render('lms_core.login_template', {
            'error': 'Invalid email or password',
            'login': login,
        })


    # ----------------------
    # SIGNUP PAGE
    # ----------------------
    @http.route('/lms/signup', type='http', auth='public', website=True)
    def signup_page(self, **kwargs):
        return request.render('lms_core.signup_template')


    # ----------------------
    # SIGNUP SUBMIT (FAKE SIGNUP)
    # ----------------------
    @http.route('/lms/signup/submit', type='http', auth='public', website=True, methods=['POST'])
    def signup_submit(self, **post):
        email = post.get('email')

        # Search for existing user
        user = request.env['res.users'].sudo().search([
            ('login', '=', email)
        ], limit=1)

        if user:
            # Manually log user in (NO PASSWORD CHECK)
            request.session.uid = user.id
            return request.redirect('/lms/dashboard')

        # If email not found, then show error
        return request.render('lms_core.signup_template', {
            'error': 'Email not found in system',
            'email': email,
        })


    # ----------------------
    # DASHBOARD
    # ----------------------
    '''
    @http.route('/lms/dashboard', type='http', auth='public', website=True)
    def lms_dashboard(self, **kwargs):
        user = request.env.user

        if not user or user._is_public():
            return request.redirect('/lms/login')

        return request.render('lms_core.lms_dashboard')
    '''

    @http.route('/lms/dashboard', type='http', auth='user', website=True)
    def lms_dashboard(self, **kwargs):
        user = request.env.user
        
        if not user or user._is_public():
            return request.redirect('/lms/login')

        
        is_admin = user.has_group('base.group_system')
        
        
        role = 'student'
        if is_admin:
            role = 'admin'
        elif is_instructor:
            role = 'instructor'

        return request.render('lms_core.lms_dashboard', {
            'user': user,
            'role': role,
        })

    @http.route('/api/search_users', type='json', auth='public', methods=['POST'], csrf=False)
    def api_search_users(self, **kwargs):
        
        data = request.get_json_data() or {}
        search_query = data.get('query', '')

        if not search_query:
            return {'status': 'error', 'message': 'No query provided'}

        
        users = request.env['res.users'].sudo().search([
            '|', 
            ('name', 'ilike', search_query), 
            ('login', 'ilike', search_query)
        ], limit=10) 

        results = []
        for user in users:
            results.append({
                'id': user.id,
                'name': user.name,
                'login': user.login,
            })

        return {
            'status': 'success',
            'data': results
        }

    @http.route('/api/user', type='json', auth='user', methods=['POST'], csrf=False)
    def get_current_user(self, **kwargs):

        user = request.env.user

        return {
            "status": "success",
            "data": {
                "id": user.id,
                "name": user.name,
                "email": user.login,
                "company": user.company_id.name,
                "lang": user.lang,
                "tz": user.tz or "Not Set",
                "image_url": f"/web/image/res.users/{user.id}/avatar_128"
            }
        }