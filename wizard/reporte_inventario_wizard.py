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

    fecha_inicio = fields.Date('Fecha inicio')
    fecha_fin = fields.Date('Fecha fin')
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
            dict = {}
            dict['fecha_inicio'] = w.fecha_inicio
            dict['fecha_fin'] = w.fecha_fin

            f = io.BytesIO()
            libro = xlsxwriter.Workbook(f)
            hoja = libro.add_worksheet('Reporte de inventario')
            formato_titulo = libro.add_format({'size': 11, 'color':'#0d354d', 'align':'center', 'fg_color':'#ffffff', 'bold':False})
            #Tamaño de las columnas
            hoja.set_column('A:H', 20)

            hoja.write(1, 0, 'Código', formato_titulo)
            hoja.write(1, 1, 'Descripción', formato_titulo)
            hoja.write(1, 2, 'Marca', formato_titulo)
            hoja.write(1, 3, 'Categoría de producto', formato_titulo)
            hoja.write(1, 4, 'Bodega', formato_titulo)
            hoja.write(1, 5, 'Ubicación', formato_titulo)
            hoja.write(1, 6, 'Existencia', formato_titulo)
            hoja.write(1, 7, 'Costo', formato_titulo)
            hoja.write(1, 8, 'Precio', formato_titulo)


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
