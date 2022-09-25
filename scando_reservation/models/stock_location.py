# -*- coding: utf-8 -*-

from odoo import models, fields


class StockLocation(models.Model):
    _inherit = 'stock.location'

    reservation_location = fields.Boolean(
        string="Is a Reservation Location?",
        help="Check this box to allow using this location as Reservation Location"
    )