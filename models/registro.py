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
from datetime import date
import calendar

class registro(models.Model):
    _name="registro"
    _rec_name="day"
#
    name = fields.Char()
    check_in = fields.Datetime(string = 'Entrada', default =datetime.date.today())
    check_out = fields.Datetime(string = 'Salida')
    detalle_ids = fields.One2many(comodel_name='detalle', inverse_name='registro_id')#, readonly=True)
    #para probar las funciones
    day = fields.Char(string="Dia", compute='_get_day')
    week_day = fields.Char(string="Dia")
    hours = fields.Char(string="Tiempo Trabajado")
    left = fields.Char(string="Compensar")
    overhour = fields.Char(string="Horas Extras")
    week_load = fields.Float(string="Carga Semanal")#, compute='_week_load')
    var = fields.Char(string="Carga Semanal")#, compute='sumer_horas_semanales')
    hora_aproximada = fields.Char(string="Hora estamiada de relevo")


    @api.one
    @api.depends('day')
    def _get_day(self):
        day = str((datetime.date.today().strftime("%A"),datetime.date.today().strftime("%d"),"de",datetime.date.today().strftime("%B"),"del", datetime.date.today().strftime("%Y"))).replace("'","").replace(",","").replace("(","").replace(")","")
        self.day = day

    @api.one
    def _check_lenght_lines(self):
        if len(self.detalle_ids)>=5:
            raise exceptions.ValidationError("No puede agregar mas de 5 linas por semana!")

    @api.one
    def _check_lenght_lines(self):
        if len(self.detalle_ids)>=5:
            raise exceptions.ValidationError("No puede agregar mas de 5 linas por semana!")

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
    def estimar_horas_trabajadas(self):
#        pdb.set_trace()
        res = ""
        if self.check_in:
            DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
            DATETIME_FORMATEO = "%H:%M:%S"
            from_dt = datetime.datetime.strptime(self.check_in, DATETIME_FORMAT)
            tope = datetime.timedelta(0, 32400)
            tope2 = datetime.timedelta(0,21600)
            hoy = datetime.datetime.now()
            ahora = date
            string_hoy = str(hoy)
            corte = string_hoy[:19]
            hoy_objeto = datetime.datetime.strptime(corte, DATETIME_FORMAT)
            #nos quedamos solo con las horas
            #paso a sintg y me quedo con la hora
            entrada = str(from_dt)[11:]
            #lo paso a objecto datetime
            entrada_objeto = datetime.datetime.strptime(entrada, DATETIME_FORMATEO)
            salida_aproximada = from_dt + tope2
            salida_string = str(salida_aproximada)[11:]
            self.hora_aproximada = salida_string

    @api.one
    def sumer_horas_semanales(self):
        DATETIME_FORMAT = "%H:%M:%S"
        FORMAT0 = "%H:%M:%S"
        x = self.detalle_ids
        h = 0
        m = 0
        s = 0
        for i in x:
            lista1 = i.hours.split(':')
            h += int(lista1[0])
            m += int(lista1[1])
            s += int(lista1[2])
        while s>=60:
            s-=60
            m+=1
        while m>=60:
            m-=60
            h+=1
        lista2 = [h,m,s]
        self.var = str(lista2[0]) + ":" + str(lista2[1]) + ":" + str(lista2[2]) + str("/") + str("45")


    @api.one
    def horas_trabajadas(self):
        pdb.set_trace()
        self._check_lines()
        self._check_lenght_lines()

        #Vemos si podemos agarrar el dia
        weekday = date.today()
        today = calendar.day_name[weekday.weekday()]
        if today == 'Monday':
            self.week_day = 'Lunes'

        if today == 'Tuesday':
            self.week_day = 'Martes'

        if today == 'Wednesday':
            self.week_day = 'Miércoles'

        if today == 'Thursday':
            self.week_day = 'Jueves'

        if today == 'Friday':
            self.week_day == 'Viernes'


        res = ""
        if (self.check_out and self.check_in) and (self.check_in <= self.check_out):
            DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
            to_dt = datetime.datetime.strptime(self.check_out, DATETIME_FORMAT)
            from_dt = datetime.datetime.strptime(self.check_in, DATETIME_FORMAT)
            tiempo_trabajado = to_dt - from_dt
            self.hours = tiempo_trabajado
            tope = datetime.timedelta(0, 32400)
            salida_aproximada = from_dt + tope
            self.hora_aproximada = salida_aproximada
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
                    'week_day':self.week_day,
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

    name = fields.Char()
    registro_id = fields.Many2one('registro')
    day = fields.Char(string="Dia")#, compute='_get_day')
    week_day = fields.Char(string="Dia")
    hours = fields.Char(string="Horas")
    left = fields.Char(string="Compensar")
    overhour = fields.Char(string="Horas Extras")
    check_in = fields.Datetime(string = 'Entrada')
    check_out = fields.Datetime(string = 'Salida')
    week_load = fields.Float(string="Carga Diaria")#, compute='_carga_semanal')
