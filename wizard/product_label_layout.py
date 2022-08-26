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
                logging.warning(linea.qty_done)
                for i in range(int(linea.qty_done)):
                    llave = str(i) + str(linea.product_id.default_code)
                    if llave not in dicc_productos_price:
                        dicc_productos_price[llave] = {
                        'codigo':linea.product_id.default_code,
                        'descripcion': linea.product_id.name,
                        'precio':linea.product_id.list_price,
                        'codigo_barras': linea.product_id.barcode
                        }
                logging.warning(linea.product_id.default_code)
                logging.warning(linea.product_id.name)
                logging.warning(linea.product_id.list_price)
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

        data['dicc_productos_price']=dicc_productos_price
        data['dicc_products']=dicc_products
        return xml_id, data
