# Add this to your partner model (res.partner)
from odoo import fields, models

class ResPartner(models.Model):
    _inherit = 'res.partner'

    vendor_bills = fields.One2many(
        'account.move',
        'partner_id',
        string='Vendor Bills',
        domain="[('move_type', 'in', ['in_invoice', 'in_refund']), ('state', '=', 'posted')]"
    )

    vendor_payments = fields.One2many(
        'account.payment',
        'partner_id',
        string='Vendor Payments',
        domain=[('payment_type', '=', 'outbound')]  # Payments to the supplier
    )