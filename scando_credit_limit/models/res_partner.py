# -*- coding: utf-8 -*-

from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    credit_limit = fields.Float(string="Customer Credit Limit")
    threshold = fields.Float(string="Threshold Amount")