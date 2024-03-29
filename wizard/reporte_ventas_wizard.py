# -*- coding: utf-8 -*-

from odoo import models, fields, api
import xlsxwriter
import base64
import io
import logging
from datetime import datetime
# import datetime

class ReporteVentasWizard(models.TransientModel):
    _name = 'imporgesa.reporte_ventas.wizard'
    _description = "Wizard para reporte de ventas"

    fecha_inicio = fields.Date('Fecha inicio')
    fecha_fin = fields.Date('Fecha fin')
    name = fields.Char('Nombre archivo', size=32)
    archivo = fields.Binary('Archivo', filters='.xls')
    diario_ids = fields.Many2many('account.journal',string='Diarios de venta')

    def print_report(self):
        data = {
             'ids': [],
             'model': 'imporgesa.reporte_ventas.wizard',
             'form': self.read()[0]
        }
        return self.env.ref('imporgesa.action_reporte_ventas').report_action([], data=data)


    def print_report_excel(self):
        for w in self:

            f = io.BytesIO()
            libro = xlsxwriter.Workbook(f)
            hoja = libro.add_worksheet('Reporte de ventas')
            formato_titulo = libro.add_format({'size': 11, 'color':'#0d354d', 'align':'center', 'fg_color':'#ffffff', 'bold':False})
            #Tamaño de las columnas
            hoja.set_column('A:Y', 20)

            hoja.write(1, 0, 'Fecha', formato_titulo)
            hoja.write(1, 1, 'Correlativo interno', formato_titulo)
            hoja.write(1, 2, 'Numero', formato_titulo)
            hoja.write(1, 3, 'Serie', formato_titulo)
            hoja.write(1, 4, 'Código producto', formato_titulo)
            hoja.write(1, 5, 'Descripción producto', formato_titulo)
            hoja.write(1, 6, 'Marca', formato_titulo)
            hoja.write(1, 7, 'Categoría producto', formato_titulo)
            hoja.write(1, 8, 'Cantidad', formato_titulo)
            hoja.write(1, 9, 'Precio', formato_titulo)
            hoja.write(1, 10, 'Subtotal venta sin IVA', formato_titulo)
            # hoja.write(1, 11, 'Total venta', formato_titulo)
            hoja.write(1, 11, 'Costo', formato_titulo)
            hoja.write(1, 12, 'Subtotal costo', formato_titulo)
            hoja.write(1, 13, 'Cliente', formato_titulo)
            hoja.write(1, 14, 'NIT', formato_titulo)
            hoja.write(1, 15, 'Giro de negocio', formato_titulo)
            hoja.write(1, 16, 'Direccion', formato_titulo)
            hoja.write(1, 17, 'Departamento', formato_titulo)
            hoja.write(1, 18, 'Saldo', formato_titulo)
            hoja.write(1, 19, 'Utilidad', formato_titulo)
            hoja.write(1, 20, 'Margen', formato_titulo)
            hoja.write(1, 21, 'Vendedor', formato_titulo)
            hoja.write(1, 22, 'Correo electrónico', formato_titulo)
            hoja.write(1, 23, 'Teléfono', formato_titulo)
            hoja.write(1, 24, 'Celular', formato_titulo)

            tipo_factura = ['out_invoice', 'out_refund']

            facturas = self.env['account.move'].search([
            ('invoice_date', '>=', w.fecha_inicio),
            ('invoice_date', '<=', w.fecha_fin),
            ('journal_id','=', w.diario_ids.ids),
            ('move_type', 'in', tipo_factura)])

            fila=2

            for factura in facturas:
                subtotal_costo = 0
                direccion = []
                utilidad = 0
                margen = 0
                precio, price_total, standard_price, quantity, amount_residual = 0,0,0,0,0

                if factura.partner_id.street:
                    direccion.append(factura.partner_id.street)
                if factura.partner_id.street2:
                    direccion.append(factura.partner_id.street2)
                if factura.partner_id.city:
                    direccion.append(factura.partner_id.city)
                if factura.partner_id.country_id.name:
                    direccion.append(factura.partner_id.country_id.name)
                direccion = ' '.join(direccion)

                for linea in factura.invoice_line_ids:
                    format3 = libro.add_format({'num_format': 'dd/mm/yy'})
                    hoja.write(fila, 0, factura.invoice_date, format3)

                    hoja.write(fila, 1, factura.name)
                    if factura.fel_serie and factura.fel_numero:
                        hoja.write(fila, 2, factura.fel_numero)
                        hoja.write(fila, 3, factura.fel_serie)
                    if linea.product_id.default_code:
                        hoja.write(fila, 4, linea.product_id.default_code)
                    hoja.write(fila, 5, linea.product_id.name)
                    if linea.product_id.marca:
                        hoja.write(fila, 6, linea.product_id.marca)
                    hoja.write(fila, 7, linea.product_id.categ_id.name)

                    if factura.move_type == 'out_invoice' and factura.state == 'posted':
                        hoja.write(fila, 8, linea.quantity)
                        hoja.write(fila, 9, linea.price_unit)
                        hoja.write(fila, 10, linea.price_subtotal)
                        # hoja.write(fila, 11, linea.price_total)
                        hoja.write(fila, 11, linea.product_id.standard_price)
                        subtotal_costo = round(linea.product_id.standard_price * linea.quantity,2)
                        hoja.write(fila, 12, subtotal_costo)

                        hoja.write(fila, 18, factura.amount_residual)
                        utilidad = linea.price_total - subtotal_costo
                        hoja.write(fila, 19, utilidad)
                        margen = round(utilidad / linea.price_total,2)
                        hoja.write(fila, 20, margen)

                    elif factura.move_type == 'out_refund' and factura.state == 'posted':
                        quantity = linea.quantity * -1
                        hoja.write(fila, 8, quantity)
                        precio = linea.price_unit * -1
                        hoja.write(fila, 9, precio)
                        price_total = linea.price_total * -1
                        price_subtotal = linea.price_subtotal *-1
                        hoja.write(fila, 10, price_subtotal)
                        # hoja.write(fila, 11, price_total)
                        standard_price = linea.product_id.standard_price * -1
                        hoja.write(fila, 11, standard_price)
                        subtotal_costo = round(linea.product_id.standard_price * linea.quantity,2)
                        subtotal_costo = subtotal_costo * -1
                        hoja.write(fila, 12, subtotal_costo)
                        amount_residual = factura.amount_residual * -1
                        hoja.write(fila, 18, amount_residual)
                        utilidad = linea.price_total - subtotal_costo
                        utilidad = utilidad * -1
                        hoja.write(fila, 19, utilidad)
                        margen = round(utilidad / linea.price_total,2)
                        margen = margen * -1
                        hoja.write(fila, 21, margen)
                    elif factura.state == 'cancel':
                        hoja.write(fila, 8, int(0))
                        hoja.write(fila, 9, int(0))
                        hoja.write(fila, 10, int(0))
                        # hoja.write(fila, 11, int(0))
                        hoja.write(fila, 11, int(0))
                        hoja.write(fila, 12, int(0))
                        hoja.write(fila, 19, int(0))
                        hoja.write(fila, 20, int(0))
                        hoja.write(fila, 21, int(0))
                    else:
                        continue

                    hoja.write(fila, 13, factura.partner_id.name)
                    if factura.partner_id.vat:
                        hoja.write(fila, 14, factura.partner_id.vat)
                    if factura.partner_id.giro_negocio_id:
                        hoja.write(fila, 15, factura.partner_id.giro_negocio_id.name)
                    hoja.write(fila, 16, direccion)
                    hoja.write(fila, 17, factura.partner_id.state_id.name)


                    if factura.partner_id.email:
                        hoja.write(fila, 22, factura.partner_id.email)
                    if factura.partner_id.phone:
                        hoja.write(fila, 23, factura.partner_id.phone)
                    if factura.partner_id.mobile:
                        hoja.write(fila, 24, factura.partner_id.mobile)

                    fila+=1

            libro.close()
            datos = base64.b64encode(f.getvalue())
            self.write({'archivo':datos, 'name':'Reporte_ventas.xlsx'})

        return {
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'imporgesa.reporte_ventas.wizard',
            'res_id': self.id,
            'view_id': False,
            'type': 'ir.actions.act_window',
            'target': 'new',
        }
