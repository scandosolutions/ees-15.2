# -*- coding: utf-8 -*-

from odoo.exceptions import ValidationError
from odoo import models, api, _


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_confirm(self):
        for order in self:
            if order.amount_total > order.partner_id.threshold:
                raise ValidationError(_("Total order amount should be less than %s" %(order.partner_id.threshold)))
        res = super(SaleOrder, self).action_confirm()
        return res