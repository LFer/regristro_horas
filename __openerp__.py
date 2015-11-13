# -*- coding: utf-8 -*-
{
    'name': 'Registro de Horas Trabajadas',
    'version': '1.0',
    'author': 'Felipe Ferreira',
    'website': 'http://www.datamatic.com.uy',
    'category': 'Recursos Humanos',
    'summary': '',
    'description': """
    Calcula las horas trabajadas, horas a compensar y horas extras.
    """,
    'depends': ['base','hr'],
    'data': [
        'views/registro_view.xml',
    ],
    'installable': True,
    'auto_install': False,
}
