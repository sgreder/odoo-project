{
    'name': 'LMS Core',
    'version': '1.0',
    'depends': [
        'base',        
        'website',     
    ],
    'data': [
        'views/templates.xml',
        # add security files later:
        # 'security/ir.model.access.csv',
        # 'security/security.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'lms_core/static/src/css/style.css',
        ],
    },
    'installable': True,
    'application': False,
}