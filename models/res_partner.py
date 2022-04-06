# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools, _


class ProductTemplate(models.Model):
    _inherit = "res.partner"

    giro_negocio = fields.Selection([('publico_final', 'Publico final'),('muebleria', 'Mueblería'), ('corporativo', 'Corporativo'), ('educacion', 'Educación'),
    ('gobierno', 'Gobierno'), ('eventos', 'Eventos'), ('distribuidora', 'Distribuidora'), ('retaurante', 'Restaurante'), ('iglesia', 'Iglesia'), ('hoteleria', 'Hotelería'),
    ('vendedor_detalle', 'Vendedor al detalle')])
