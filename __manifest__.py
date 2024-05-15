# -*- coding: utf-8 -*-
{
    'name': "Imporgesa",

    'summary': """ Imporgesa """,

    'description': """
        Imporgesa
    """,

    'author': "STECHNOLOGIES",
    'website': "",

    'category': 'Uncategorized',
    'version': '0.1',

    'depends': ['product','base','sale', 'stock', 'sale_margin','account_gt'],

    'data': [
        'security/ir.model.access.csv',
        'report/cotizacion_supersemiagro.xml',
        'report/cotizacion_supersemiagro_nutrifod.xml',
        # 'views/product_template_views.xml',
        'views/product_views.xml',
        # 'views/product_template_views.xml',
        'views/res_partner_views.xml',
        'views/sale_views.xml',
        #'views/reporte_libro_diario_views.xml',
        'views/account_report.xml',
        #'views/account_journal_views.xml',
        'views/account_payments_views.xml',
        'views/account_payments_register_views.xml',
        'report/reporte_cheque_bi_view.xml',
        'wizard/recuperacion_pagos_wizard_views.xml',
        'wizard/reporte_ventas_wizard_views.xml',
        'wizard/reporte_inventario_wizard_views.xml',
        'report/label_code_price.xml',
        'report/label_code_view.xml',
        'report/label_code_price_two_view.xml',
        'report/label_code_two_view.xml',
        'report/stock_report_views.xml',
        'report/label_code_lines_view.xml',
        'report/label_code_lines_two_view.xml',
        'views/res_config_settings_views.xml',
        'report/sale_report.xml'
    ],
    'qweb': [
    ],
    'license': 'LGPL-3',
}
