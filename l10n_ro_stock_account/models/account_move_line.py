# ©  2008-2018 Fekete Mihai <mihai.fekete@forbiom.eu>
#              Dorin Hongu <dhongu(@)gmail(.)com
# See README.rst file on addons root folder for license details

from odoo import _, api, fields, models
from odoo.exceptions import AccessError, UserError
from odoo.tools.float_utils import float_compare, float_is_zero


# all just adds a field in view;
class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    #    is_price_diffrence = fields.Boolean(help="When posting a invoice, tells if this line represent differences of price/quantity with the reception if exist will delete them, and recreate if necessary")
    # we are going to use  field is_anglo_saxon_line that exist and we do not need to unlink them ...

    # the relation from  stock_inventory   acc_move_line_ids = fields.One2many(  just to show in view
    stock_inventory_id = fields.Many2one(
        "stock.inventory",
        string="Stock Inventory",
        help="This account move line has been generated by this inventory. A field made just in this module just to show in inventory",
    )

    # MAyBE OK? NOT TO CHAGE IN INVOICE QTY OF RECIVEND PRODUCTS???
    # @api.onchange('quantity')
    # def _onchange_quantity(self):
    #     message = ''
    #     if self.move_id.type in ['in_refund', 'out_refund']:
    #         return
    #     if self.product_id and self.product_id.type == 'product':
    #
    #         if self.purchase_line_id:
    #             qty = 0
    #             for inv_line in self.purchase_line_id.invoice_lines:
    #                 if not isinstance(inv_line.id, models.NewId) and inv_line.move_id.state not in ['cancel']:
    #                     if inv_line.move_id.type == 'in_invoice':
    #                         qty += inv_line.uom_id._compute_quantity(inv_line.quantity,
    #                                                                  self.purchase_line_id.product_uom)
    #                     elif inv_line.move_id.type == 'in_refund':
    #                         qty -= inv_line.uom_id._compute_quantity(inv_line.quantity,
    #                                                                  self.purchase_line_id.product_uom)
    #
    #             qty_invoiced = qty
    #
    #             qty = self.purchase_line_id.qty_received - qty_invoiced
    #
    #             qty = self.purchase_line_id.product_uom._compute_quantity(qty, self.uom_id)
    #
    #             if qty < self.quantity:
    #                 raise UserError(
    #                     _('It is not allowed to record an invoice for a quantity bigger than %s') % str(qty))
    #         else:
    #             message = _('It is not indicated to change the quantity of a stored product!')
    #     if message:
    #         return {
    #             'warning': {'title': "Warning", 'message': message},
    #         }

    def _get_computed_account(self):
        # OVERRIDE to use the stock input account by default on vendor bills when dealing
        # with anglo-saxon accounting.
        self.ensure_one()
        ro_chart = self.env["ir.model.data"].get_object_reference(
            "l10n_ro", "ro_chart_template"
        )[1]
        payable_acc = self.company_id.property_stock_picking_payable_account_id.id
        if (
            self.product_id.type == "product"
            and self.move_id.company_id.anglo_saxon_accounting
            and self.move_id.is_purchase_document()
            and self.move_id.company_id.chart_template_id.id == ro_chart
        ):
            fiscal_position = self.move_id.fiscal_position_id
            accounts = self.product_id.product_tmpl_id.get_product_accounts(
                fiscal_pos=fiscal_position
            )
            purchase = self.move_id.purchase_id
            if self.product_id.purchase_method == "receive":
                # Control bills based on received quantities
                if self.product_id.type == "product":
                    if any([picking.notice for picking in purchase.picking_ids]):
                        # if exist at least one notice/aviz we are going to make
                        # at reception accounting lines with 408
                        # even if the invoice came the same day as reception;
                        # we are going to have a debit and a credit in account 408
                        # so is the same as making only accounting lines on
                        # invoice
                        return payable_acc
                    else:
                        return accounts["stock_valuation"]
            else:
                # Control bills based on ordered quantities
                if self.product_id.type == "product":
                    return accounts["stock_valuation"]
        return super(AccountMoveLine, self)._get_computed_account()