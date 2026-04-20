{
    'name': 'LMS Course Management',  
    'version': '1.0',
    'depends': ['lms_core','website'],  
    'data': [
        'views/templates.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'application': False,
}
