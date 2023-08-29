# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools, _

class ImporgesaTransaccion(models.Model):
    _name = "imporgesa.transaccion"

    venta_id = fields.Many2one('sale.order','Venta')
    forma_pago_id = fields.Many2one('imporgesa.forma_pago','Forma de pago')
    banco_id = fields.Many2one('imporgesa.banco', 'Banco')
    numero_transaccion = fields.Char('Número de transacción')
    monto = fields.Float('Monto')

    @api.onchange('numero_transaccion')
    def _revisar_numero_transaccion(self):
        for line in self:
            if line.numero_transaccion:
                transaccion_venta_id = self.env['imporgesa.transaccion'].search([('numero_transaccion', '=', line.numero_transaccion)])
                if transaccion_venta_id:
                    mensaje = "La transaccion "+str(line.numero_transaccion) + " del banco "+ str(line.banco_id.name) +" de monto "+ str(line.monto)+" ya fue utilizada en el pedido " + str(transaccion_venta_id.venta_id.name) + " del cliente " +str(transaccion_venta_id.venta_id.partner_id.name)
                    venta_id = self._context.get('venta_id')
                    venta_search_id = self.env['sale.order'].search([('id','=',venta_id)])
                    if venta_search_id:
                        venta_search_id.message_post(body=mensaje)
                    return {
                        'warning': {'title': "Warning", 'message': mensaje},
                    }

class ImporgesaTransaccion(models.Model):
    _name = "imporgesa.forma_pago"

    name = fields.Char('Name')

class ImporgesaBanco(models.Model):
    _name = "imporgesa.banco"

    name = fields.Char('Name')

class ImporgesaGiroNegocio(models.Model):
    _name = "imporgesa.giro_negocio"

    name = fields.Char('Nombre')

class AccountInvoiceReport(models.Model):
    _inherit = "account.invoice.report"

    default_code = fields.Char(string='Referencia interna', readonly=True)
    nombre_producto = fields.Char(string='Nombre de producto', readonly=True)
    subtotal_costo = fields.Float(string='Subtotal costo', readonly=True, groups=('base.group_erp_manager'))
    subtotal_utilidad = fields.Float(string='Subtotal utilidad', readonly=True, groups=('base.group_erp_manager'))
    margen = fields.Float(string="Margen %", readonly=True, group_operator="avg", groups=('base.group_erp_manager'))
    numero_factura = fields.Char(string="Numero de factura", readonly=True)

    def _select(self):
        select_str = super(AccountInvoiceReport, self)._select()
        select_str += """
                ,template.default_code as default_code,
                template.name as nombre_producto,
                (prop.value_float * line.quantity) * (CASE WHEN move.move_type IN ('out_refund') THEN -1 ELSE 1 END)  as subtotal_costo,
                ((-line.balance *(CASE WHEN move.move_type IN ('out_refund') THEN -1 ELSE 1 END)* currency_table.rate)-(prop.value_float * line.quantity)) * (CASE WHEN move.move_type IN ('out_refund') THEN -1 ELSE 1 END) as subtotal_utilidad,
                ((((-line.balance *(CASE WHEN move.move_type IN ('out_refund') THEN -1 ELSE 1 END) * currency_table.rate)-(prop.value_float * line.quantity)) / (-line.balance * currency_table.rate))*100) as margen,
                CONCAT(move.fel_serie, '-', move.fel_numero) AS numero_factura
            """
        return select_str

    def _from(self):
        from_str = super(AccountInvoiceReport, self)._from()
        from_str += """
                JOIN ir_property prop on prop.res_id = 'product.product,' || product.id \
            """
        return from_str

    def _where(self):
        where_str = super(AccountInvoiceReport, self)._where()
        where_str += """
                GROUP BY
                    line.id,
                    move.state,
                    move.move_type,
                    move.partner_id,
                    move.invoice_user_id,
                    move.fiscal_position_id,
                    move.payment_state,
                    move.invoice_date,
                    move.invoice_date_due,
                    uom_template.id,
                    template.categ_id,
                    uom_line.factor,
                    uom_template.factor,
                    currency_table.rate,
                    partner.country_id,
                    commercial_partner.country_id,
                    move.team_id,
                    template.default_code,
                    template.name,
                    prop.value_float,
                    move.fel_serie,
                    move.fel_numero
            """
        return where_str
