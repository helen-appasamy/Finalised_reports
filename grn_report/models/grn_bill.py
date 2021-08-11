# -*- coding: utf-8 -*-

from odoo import api, tools, fields, models

class BillGRNReport(models.Model):
    _name = "bill.grn.report"
    _auto = False
    _description = "Receipts with Bill"

    state = fields.Selection([
        ('purchase', 'Purchase Order'),
        ('done', 'Locked'),
    ], string='Status')
    company_id = fields.Many2one('res.company',string='Company', readonly=1)
    partner_id = fields.Many2one('res.partner',string='Vendor', readonly=1)
    purchase_order_id = fields.Many2one('purchase.order',string='PO Number', readonly=1)
    date_approve = fields.Date(string="Confirmed Date", readonly=1)
    product_id = fields.Many2one('product.product',string='Product', readonly=1)
    product_uom_qty = fields.Float(string='Ordered Qty', readonly=1)
    reference = fields.Char(string='Transfer Number', readonly=1)
    product_qty = fields.Float(string='Done Qty', readonly=1)
    move_id = fields.Many2one('account.move',string='Bill/Debit Number', readonly=1)
    quantity = fields.Float(string='Billed Qty', readonly=1)


    def _select(self):
        return """
            SELECT
                    row_number() over() as id,
                    po.state,
                    po.company_id,
                    po.partner_id,
                    po.id as purchase_order_id,
                    po.date_approve,
                    order_line.product_id,
                    order_line.product_uom_qty,
                    stocks.reference,
                    stocks.product_qty,
                    account_line.move_id,
                    account_line.quantity
        """
    def _from(self):
        return """
            FROM purchase_order as po
        """

    def _join(self):
        return """
            LEFT JOIN purchase_order_line as order_line ON po.id=order_line.order_id
            LEFT JOIN stock_move as stocks ON order_line.id=stocks.purchase_line_id
            LEFT JOIN account_move_line as account_line ON stocks.invoice_line_id=account_line.id
        """

    def _where(self):
        return """
            WHERE stocks.state = 'done'
        """

    def _group_by(self):
        return """
            GROUP BY              
                po.state,
                po.company_id,
                po.partner_id,
                po.id,
                po.date_approve,
                order_line.product_id,
                order_line.product_uom_qty,
                stocks.reference,
                stocks.product_qty,
                account_line.move_id,
                account_line.quantity
        """

    def init(self):
        tools.drop_view_if_exists(self._cr, self._table)
        self._cr.execute("""
            CREATE OR REPLACE VIEW %s AS (
                %s
                %s
                %s
                %s
                %s
            ) """ % (self._table, self._select(), self._from(), self._join(), self._where(), self._group_by())
            )
