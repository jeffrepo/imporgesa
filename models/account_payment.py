# -*- coding: utf-8 -*-

from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.exceptions import AccessError, UserError, ValidationError


class AccountPayment(models.Model):
    _inherit = "account.payment"

    vendedor_id = fields.Many2one('res.partner', 'Vendedor')
