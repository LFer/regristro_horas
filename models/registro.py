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

registro()