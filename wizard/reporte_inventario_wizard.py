# -*- coding: utf-8 -*-

from odoo import models, fields, api
import xlsxwriter
import base64
import io
import logging
from datetime import datetime
import datetime

class ReporteInventarioWizard(models.TransientModel):
    _name = 'imporgesa.reporte_inventario.wizard'
    _description = "Wizard para reporte de inventarios"

    # fecha_inicio = fields.Date('Fecha inicio')
    # fecha_fin = fields.Date('Fecha fin')
    name = fields.Char('Nombre archivo', size=32)
    archivo = fields.Binary('Archivo', filters='.xls')

    def print_report(self):
        data = {
             'ids': [],
             'model': 'imporgesa.reporte_inventario.wizard',
             'form': self.read()[0]
        }
        return self.env.ref('imporgesa.action_reporte_inventario').report_action([], data=data)


    def print_report_excel(self):
        for w in self:
            f = io.BytesIO()
            libro = xlsxwriter.Workbook(f)
            hoja = libro.add_worksheet('Reporte de inventario')
            formato_titulo = libro.add_format({'size': 11, 'color':'#0d354d', 'align':'center', 'fg_color':'#ffffff', 'bold':False})
            #Tamaño de las columnas
            hoja.set_column('A:K', 20)

            hoja.write(1, 0, 'Código', formato_titulo)
            hoja.write(1, 1, 'Descripción', formato_titulo)
            hoja.write(1, 2, 'Marca', formato_titulo)
            hoja.write(1, 3, 'Categoría de producto', formato_titulo)
            hoja.write(1, 4, 'Bodega', formato_titulo)
            hoja.write(1, 5, 'Ubicación', formato_titulo)
            hoja.write(1, 6, 'Existencia', formato_titulo)
            hoja.write(1, 7, 'Costo', formato_titulo)
            hoja.write(1, 8, 'Precio', formato_titulo)
            hoja.write(1, 9, 'Última compra', formato_titulo)
            hoja.write(1, 10, 'Última venta', formato_titulo)

            informes_inventario = self.env['stock.quant'].search([])

            fila=2
            for inventario in informes_inventario:
                if inventario.location_id.usage == 'internal':
                    if inventario.product_id.default_code:
                        hoja.write(fila, 0, inventario.product_id.default_code)
                    hoja.write(fila, 1, inventario.product_id.name)
                    if inventario.product_id.marca:
                        hoja.write(fila, 2, inventario.product_id.marca)
                    if inventario.product_id.categ_id:
                        hoja.write(fila, 3, inventario.product_id.categ_id.name)
                    bodega = self.env['stock.warehouse'].search([('lot_stock_id', '=', inventario.location_id.id)])
                    if bodega:
                        hoja.write(fila, 4, bodega[0].name)
                    hoja.write(fila, 5, inventario.location_id.name)
                    hoja.write(fila, 6, inventario.inventory_quantity_auto_apply)
                    hoja.write(fila, 7, inventario.product_id.standard_price)
                    hoja.write(fila, 8, inventario.product_id.list_price)

                    ubicacion_id = self.env['stock.location'].search([('usage', '=', 'supplier')]).ids

                    if inventario.product_id and ubicacion_id:
                        stock_move_line = self.env['stock.move.line'].search([
                        ('product_id', '=', inventario.product_id.id),
                        ('location_id', 'in', ubicacion_id)],order='date asc')
                    else:
                        continue

                    if stock_move_line:
                        hoja.write(fila, 9, stock_move_line[0].date.strftime('%d/%m/%Y'))
                    else:
                        continue


                    ubicacion_id_customer = self.env['stock.location'].search([('usage', '=', 'customer')]).ids
                    if inventario.product_id and ubicacion_id_customer:
                        stock_move_line_venta = self.env['stock.move.line'].search([
                        ('product_id', '=', inventario.product_id.id),
                        ('location_id', 'in', ubicacion_id_customer)],order='date asc')
                        if stock_move_line_venta:
                            hoja.write(fila, 10, stock_move_line_venta[0].date.strftime('%d/%m/%Y'))
                    else:
                        continue


                    fila+=1


            libro.close()
            datos = base64.b64encode(f.getvalue())
            self.write({'archivo':datos, 'name':'Reporte_inventario.xlsx'})

        return {
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'imporgesa.reporte_inventario.wizard',
            'res_id': self.id,
            'view_id': False,
            'type': 'ir.actions.act_window',
            'target': 'new',
        }
