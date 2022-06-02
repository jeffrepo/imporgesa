# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.tools.misc import formatLang
from odoo.exceptions import RedirectWarning, UserError, ValidationError, AccessError

import logging

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        self.verificacion_cliente_vedado()
        return res

    def verificacion_cliente_vedado(self):
        clientes = self.env['res.partner'].search([('id', '=', self.partner_id.id), ('vedado', '=', True)])

        for cliente in clientes:
            if cliente.vedado:
                raise UserError(_('El cliente '+cliente.name+ ' esta vedado'))


        return True
