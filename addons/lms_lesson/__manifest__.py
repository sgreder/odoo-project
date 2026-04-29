{
    'name': 'LMS Lesson',
    'version': '17.0.1.0.0',
    'summary': 'Defines the lms.lesson and lms.lesson.content models',
    'category': 'Education',
    'author': 'Your Company',
    'depends': ['base', 'lms_course_management'],
    'data': [
        'security/ir.model.access.csv',
        'views/lms_lesson_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
