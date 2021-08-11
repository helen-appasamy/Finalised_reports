# -*- coding: utf-8 -*-
{
    'name' : 'GRN-Bill Validation Report',
    'version' : '1.1',
    'summary': 'Bill details agaisnt the Transfer reference',
    'depends' : ['base','sale'],
    'data': [
        'security/grn_security.xml',
        'security/ir.model.access.csv',
        'views/grn_bill.xml'
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    }