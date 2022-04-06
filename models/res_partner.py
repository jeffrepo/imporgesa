# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools, _


class ProductTemplate(models.Model):
    _inherit = "res.partner"

    giro__negocio = fields.Selection([('1', 'Publico final'),('2', 'Mueblería'), ('3', 'Corporativo'), ('4', 'Educación'),
    ('5', 'Gobierno'), ('6', 'Eventos'), ('7', 'Distribuidora'), ('8', 'Restaurante'), ('9', 'Iglesia'), ('10', 'Hotelería'),
    ('11', 'Vendedor al detalle')])
