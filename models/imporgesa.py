# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools, _


class ImporgesaGiroNegocio(models.Model):
    _name = "imporgesa.giro_negocio"

    name = fields.Char('Nombre')
