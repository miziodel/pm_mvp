# -*- coding: utf-8 -*-
{
    'name': "pm_mvp",

    'summary': """
        PM MVP extends Odoo Project Management basic and OCA modules for a different
        project management experience""",

    'description': """
        PM MVP extends basic PM modules adding:
        - projects dashboard for status overview
        - projects timeline for monthly planning
        - projects scheduled actions for immediate critical actions
        - ...
    """,

    'author': "Maurizio Delmonte",
    'website': "https://www.linkedin.com/in/mdelmonte",
    'license': 'AGPL-3',


    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Project Management',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 
                'web_timeline',
                'project',
                'project_list',
                'project_status',
                'project_timeline',
                'project_description',
                'project_key',
                'project_milestone',
                'project_parent_task_filter',
                'project_tag',
                'project_timesheet_time_control',
                ],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/milestone_views.xml',
        'views/project_views.xml',
        'views/task_views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}