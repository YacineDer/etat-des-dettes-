{
    'name': 'État des Dettes',
    'version': '1.0',
    'summary': 'Track unpaid supplier invoices',
    'category': 'Accounting',
    'author': 'Yacine Deradra',
    'depends': ['account'],
    'data': [
        'security/ir.model.access.csv',
        'views/supplier_debt_views.xml',
        'reports/supplier_debt_report.xml',
        'views/supplier_debt_menu.xml',
    ],
    'installable': True,
    'application': False,
}
