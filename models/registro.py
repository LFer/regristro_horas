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
    hours = fields.Char(string="Tiempo Trabajado")
    left = fields.Char(string="Compensar")
    overhour = fields.Char(string="Horas Extras")
    week_load = fields.Float(string="Carga Semanal")#, compute='_week_load')
    var = fields.Float(string="test", default="3")
    hora_aproximada = fields.Char(string="Hora estamiada de relevo")



    # @api.one
    # @api.depends('week_load')
    # def _week_load(self):
    #     pdb.set_trace()
    #     if not self.var:
    #         self.week_load = 0.0
    #     else:
    #         self.week_load = 100.0 * self.hours / 45

    @api.one
    @api.depends('day')
    def _get_day(self):
        day = str((datetime.date.today().strftime("%A"),datetime.date.today().strftime("%d"),"de",datetime.date.today().strftime("%B"),"del", datetime.date.today().strftime("%Y"))).replace("'","").replace(",","").replace("(","").replace(")","")
        self.day = day

    @api.one
    def _check_lenght_lines(self):
#
        if len(self.detalle_ids)>=5:
            raise exceptions.ValidationError("No puede agregar mas de 5 linas por semana!")
    def _function(self):
        i = 0
        if self.var<=36:
            for x in (self.detalle_ids):
                i += x.hours
        self.var = i


    @api.one
    def _check_lenght_lines(self):
#
        if len(self.detalle_ids)>=5:
            raise exceptions.ValidationError("No puede agregar mas de 5 linas por semana!")

#     @api.one
#     @api.onchange('check_in')
#     def fecha_entrada(self):
# #        pdb.set_trace()
#         day = str((datetime.date.today().strftime("%A"),datetime.date.today().strftime("%d"),"de",datetime.date.today().strftime("%B"),"del", datetime.date.today().strftime("%Y"))).replace("'","").replace(",","").replace("(","").replace(")","")
#         if not self.check_in:
#             pass
#         else:
#             self.day = day

#     @api.one
#     @api.onchange('check_in')
#     def fecha(self):
# #        pdb.set_trace()
#         day = str((datetime.date.today().strftime("%A"),datetime.date.today().strftime("%d"),"de",datetime.date.today().strftime("%B"),"del", datetime.date.today().strftime("%Y"))).replace("'","").replace(",","").replace("(","").replace(")","")
#         if not self.day:
#             self.day = day
#         else:
#             self.day = day

#         if self.day:
#             self.day = day
#         else:
#             self.day = day

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
        pdb.set_trace()
        DATETIME_FORMAT = "%H:%M:%S"
        x = self.detalle_ids

        #-------------------------------------------------------------#
        lunes1 = datetime.datetime.strptime(x[0].hours, DATETIME_FORMAT)
        lunes_hora = lunes1.hour
        lunes_min = lunes1.minute
        lunes_sec = lunes1.second

        martes1 = datetime.datetime.strptime(x[1].hours, DATETIME_FORMAT)
        martes_hora = martes1.hour
        martes_min = martes1.minute
        martes_sec = martes1.second

        miercoles1 = datetime.datetime.strptime(x[2].hours, DATETIME_FORMAT)
        miercoles_hora = miercoles1.hour
        miercoles_min = miercoles1.minute
        miercoles_sec = miercoles1.second

        jueves1 = datetime.datetime.strptime(x[3].hours, DATETIME_FORMAT)
        jueves_hora = jueves1.hour
        jueves_min = jueves1.minute
        jueves_sec = jueves1.second

        viernes1 = datetime.datetime.strptime(x[4].hours, DATETIME_FORMAT)
        viernes_hora = viernes1.hour
        viernes_min = viernes1.minute
        viernes_sec = viernes1.second

        #-------------------------------------------------------------#
        # lunes2 = datetime.datetime.strptime(x[0].left, DATETIME_FORMAT)
        # lunes_hora_left = lunes2.hour
        # lunes_min_left = lunes2.minute
        # lunes_sec_left = lunes2.second

        # martes2 = datetime.datetime.strptime(x[1].left, DATETIME_FORMAT)
        # martes_hora_left = martes2.hour
        # martes_min_left = martes2.minute
        # martes_sec_left = martes2.second

        miercoles2 = datetime.datetime.strptime(x[2].left, DATETIME_FORMAT)
        miercoles_hora_left = miercoles2.hour
        miercoles_min_left = miercoles2.minute
        miercoles_sec_left = miercoles2.second

        # jueves2 = datetime.datetime.strptime(x[3].left, DATETIME_FORMAT)
        # jueves_hora_left = jueves2.hour
        # jueves_min_left = jueves2.minute
        # jueves_sec_left = jueves2.second

        viernes2 = datetime.datetime.strptime(x[4].left, DATETIME_FORMAT)
        viernes_hora_left = viernes2.hour
        viernes_min_left = viernes2.minute
        viernes_sec_left = viernes2.second

        #-------------------------------------------------------------#
        lunes3 = datetime.datetime.strptime(x[0].overhour, DATETIME_FORMAT)
        lunes_hora_extra = lunes3.hour
        lunes_min_extra = lunes3.minute
        lunes_sec_extra = lunes3.second

        martes3 = datetime.datetime.strptime(x[1].overhour, DATETIME_FORMAT)
        martes_hora_extra = martes3.hour
        martes_min_extra = martes3.minute
        martes_sec_extra = martes3.second

        # miercoles3 = datetime.datetime.strptime(x[2].overhour, DATETIME_FORMAT)
        # miercoles_hora_extra = miercoles3.hour
        # miercoles_min_extra = miercoles3.minute
        # miercoles_sec_extra = miercoles3.second

        jueves3 = datetime.datetime.strptime(x[3].overhour, DATETIME_FORMAT)
        jueves_hora_extra = jueves3.hour
        jueves_min_extra = jueves3.minute
        jueves_sec_extra = jueves3.second

        # viernes3 = datetime.datetime.strptime(x[4].overhour, DATETIME_FORMAT)
        # viernes_hora_extra = viernes3.hour
        # viernes_min_extra = viernes3.minute
        # viernes_sec_extra = viernes3.second

        #-------------------------------------------------------------#

        horas = lunes_hora + martes_hora + miercoles_hora + jueves_hora + viernes_hora
        minutos = lunes_min + martes_min + miercoles_min + jueves_min + viernes_min
        segundos = lunes_sec + martes_sec + miercoles_sec + jueves_sec + viernes_sec

        #-------------------------------------------------------------#

        horas_faltantes = miercoles_hora_left +  viernes_hora_left
        minutos_faltantes =  miercoles_min_left
        segundos_faltantes = miercoles_sec_left +  viernes_sec_left

        #-------------------------------------------------------------#

        horas_extra = lunes_hora_extra + martes_hora_extra + jueves_hora_extra
        minutos_extra = lunes_min_extra + martes_min_extra + jueves_min_extra
        segundos_extra = lunes_sec_extra + martes_sec_extra + jueves_sec_extra

        variables = {}
        al = {}
        pedo =  []






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

    name = fields.Char()
    registro_id = fields.Many2one('registro')
    day = fields.Char(string="Dia")#, compute='_get_day')
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

    # @api.one
    # @api.depends('day')
    # def _get_day(self):
    #     day = str((datetime.date.today().strftime("%A"),datetime.date.today().strftime("%d"),"de",datetime.date.today().strftime("%B"),"del", datetime.date.today().strftime("%Y"))).replace("'","").replace(",","").replace("(","").replace(")","")
    #     self.day = day
