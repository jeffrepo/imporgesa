# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from collections import defaultdict
from odoo import fields, models
import logging


class ProductLabelLayout(models.TransientModel):
    _inherit = 'product.label.layout'
    _description = 'Agregando nuevas opciones '

    print_format = fields.Selection(selection_add=[
    ('code_price', '3 x 2 con precio'),
    ('code', '3 x 2'),
    ('code_line', '3 x 2 linea')
    ], ondelete={'code_price': 'set default', 'code': 'set default', 'code_line': 'set default'})

    def _prepare_report_data(self):
        xml_id, data = super()._prepare_report_data()

        dicc_products_price = {}
        dicc_products = {}
        dicc_products_lines = {}

        if self.print_format == 'code_price':
            xml_id = 'imporgesa.report_label_code_price'
            if self.move_line_ids:
                for linea in self.move_line_ids:
                    logging.warning('1 with price')
                    if linea.product_id.id not in dicc_products_price:
                        dicc_products_price[linea.product_id.id]=[]
                    for i in range(int(linea.qty_done)):
                        # llave = str(i) + str(linea.product_id.default_code)
                        if linea.product_id.id in dicc_products_price:
                            dicc_products_price[linea.product_id.id].append({
                            'codigo':linea.product_id.default_code,
                            'descripcion': linea.product_id.name,
                            'precio':linea.product_id.list_price,
                            'codigo_barras': linea.product_id.barcode
                            })


            if self.product_ids and len(self.move_line_ids)==0:

                for i in range(self.custom_quantity):
                    logging.warning('2 with price')
                    logging.warning(self)
                    logging.warning(self.custom_quantity)
                    for product_code in self.product_ids:
                        # llave = str(i) + str(product_code.default_code)
                        if product_code.id not in dicc_products_price:
                            dicc_products_price[product_code.id] = []
                        logging.warning('')
                        logging.warning(product_code.id)
                        if product_code.id in dicc_products_price:
                            dicc_products_price[product_code.id].append({
                            'codigo':product_code.default_code,
                            'descripcion': product_code.name,
                            'precio':product_code.list_price,
                            'codigo_barras': product_code.barcode
                            })

            if self.product_tmpl_ids:
                for i in range(self.custom_quantity):
                    logging.warning('3 with price')

                    # llave = str(i) + str(self.product_tmpl_ids.default_code)
                    if self.product_tmpl_ids.default_code not in dicc_products_price:
                        dicc_products_price[self.product_tmpl_ids.default_code] = []

                    if self.product_tmpl_ids.default_code in dicc_products_price:
                        dicc_products_price[self.product_tmpl_ids.default_code].append({
                        'codigo':self.product_tmpl_ids.default_code,
                        'descripcion': self.product_tmpl_ids.name,
                        'precio':self.product_tmpl_ids.list_price,
                        'codigo_barras': self.product_tmpl_ids.barcode
                        })

        if self.print_format == 'code':
            xml_id = 'imporgesa.report_label_code'
            if self.move_line_ids:
                for linea in self.move_line_ids:
                    logging.warning('1')
                    for i in range(int(linea.qty_done)):
                        # llave = str(i) + str(linea.product_id.default_code)
                        if linea.product_id.default_code not in dicc_products:
                            dicc_products[linea.product_id.default_code] =[]
                        if linea.product_id.default_code in dicc_products:
                            logging.warning('I: '+str(i))
                            dicc_products[linea.product_id.default_code].append({
                            'codigo':linea.product_id.default_code,
                            'descripcion': linea.product_id.name,
                            'codigo_barras': linea.product_id.barcode
                            })

            if self.product_ids and len(self.move_line_ids) == 0:
                for i in range(self.custom_quantity):
                    logging.warning('2')
                    for product_code in self.product_ids:
                        # llave = str(i) + str(product_code.default_code)
                        if product_code.default_code not in dicc_products:
                            dicc_products[product_code.default_code] = []

                        if product_code.default_code in dicc_products:
                            dicc_products[product_code.default_code].append(
                            {
                            'codigo':product_code.default_code,
                            'descripcion': product_code.name,
                            'codigo_barras': product_code.barcode
                            })


            if self.product_tmpl_ids:
                for i in range(self.custom_quantity):
                    logging.warning('3')
                    # llave = str(i) + str(self.product_tmpl_ids.default_code)
                    if self.product_tmpl_ids.default_code not in dicc_products:
                        dicc_products[self.product_tmpl_ids.default_code]=[]

                    if self.product_tmpl_ids.default_code in dicc_products:
                        dicc_products[self.product_tmpl_ids.default_code].append({
                        'codigo':self.product_tmpl_ids.default_code,
                        'descripcion': self.product_tmpl_ids.name,
                        'codigo_barras': self.product_tmpl_ids.barcode
                        })

        if self.print_format == 'code_line':
            xml_id = 'imporgesa.report_label_code_lines'
            logging.warning('1 code line')
            if self.move_line_ids:
                for linea in self.move_line_ids:
                    logging.warning(linea.product_id.name)
                    if linea.id not in dicc_products_lines:
                        dicc_products_lines[linea.id]=[]
                        dicc_products_lines[linea.id].append({
                        'code': linea.product_id.default_code,
                        'qty_done': linea.qty_done,
                        'uom_id': linea.product_id.uom_id.name,
                        'description': linea.product_id.name,
                        'barcode': linea.product_id.barcode,
                        })

        new_value = None
        if dicc_products_price:
            new_value = dicc_products_price.values()
        if dicc_products:
            new_value = dicc_products.values()

        nueva_list_precios = []
        if new_value:
            for n in new_value:
                nueva_list_precios.append(n)



        data['dicc_products_price']=nueva_list_precios
        data['dicc_products']=nueva_list_precios
        data['dicc_products_lines']=dicc_products_lines
        logging.warning('-----------Return')
        logging.warning(data['dicc_products_price'])
        logging.warning(data['dicc_products'])
        logging.warning(data['dicc_products_lines'])
        logging.warning(xml_id)

        return xml_id, data
