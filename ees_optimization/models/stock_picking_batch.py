# -*- coding: utf-8 -*-

from odoo.exceptions import UserError
from odoo import models, fields, _


class StockPickingBatch(models.Model):
    _inherit = 'stock.picking.batch'

    carrier_id = fields.Many2one('delivery.carrier', string='Carrier')

    def action_confirm(self):
        self.ensure_one()
        if not self.picking_ids:
            raise UserError(_("You have to set some pickings to batch."))
        self.picking_ids.sudo().write({'carrier_id': self.carrier_id.id})
        return super(StockPickingBatch, self).action_confirm()
