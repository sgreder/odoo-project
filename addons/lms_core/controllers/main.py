import re

from odoo import http
from odoo.exceptions import ValidationError
from odoo.http import request
from psycopg2 import IntegrityError


EMAIL_RE = re.compile(r'^[^@\s]+@[^@\s]+\.[^@\s]+$')


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
    """@http.route('/lms/signup/submit', type='http', auth='public', website=True, methods=['POST'])
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
        })"""
    
    # ----------------------
    # SIGNUP SUBMIT (REAL SIGNUP)
    # ----------------------
    @http.route('/lms/signup/submit', type='http', auth='public', website=True, methods=['POST'])
    def signup_submit(self, **post):

        name = (post.get('username') or '').strip()
        email = (post.get('email') or '').strip().lower()
        password = post.get('password') or ''

        def _error(msg):
            return request.render('lms_core.signup_template', {
                'error': msg,
                'email': email,
                'username': name,
            })

        # ----------------------
        # REQUIRED FIELDS
        # ----------------------
        if not name or not email or not password:
            return _error('Name, email and password are required.')

        # ----------------------
        # EMAIL FORMAT
        # ----------------------
        if not EMAIL_RE.match(email):
            return _error('Please enter a valid email address.')

        # ----------------------
        # PASSWORD STRENGTH
        # ----------------------
        if len(password) < 8 or not re.search(r'[A-Za-z]', password) or not re.search(r'\d', password):
            return _error('Password must be at least 8 characters and contain a letter and a number.')

        Users = request.env['res.users'].sudo()

        # ----------------------
        # UNIQUENESS (email + name)
        # ----------------------
        if Users.search_count([('login', '=', email)]):
            return _error('An account with this email already exists.')

        if Users.search_count([('name', '=', name)]):
            return _error('That username is already taken.')

        # ----------------------
        # CREATE USER
        # ----------------------
        try:
            Users.create({
                'name': name,
                'login': email,
                'password': password,
                'is_student': True,
                'groups_id': [(6, 0, [
                    request.env.ref('base.group_user').id
                ])],
            })
        except IntegrityError:
            request.env.cr.rollback()
            return _error('An account with this email or username already exists.')
        except ValidationError as e:
            request.env.cr.rollback()
            return _error(e.args[0] if e.args else 'Failed to create account.')
        except Exception:
            request.env.cr.rollback()
            return _error('Failed to create account.')

        # ----------------------
        # LOG USER IN
        # ----------------------
        uid = request.session.authenticate(request.db, email, password)

        if uid:
            return request.redirect('/lms/dashboard')

        # fallback (rare)
        return request.redirect('/lms/login')

    # ----------------------
    # PROFILE PAGE (HTML)
    # ----------------------
    @http.route('/lms/profile', type='http', auth='user', website=True)
    def lms_profile(self, **kwargs):
        profile = request.env.user.get_profile_data()
        return request.render('lms_core.profile_template', {
            'profile': profile,
        })

    # ----------------------
    # PROFILE ENDPOINT (JSON)
    # ----------------------
    @http.route('/api/profile', type='json', auth='user')
    def api_profile(self, **kwargs):
        return request.env.user.get_profile_data()


    # ----------------------
    # DASHBOARD
    # ----------------------
    @http.route('/lms/dashboard', type='http', auth='public', website=True)
    def lms_dashboard(self, **kwargs):
        user = request.env.user

        if not user or user._is_public():
            return request.redirect('/lms/login')

        return request.render('lms_core.lms_dashboard')

    # ----------------------
    # SEARCH USER
    # ----------------------
    @http.route('/lms/search', type='http', auth='user', website=True)
    def lms_search(self, query=None, **kwargs):
        users = request.env['res.users'].sudo().search_users(query)

        return request.render('lms_core.search_results', {
            'query': query,
            'users': users,
        })