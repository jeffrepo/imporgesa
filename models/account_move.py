from odoo import api, fields, models, tools, _

class AccountMove(models.Model):
    _inherit = 'account.move'

    # vendedor_id = fields.Many2one('res.partner', 'Vendedor')
    descripcion = fields.Char('Descripción')

    def _create_payment_vals_from_wizard(self):
        vals = super()._create_payment_vals_from_wizard()
        if self.descripcion:
            vals.update({'descripcion': self.descripcion})
        
        return vals
