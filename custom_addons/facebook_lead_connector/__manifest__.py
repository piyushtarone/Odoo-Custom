{
    'name': 'Facebook Lead Connector',
    'version': '1.0',
    'category': 'CRM',
    'summary': 'Facebook Lead Form Integration',
    'author': 'Piyush',
    'depends': [
        'base',
        'crm'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/facebook_config_views.xml',
    ],
    'installable': True,
    'application': True,
}
