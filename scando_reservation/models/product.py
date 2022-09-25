# -*- coding: utf-8 -*-

from odoo import models


class Product(models.Model):
    _inherit = 'product.product'

    def _get_domain_locations(self):
        domain_quant_loc, domain_move_in_loc, domain_move_out_loc = super(Product, self)._get_domain_locations()
        if self._context.get("is_from_product_reservation"):
            domain_quant_loc += [('location_id.reservation_location', '=', True)]
            domain_move_in_loc += [('location_id.reservation_location', '=', True)]
            domain_move_out_loc += [('location_id.reservation_location', '=', True)]
        return (domain_quant_loc , domain_move_in_loc , domain_move_out_loc)
