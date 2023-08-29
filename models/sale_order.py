# -*- coding: utf-8 -*-

from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.exceptions import AccessError, UserError, ValidationError

class SaleOrder(models.Model):
    _inherit = "sale.order"

    margin = fields.Monetary("Margin", groups="base.group_erp_manager")
    margin_percent = fields.Float("Margin (%)", groups="base.group_erp_manager")
    forma_entrega = fields.Selection([ ('Cargo Expreso', 'Cargo Expreso'),
                                      ('Forza', 'Forza'),('COD Forza','COD Forza'),('Guatex', 'Guatex'),
                                      ('Transporte propio', 'Transporte propio'),
                                     ('Cliente recoge', 'Cliente recoge'),
                                     ('Otro Transporte', 'Otro Transporte'),('no_aplica', 'No aplica')],'Forma entrega')
    transaccion_ids = fields.One2many('imporgesa.transaccion','venta_id', string="Transaccion")
    total_transaccion = fields.Monetary(string='Total transacciones', store=True, compute='_calculo_total', tracking=5)

    @api.onchange('transaccion_ids.numero_transaccion')
    def _revisar_numero_transaccion(self):
        for line in self:
            if line.numero_transaccion:
                transaccion_venta_id = self.env['imporgesa.transaccion'].search([('numero_transaccion', '=', line.numero_transaccion)])
                if transaccion_venta_id:
                    mensaje = "La transacción "+str(line.numero_transaccion) + " del banco " + str(transaccion_venta_id.banco_id.name ) + " de monto "+ str(transaccion_venta_id.monto) +" ya fue utilizada en el " + str(transaccion_venta_id.venta_id.name) + " del cliente " + str(transaccion_venta_id.venta_id.partner_id.name)
                    line.message_post(body=mensaje)
                    return {
                        'warning': {'title': "Warning", 'message': mensaje},
                    }

    @api.depends('transaccion_ids.monto')
    def _calculo_total(self):
        for order in self:
            total = 0
            for line in order.transaccion_ids:
                total += line.monto
            order.update({
                'total_transaccion': total,
            })

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
