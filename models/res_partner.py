# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools, _


class ResPartner(models.Model):
    _inherit = "res.partner"

    # giro_negocio = fields.Selection([('publico_final', 'Publico final'),('muebleria', 'Mueblería'), ('corporativo', 'Corporativo'), ('educacion', 'Educación'),
    # ('gobierno', 'Gobierno'), ('eventos', 'Eventos'), ('distribuidora', 'Distribuidora'), ('retaurante', 'Restaurante'), ('iglesia', 'Iglesia'), ('hoteleria', 'Hotelería'),
    # ('vendedor_detalle', 'Vendedor al detalle')],string ="Giro de negocio")
    vendedor = fields.Boolean(default=False, string="Vendedor")

    @api.model
    def _get_default_company(self):
        return self.env.company.id

    giro_negocio_id = fields.Many2one('imporgesa.giro_negocio','giro de negocio')
    company_id = fields.Many2one(default=_get_default_company)

    @api.model_create_multi
    def create(self, vals_list):
        res = super(ResPartner, self).create(vals_list)
        if res.customer_rank > 0:
            res.user_id = self.env.user.id
        return res
