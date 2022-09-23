# -*- coding: utf-8 -*-

from collections import defaultdict
from odoo.tools import float_is_zero
from odoo import api, models, _
from odoo.exceptions import ValidationError


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    def _product_domain(self, product_variant_ids):
        return [('product_id', 'in', product_variant_ids)]

    def _move_domain(self, product_variant_ids, wh_location_ids):
        move_domain = self._product_domain(product_variant_ids)
        move_domain += [('product_uom_qty', '!=', 0)]
        out_domain = move_domain + [
            '&',
            ('location_id', 'in', wh_location_ids),
            ('location_dest_id', 'not in', wh_location_ids),
        ]
        in_domain = move_domain + [
            '&',
            ('location_id', 'not in', wh_location_ids),
            ('location_dest_id', 'in', wh_location_ids),
        ]
        return in_domain, out_domain

    def _move_confirmed_domain(self, product_variant_ids, wh_location_ids):
        in_domain, out_domain = self._move_domain(product_variant_ids, wh_location_ids)
        out_domain += [('state', 'not in', ['draft', 'cancel', 'done'])]
        in_domain += [('state', 'not in', ['draft', 'cancel', 'done'])]
        return in_domain, out_domain

    def _get_free_stock_qty(self):
        product_variant_ids = self.product_id.ids
        warehouse = self.warehouse_id

        wh_location_ids = [loc['id'] for loc in self.env['stock.location'].search_read(
            [('id', 'child_of', warehouse.view_location_id.id), ('reservation_location', '=', True)],
            ['id'],
        )]
        in_domain, out_domain = self._move_confirmed_domain(
            product_variant_ids,
            wh_location_ids
        )
        outs = self.env['stock.move'].search(out_domain, order='reservation_date, priority desc, date, id')
        reserved_outs = self.env['stock.move'].search(
            out_domain + [('state', 'in', ('partially_available', 'assigned'))],
            order='priority desc, date, id')
        outs_per_product = defaultdict(list)
        reserved_outs_per_product = defaultdict(list)
        for out in outs:
            outs_per_product[out.product_id.id].append(out)
        for out in reserved_outs:
            reserved_outs_per_product[out.product_id.id].append(out)
        ins = self.env['stock.move'].search(in_domain, order='priority desc, date, id')
        ins_per_product = defaultdict(list)
        for in_ in ins:
            ins_per_product[in_.product_id.id].append({
                'qty': in_.product_qty,
                'move': in_,
                'move_dests': in_._rollup_move_dests(set())
            })
        currents = outs.product_id._get_only_qty_available()
        free_stock = 0.0
        for product in (ins | outs).product_id:
            product_rounding = product.uom_id.rounding
            for out in reserved_outs_per_product[product.id]:
                reserved = out.product_uom._compute_quantity(out.reserved_availability, product.uom_id)
                currents[product.id] -= reserved

            for out in outs_per_product[product.id]:
                reserved = 0.0
                if out.state in ('partially_available', 'assigned'):
                    reserved = out.product_uom._compute_quantity(out.reserved_availability, product.uom_id)
                demand = out.product_qty - reserved

                if float_is_zero(demand, precision_rounding=product_rounding):
                    continue
                current = currents[product.id]
                taken_from_stock = min(demand, current)
                if not float_is_zero(taken_from_stock, precision_rounding=product_rounding):
                    currents[product.id] -= taken_from_stock

            free_stock = currents.get(product.id, 0)
        return free_stock

    def write(self, values):
        result = super(SaleOrderLine, self).write(values)
        for rec in self:
            if self.user_has_groups('sales_team.group_sale_salesman'):
                free_qty_available = rec._get_free_stock_qty() or rec.product_id.with_context(
                        warehouse=rec.warehouse_id.ids, is_from_product_reservation=True).virtual_available
                if rec.product_uom_qty > free_qty_available:
                    rec.product_uom_qty = 0.0
                    raise ValidationError(_("The available quantity for this product is : {}".format(free_qty_available)))
        return result
