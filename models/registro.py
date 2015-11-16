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
    check_in = fields.Datetime(string = 'Entrada', default = fields.Date.context_today)
    check_out = fields.Datetime(string = 'Salida')
    detalle_ids = fields.One2many(comodel_name='detalle', inverse_name='registro_id')#, readonly=True)
    #para probar las funciones
    day = fields.Char(string="Dia")
    hours = fields.Char(string="Tiempo Trabajado")
    left = fields.Char(string="Compensar")
    overhour = fields.Char(string="Horas Extras")
    week_load = fields.Float(string="Carga Semanal")#, compute='_taken_seats')


    @api.one
    @api.onchange('detalle_ids')
    def fecha(self):
        lista = self.detalle_ids
        if len(linsta)>5:
            print "Hello"

    @api.onchange('hours')
    def fecha_this_will_work(self):
        if self.hours:
            pdb.set_trace()
            pass
        else:    
            lista = self.detalle_ids
            if len(linsta)>8:
                print "Hello"
    @api.one
    @api.onchange('day')
    def fecha(self):
#        pdb.set_trace()
        if not self.day:
            var = str((datetime.date.today().strftime("%A"),datetime.date.today().strftime("%d"),"de",datetime.date.today().strftime("%B"),"del", datetime.date.today().strftime("%Y"))).replace("'","").replace(",","").replace("(","").replace(")","")
            self.day = var
        else:
            print "No lo logro"
#        pdb.set_trace()
   





        

        # tabla = self.detalle_ids.ids     
        # for x in tabla:
        #     self.env.cr.execute(""" DELETE FROM ONLY detalle WHERE id = %(x)s  """,{'x':x})           
    @api.one
    def _check_lines(self):#TODO Hacerla mas escricta
#        pdb.set_trace()
        lista = self.detalle_ids.ids
        if len(lista) !=0:    
            for x in lista:
                y = self.env['detalle'].browse(x)            
                if y.check_in == self.check_in or y.check_out == self.check_out:
                    raise exceptions.ValidationError("No puede Calcular horas para el mismo dia!")

    # @api.one
    # def _double_check(self,check_in, check_out):
    #     lista = self.detalle_ids.ids
    #     if len(lista) !=0:    
    #         for x in lista:
    #             y = self.env['detalle'].browse(x)            
    #             if y.check_in == self.check_in or y.check_out == self.check_out:
    #                 raise exceptions.ValidationError("No puede Calcular horas para el mismo dia!")       


    @api.one
    def horas_trabajadas(self):
#        pdb.set_trace()
        self._check_lines()
        res = ""
        if (self.check_out and self.check_in) and (self.check_in <= self.check_out):
            DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
            to_dt = datetime.datetime.strptime(self.check_out, DATETIME_FORMAT)
            from_dt = datetime.datetime.strptime(self.check_in, DATETIME_FORMAT)
            timedelta = to_dt - from_dt
            diff_day = timedelta.days + float(timedelta.seconds) / 3600
            res = diff_day
            self.hours = res
            horas = round(math.floor(diff_day))
            x = res - int(res)
            minutos = x*60
            minutosfloor = round(math.floor(minutos))
            segundos = minutos/60
            segundosfloor = str(segundos - int(segundos))[1:4].replace('.',':')
            #para devolver pasamos todo a strings
            horastring = str(horas).replace('.',':').replace('0','')
            minutostring = str(minutosfloor).replace('0','').replace('.','')
            horas_trabajadas = horastring + minutostring
            self.hours = horas_trabajadas
        if not self.check_out:
            raise exceptions.except_orm(_('Error!'), _('Debe Ingresar un Horario de Salida.'))
        if horas >= 9:
#            pdb.set_trace()
            self.overhour = str(int(horas-9)) + ":" + minutostring
            self.left = ''
        else:
            self.left = str(int(math.fabs(int(horas-9)))) + ":" + str(int(60-minutos))
            self.overhour = ''
            
        lineas = {
                'day':self.day,
                'hours':self.hours,
                'left':self.left,
                'overhour':self.overhour,
                'check_in':self.check_in,
                'check_out':self.check_out,
                }
        lineas2=[(0,0,lineas)]
        self.write({'detalle_ids':lineas2})
        return        


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
    week_load = fields.Float(string="Carga Semanal")#, compute='_taken_seats')

