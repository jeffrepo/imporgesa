# -*- coding: utf-8 -*-

from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.exceptions import AccessError, UserError, ValidationError


class AccountJournal(models.Model):
    _inherit = "account.journal"

    pago_comisiones = fields.One2many('account.journal.lineas_pago', 'pago_comision')

class AccountJournalLineas(models.Model):
    _name = 'account.journal.lineas_pago'
    _description= 'Se estan creando estas lineas para comisiones del empleado'

    pago_comision = fields.Many2one('account.journal')
    vendedor_id = fields.Many2one('res.partner', 'Vendedor')
    comision = fields.Float('Comision %')
