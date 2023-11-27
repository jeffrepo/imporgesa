# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools, _


class ProductTemplate(models.Model):
    _inherit = "product.template"

    marca = fields.Char('Marca')
    descripcion_producto = fields.Text('Descripcion')
    link_web = fields.Char('',default="www.goodtime.com.gt")
