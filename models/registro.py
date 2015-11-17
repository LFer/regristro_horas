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
    _rec_name="day"
#
    check_in = fields.Datetime(string = 'Entrada', default = datetime.date.today())
    check_out = fields.Datetime(string = 'Salida')
    detalle_ids = fields.One2many(comodel_name='detalle', inverse_name='registro_id')#, readonly=True)
    #para probar las funciones
    day = fields.Char(string="Dia")
    hours = fields.Char(string="Tiempo Trabajado")
    left = fields.Char(string="Compensar")
    overhour = fields.Char(string="Horas Extras")
    week_load = fields.Float(string="Carga Semanal")#, compute='_week_load')
    var = fields.Float(string="test", default="3")



    # @api.one
    # @api.depends('week_load')
    # def _week_load(self):
    #     pdb.set_trace()
    #     if not self.var:
    #         self.week_load = 0.0
    #     else:
    #         self.week_load = 100.0 * self.hours / 45



    def _function(self):
        i = 0
        if self.var<=36:
            for x in (self.detalle_ids):
                i += x.hours
        self.var = i


    @api.one
    def _check_lenght_lines(self):
#        pdb.set_trace()
        if len(self.detalle_ids)>=5:
            raise exceptions.ValidationError("No puede agregar mas de 5 linas por semana!")

    @api.one
    @api.onchange('day')
    def fecha(self):
        day = self.day = str((datetime.date.today().strftime("%A"),datetime.date.today().strftime("%d"),"de",datetime.date.today().strftime("%B"),"del", datetime.date.today().strftime("%Y"))).replace("'","").replace(",","").replace("(","").replace(")","")
        return day


    @api.one
    def _check_lines(self):#TODO Hacerla mas escricta
#        pdb.set_trace()
        lista = self.detalle_ids.ids
        if len(lista) !=0:
            for x in lista:
                y = self.env['detalle'].browse(x)
                if y.check_in == self.check_in or y.check_out == self.check_out:
                    raise exceptions.ValidationError("No puede Calcular horas para el mismo dia!")


    @api.one
    def horas_trabajadas(self):
#        pdb.set_trace()
        self._check_lines()
        self._check_lenght_lines()
        res = ""
        if (self.check_out and self.check_in) and (self.check_in <= self.check_out):
            DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
            to_dt = datetime.datetime.strptime(self.check_out, DATETIME_FORMAT)
            from_dt = datetime.datetime.strptime(self.check_in, DATETIME_FORMAT)
            tiempo_trabajado = to_dt - from_dt
            self.hours = tiempo_trabajado
            tope = datetime.timedelta(0, 32400)
            if tiempo_trabajado.seconds == tope.seconds:
                self.left = ''
                self.overhour = ''
                self.week_load = 100 * tiempo_trabajado.seconds / tope.seconds
            if tiempo_trabajado.seconds >= tope.seconds:
                if tiempo_trabajado.seconds - tope.seconds > 0:
                    self.overhour = tiempo_trabajado - tope
                    self.left = ''
                    self.week_load = 100 * tiempo_trabajado.seconds / tope.seconds
            else:
                self.left = tope - tiempo_trabajado
                self.week_load = 100 * tiempo_trabajado.seconds / tope.seconds
                self.overhour = ''

            lineas = {
                    'day':self.day,
                    'hours':self.hours,
                    'left':self.left,
                    'overhour':self.overhour,
                    'check_in':self.check_in,
                    'check_out':self.check_out,
                    'week_load':self.week_load,
                    }
            lineas2=[(0,0,lineas)]
            return self.write({'detalle_ids':lineas2})



registro()

class detalle(models.Model):
    _name="detalle"

    registro_id = fields.Many2one('registro')
    day = fields.Char   (string="Dia")
    hours = fields.Char(string="Horas")
    left = fields.Char(string="Compensar")
    overhour = fields.Char(string="Horas Extras")
    check_in = fields.Datetime(string = 'Entrada')
    check_out = fields.Datetime(string = 'Salida')
    week_load = fields.Float(string="Carga Semanal")#, compute='_carga_semanal')

    # @api.one
    # @api.depends('hours', 'week_load')
    # def _carga_semanal(self):
    #     if not self.hours:
    #         self.week_load = 0.0
    #     else:
    #         self.week_load = 100 * self.hours/9
