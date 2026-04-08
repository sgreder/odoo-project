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

        name = post.get('username')
        email = post.get('email')
        password = post.get('password')

        # ----------------------
        # VALIDATION
        # ----------------------
        if not email or not password:
            return request.render('lms_core.signup_template', {
                'error': 'Email and password are required',
                'email': email,
            })

        # ----------------------
        # CHECK IF USER EXISTS
        # ----------------------
        existing_user = request.env['res.users'].sudo().search([
            ('login', '=', email)
        ], limit=1)

        if existing_user:
            return request.render('lms_core.signup_template', {
                'error': 'An account with this email already exists',
                'email': email,
            })

        # ----------------------
        # CREATE USER
        # ----------------------
        try:
            user = request.env['res.users'].sudo().create({
                'name': name or email,
                'login': email,
                'is_student': True,
                'groups_id': [(6, 0, [
                    request.env.ref('base.group_user').id
                ])],
            })

            user._set_password(password)

            request.env.cr.commit()
            
        except Exception:
            return request.render('lms_core.signup_template', {
                'error': 'Failed to create account',
                'email': email,
            })

        # ----------------------
        # LOG USER IN
        # ----------------------
        uid = request.session.authenticate(request.db, email, password)

        if uid:
            return request.redirect('/lms/dashboard')

        # fallback (rare)
        return request.redirect('/lms/login')


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

    # ----------------------
    # USER PROFILE PAGE
    # ----------------------
    @http.route('/lms/user/<int:user_id>', type='http', auth='user', website=True)
    def user_profile(self, user_id, **kwargs):
        user = request.env['res.users'].sudo().browse(user_id)

        if not user.exists():
            return request.redirect('/lms/dashboard')

        return request.render('lms_core.user_profile', {
            'profile_user': user,
        })
    
    # ----------------------
    # USER RATING PAGE
    # ----------------------
    @http.route('/lms/user/rate', type='http', auth='user', website=True, methods=['POST'])
    def rate_user(self, **post):
        try:
            user_id = int(post.get('user_id'))
            rating = int(post.get('rating'))
        except (TypeError, ValueError):
            return request.redirect('/lms/dashboard')

        user = request.env['res.users'].sudo().browse(user_id)

        # Check if user exists
        if not user.exists():
            return request.redirect('/lms/dashboard')

        # Submit or update rating
        user.submit_or_update_rating(rating)

        # Redirect back to profile
        return request.redirect(f'/lms/user/{user_id}')

    @http.route('/lms/user/<int:user_id>/rate', type='http', auth='user', website=True)
    def rate_page(self, user_id, **kwargs):
        user = request.env['res.users'].sudo().browse(user_id)

        return request.render('lms_core.user_rate_page', {
            'profile_user': user
        })
    
    # ----------------------
    # EDIT USER PROFILE PAGE
    # ----------------------
    @http.route('/lms/user/<int:user_id>/edit', type='http', auth='user', website=True, methods=['GET'])
    def edit_user_profile_page(self, user_id, **kwargs):
        user = request.env['res.users'].sudo().browse(user_id)

        if not user.exists():
            return request.redirect('/lms/dashboard')

        if request.env.user.id != user.id:
            return request.redirect(f'/lms/user/{user_id}')

        return request.render('lms_core.edit_user_profile', {
            'profile_user': user,
        })
    
    @http.route('/lms/user/<int:user_id>/edit', type='http', auth='user', website=True, methods=['POST'])
    def edit_user_profile_submit(self, user_id, **post):
        user = request.env['res.users'].sudo().browse(user_id)

        if not user.exists():
            return request.redirect('/lms/dashboard')

        if request.env.user.id != user.id:
            return request.redirect(f'/lms/user/{user_id}')

        login = (post.get('login') or '').strip()

        if not login:
            return request.render('lms_core.edit_user_profile', {
                'profile_user': user,
                'error': 'Email is required.',
            })

        existing_user = request.env['res.users'].sudo().search([
            ('login', '=', login),
            ('id', '!=', user.id),
        ], limit=1)

        if existing_user:
            return request.render('lms_core.edit_user_profile', {
                'profile_user': user,
                'error': 'That email is already being used by another account.',
            })

        vals = {
            'name': (post.get('name') or '').strip(),
            'login': login,
            'bio': (post.get('bio') or '').strip(),
            'experience_level': post.get('experience_level') or False,
            'is_student': bool(post.get('is_student')),
            'is_instructor': bool(post.get('is_instructor')),
            'is_admin': bool(post.get('is_admin')),
        }

        user.write(vals)

        return request.redirect(f'/lms/user/{user_id}')