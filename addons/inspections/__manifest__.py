{
    'name': 'Inspection',
    'version': '0.1',
    'author': 'Jose Eli',
    'category': 'Services',
    'depends': ['base'],
    'description': """
Inspection process
====================

""",

    'data': [
        'security/ir.model.access.csv',

        'data/inspection_stage_data.xml',

        'views/inspection_views.xml',
        'views/templates.xml',

    ],
    'demo': [

    ],
    'license': 'LGPL-3',
}