# -*- coding: utf-8 -*-

from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.exceptions import AccessError, UserError, ValidationError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def action_confirm(self):
        for sale in self:
            product_zero = False
            list_product = []
            if sale.order_line:
                for line in sale.order_line:
                    if line.qty_available_today < line.product_uom_qty:
                        product_zero = True
                        list_product.append(line.product_id.name)

            if product_zero and len(list_product) > 0:
                raise UserError(_(
                    'Productos sin existencia: ' + ','.join(list_product) ))
        return super(SaleOrder, self).action_confirm()
