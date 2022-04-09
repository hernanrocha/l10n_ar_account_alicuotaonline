# -*- coding: utf-8 -*-
{
    'name': "Consulta de padrón en AlicuotaOnline.com",
    'summary': """""",
    'description': """
        Extensión del módulo base de Contabilidad Argentina para conectar con AlicuotaOnline
    """,
    'author': "AlicuotaOnline.com",
    'website': "https://alicuotaonline.com",
    'category': 'Localization/Argentina',
    'version': '11.0.0.1',
    'depends': ['l10n_ar_account_withholding'],
    'data': [
        'security/ir.model.access.csv',

        'views/iibb_views.xml',
        'views/table_views.xml',
        'views/account_menuitem.xml',

        'wizard/res_config_settings_views.xml',
    ],
    'demo': [],
}