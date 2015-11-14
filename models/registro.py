# -*- coding: utf-8 -*-
from openerp import models, fields, _, api, exceptions
from openerp.exceptions import Warning
import logging
import openerp.addons.decimal_precision as dp
_logger = logging.getLogger(__name__)
import ipdb as pdb

class registro(models.Model):
    _name="registro"

    check_in = fields.Datetime(string = 'Entrada', default = fields.Date.context_today)
    check_out = fields.Datetime(string = 'Salida')
    detalle_ids = fields.One2many(comodel_name='detalle', inverse_name='registro_id')
    #para probar las funciones
    day = fields.Char(string="Dia")
    hours = fields.Char(string="Horas")
    left = fields.Char(string="Compensar")
    overhour = fields.Char(string="Horas Extras")

    @api.one
    def dow(self):
        pdb.set_trace()
        date = self.check_in
        days=["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
        dayNumber=date.weekday()
        print days[dayNumber]    

registro()

class detalle(models.Model):
    _name="detalle"

    registro_id = fields.Many2one('registro')
    day = fields.Char(string="Dia")
    hours = fields.Char(string="Horas")
    left = fields.Char(string="Compensar")
    overhour = fields.Char(string="Horas Extras")