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
    ('code', '3 x 2')
    ], ondelete={'code_price': 'set default', 'code': 'set default'})

    def _prepare_report_data(self):
        xml_id, data = super()._prepare_report_data()

        dicc_productos_price = {}
        dicc_products = {}

        if self.print_format == 'code_price':
            xml_id = 'imporgesa.report_label_code_price'

            for linea in self.move_line_ids:

                for i in range(int(linea.qty_done)):
                    llave = str(i) + str(linea.product_id.default_code)
                    if llave not in dicc_productos_price:
                        dicc_productos_price[llave] = {
                        'codigo':linea.product_id.default_code,
                        'descripcion': linea.product_id.name,
                        'precio':linea.product_id.list_price,
                        'codigo_barras': linea.product_id.barcode
                        }


            if self.product_ids:

                for i in range(self.custom_quantity):
                    logging.warning('new i '+str(i))
                    logging.warning(self.product_ids.name)
                    llave = str(i) + str(self.product_ids.default_code)
                    if llave not in dicc_productos_price:
                        dicc_productos_price[llave] = {
                        'codigo':self.product_ids.default_code,
                        'descripcion': self.product_ids.name,
                        'precio':self.product_ids.list_price,
                        'codigo_barras': self.product_ids.barcode
                        }
            if self.product_tmpl_ids:
                for i in range(self.custom_quantity):
                    logging.warning('new i '+str(i))
                    logging.warning(self.product_tmpl_ids.name)
                    llave = str(i) + str(self.product_tmpl_ids.default_code)
                    if llave not in dicc_productos_price:
                        dicc_productos_price[llave] = {
                        'codigo':self.product_tmpl_ids.default_code,
                        'descripcion': self.product_tmpl_ids.name,
                        'precio':self.product_tmpl_ids.list_price,
                        'codigo_barras': self.product_tmpl_ids.barcode
                        }
            logging.warning(dicc_productos_price)

        if self.print_format == 'code':
            xml_id = 'imporgesa.report_label_code'

            for linea in self.move_line_ids:
                for i in range(int(linea.qty_done)):
                    llave = str(i) + str(linea.product_id.default_code)
                    if llave not in dicc_productos_price:
                        dicc_products[llave] = {
                        'codigo':linea.product_id.default_code,
                        'descripcion': linea.product_id.name,
                        'codigo_barras': linea.product_id.barcode
                        }
            if self.product_ids:
                for i in range(self.custom_quantity):
                    # logging.warning('new i '+str(i))
                    # logging.warning(self.product_ids.name)
                    llave = str(i) + str(self.product_ids.default_code)
                    if llave not in dicc_productos_price:
                        dicc_products[llave] = {
                        'codigo':self.product_ids.default_code,
                        'descripcion': self.product_ids.name,
                        'codigo_barras': self.product_ids.barcode
                        }
            if self.product_tmpl_ids:
                for i in range(self.custom_quantity):
                    # logging.warning('new i '+str(i))
                    # logging.warning(self.product_ids.name)
                    llave = str(i) + str(self.product_tmpl_ids.default_code)
                    if llave not in dicc_productos_price:
                        dicc_products[llave] = {
                        'codigo':self.product_tmpl_ids.default_code,
                        'descripcion': self.product_tmpl_ids.name,
                        'codigo_barras': self.product_tmpl_ids.barcode
                        }

        data['dicc_productos_price']=dicc_productos_price
        data['dicc_products']=dicc_products
        return xml_id, data
