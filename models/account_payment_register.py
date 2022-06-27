# -*- coding: utf-8 -*-
from collections import defaultdict
from lxml import etree

from odoo import models, fields, api, _
from odoo.exceptions import UserError
from odoo.tools import float_compare, frozendict


class AccountPaymentRegister(models.TransientModel):
    _inherit = 'account.payment.register'

    vendedor_id = fields.Many2one('res.partner', 'Vendedor')

    def _create_payment_vals_from_wizard(self):
        vals = super()._create_payment_vals_from_wizard()
        if self.vendedor_id.id:
            vals.update({'vendedor_id': self.vendedor_id.id})
        return vals
