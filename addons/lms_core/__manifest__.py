{
    'name': 'LMS Core',
    'version': '1.0',
    'depends': ['website'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/templates.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'lms_core/static/src/css/style.css',
        ],
    },
    'installable': True,
    'application': False,
}