# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools, _

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    margen_venta = fields.Float('Margen de venta',config_parameter='sale.margen_venta')
