# -*- coding: utf-8 -*-

from odoo import models, fields, api

from functools import lru_cache
import logging


class ReporteEtiquetaSinPrecio (models.AbstractModel):
    _name='report.imporgesa.label_code_view'
    _description='Creado para la etiqueta sin precio'

    def creacion_datos(self, orders):
        dicc_products={}
        for order in orders:
            for linea in order.order_line:
                if linea.product_id.default_code not in dicc_products:
                    dicc_products[linea.product_id.default_code]=[]
                for i in range(int(linea.product_uom_qty)):
                    if linea.product_id.default_code in dicc_products:
                        dicc_products[linea.product_id.default_code].append({
                        'codigo':linea.product_id.default_code,
                        'descripcion': linea.product_id.name,
                        'codigo_barras': linea.product_id.barcode
                        })
        return dicc_products

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['sale.order'].browse(docids)
        dicc_products = self.creacion_datos(docs)
        return {
            'doc_ids': docids,
            'doc_model': 'sale.order',
            'docs': docs,
            'dicc_products': dicc_products,
        }

class ReporteEtiquetaConPrecio (models.AbstractModel):
    _name='report.imporgesa.label_code_price_view'
    _description='Creado para la etiqueta con precio'

    def creacion_datos(self, orders):
        dicc_products_price={}
        for order in orders:
            for linea in order.order_line:
                if linea.product_id.default_code not in dicc_products_price:
                    dicc_products_price[linea.product_id.default_code]=[]
                for i in range(int(linea.product_uom_qty)):
                    if linea.product_id.default_code in dicc_products_price:
                        dicc_products_price[linea.product_id.default_code].append({
                        'codigo':linea.product_id.default_code,
                        'descripcion': linea.product_id.name,
                        'precio':linea.product_id.list_price,
                        'codigo_barras': linea.product_id.barcode
                        })
        return dicc_products_price

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['sale.order'].browse(docids)
        dicc_products_price = self.creacion_datos(docs)
        return {
            'doc_ids': docids,
            'doc_model': 'sale.order',
            'docs': docs,
            'dicc_products_price': dicc_products_price,
        }

class ReporteEtiquetaUnica (models.AbstractModel):
    _name='report.imporgesa.label_code_lines_view'
    _description='Creado para solo una etiqueta por linea'

    def creacion_datos(self, orders):
        dicc_products_lines={}
        for order in orders:
            for linea in order.order_line:
                if linea.product_id.default_code not in dicc_products_lines:
                    dicc_products_lines[linea.product_id.default_code]=[]

                if linea.product_id.default_code in dicc_products_lines:
                    dicc_products_lines[linea.product_id.default_code].append({
                    'code': linea.product_id.default_code,
                    'qty_done': linea.product_uom_qty,
                    'uom_id': linea.product_id.uom_id.name,
                    'description': linea.product_id.name,
                    'barcode': linea.product_id.barcode,
                    })
        return dicc_products_lines

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['sale.order'].browse(docids)
        dicc_products_lines = self.creacion_datos(docs)
        return {
            'doc_ids': docids,
            'doc_model': 'sale.order',
            'docs': docs,
            'dicc_products_lines': dicc_products_lines,
        }
