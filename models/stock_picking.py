# -*- coding: utf-8 -*-


from odoo import SUPERUSER_ID, _, api, fields, models
import logging


class Picking(models.Model):
    _inherit = "stock.picking"
    
    total_pedido = fields.Float('Total pedido')