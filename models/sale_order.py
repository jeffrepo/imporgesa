# -*- coding: utf-8 -*-

from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.exceptions import AccessError, UserError, ValidationError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    margin = fields.Monetary("Margin", groups="base.group_erp_manager")
    margin_percent = fields.Float("Margin (%)", groups="base.group_erp_manager")

    def action_confirm(self):
        for sale in self:
            product_zero = False
            list_product = []
            if sale.order_line:
                for line in sale.order_line:
                    if line.product_id.detailed_type =='product' and line.qty_available_today < line.product_uom_qty:
                        product_zero = True
                        list_product.append(line.product_id.name)

            if product_zero and len(list_product) > 0:
                raise UserError(_(
                    'Productos sin existencia: ' + ','.join(list_product) ))
                
            if self.env.user.has_group('base.group_erp_manager') == False:
                margen_venta = self.env['ir.config_parameter'].sudo().get_param('sale.margen_venta')
                if float(margen_venta) > 0:
                    self.sale_price_verify(sale,float(margen_venta))
        return super(SaleOrder, self).action_confirm()

    def sale_price_verify(self,sale,margen_venta):
        if sale.order_line:
            for line in sale.order_line:
                formula = (line.product_id.standard_price * 1.12/(1-margen_venta))
                if line.price_unit < formula:
                    raise UserError(_(
                    'Precio de ventar menor al margen: ' + str(line.product_id.name) ))
        return True

class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    margin = fields.Float(
        "Margin", groups="base.group_erp_manager")
    margin_percent = fields.Float(
        "Margin (%)", groups="base.group_erp_manager")
