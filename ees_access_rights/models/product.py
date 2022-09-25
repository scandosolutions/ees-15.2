# -*- coding: utf-8 -*-

from odoo.exceptions import UserError
from odoo import models, api, _


class Product(models.Model):
    _inherit = 'product.product'

    @api.model
    def create(self, vals):
        if self.user_has_groups('base.group_erp_manager') or not self.user_has_groups('ees_access_rights.group_product_creation'):
            raise UserError(_("You are not allowed to create Product"))
        res = super(Product, self).create(vals)
        return res
