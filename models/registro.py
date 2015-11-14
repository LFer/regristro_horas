# -*- coding: utf-8 -*-
from openerp import models, fields, _, api, exceptions
from openerp.exceptions import Warning
import logging
import openerp.addons.decimal_precision as dp
_logger = logging.getLogger(__name__)
import ipdb as pdb
import datetime
import time
from datetime import timedelta
import math


class registro(models.Model):
    _name="registro"
#        
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
        var = str((datetime.date.today().strftime("%A"),datetime.date.today().strftime("%d"),"de",datetime.date.today().strftime("%B"),"del", datetime.date.today().strftime("%Y"))).replace("'","").replace(",","")
        date = self.check_in
        days=["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
        dayNumber=date.weekday()

        print days[dayNumber]    
    
    @api.onchange('day')
    def fecha(self):
#        pdb.set_trace()
        if not self.day:
            var = str((datetime.date.today().strftime("%A"),datetime.date.today().strftime("%d"),"de",datetime.date.today().strftime("%B"),"del", datetime.date.today().strftime("%Y"))).replace("'","").replace(",","").replace("(","").replace(")","")
            self.day = var
        else:
            print "No lo logro"

#    @api.onchange('day')
    @api.one
    def horas_trabajadas(self):
#        pdb.set_trace()        
        res = ""
        if (self.check_out and self.check_in) and (self.check_in <= self.check_out):
            DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
            to_dt = datetime.datetime.strptime(self.check_out, DATETIME_FORMAT)
            from_dt = datetime.datetime.strptime(self.check_in, DATETIME_FORMAT)
            timedelta = to_dt - from_dt
            diff_day = timedelta.days + float(timedelta.seconds) / 3600
            res = diff_day
            self.hours = res
        return res
#        horas divido entre 3600
#        minutos divido entre 60
            # puede servir
            # c = time.strptime("2002-03-14 17:42:00","%Y-%m-%d %H:%M:%S")
            # t = time.mktime(c)
            # t = t + 1800 #30 minutes is 1800 secs
            # time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(t))
            # '2002-03-14 18:12:00'
registro()

class detalle(models.Model):
    _name="detalle"

    registro_id = fields.Many2one('registro')
    day = fields.Char(string="Dia")
    hours = fields.Char(string="Horas")
    left = fields.Char(string="Compensar")
    overhour = fields.Char(string="Horas Extras")
