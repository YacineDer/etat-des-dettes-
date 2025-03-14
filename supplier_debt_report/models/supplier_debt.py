from odoo import fields, models

class SupplierDebtReport(models.Model):
    _name = 'supplier.debt.report'
    _description = 'Supplier Debt Report'
    _auto = False  # SQL-based model (view)
    _rec_name = 'partner_id'

    partner_id = fields.Many2one('res.partner', string='Supplier', readonly=True)
    total_invoice = fields.Monetary(string='Total Invoice', readonly=True, currency_field='currency_id')
    total_paid = fields.Monetary(string='Total Paid', readonly=True, currency_field='currency_id')
    total_due = fields.Monetary(string='Amount Due', readonly=True, currency_field='currency_id')
    currency_id = fields.Many2one('res.currency', string='Currency', readonly=True)
    doc_state = fields.Selection([
        ('draft', 'Draft'),
        ('posted', 'Posted'),
        ('cancel', 'Cancelled')
    ], string='Document Status', readonly=True)

    payment_status = fields.Selection([
        ('not_paid', 'Not Paid'),
        ('in_payment', 'In Payment'),
        ('paid', 'Paid'),
        ('partial', 'Partially Paid'),
        ('reversed', 'Reversed')
    ], string='Payment Status', readonly=True)

    bill_lines = fields.One2many('account.move', 'partner_id', string='Bills', compute='_compute_bills')
    payment_lines = fields.One2many('account.payment', 'partner_id', string='Payments', compute='_compute_payments')

    def _compute_bills(self):
        for record in self:
            record.bill_lines = self.env['account.move'].search([
                ('partner_id', '=', record.partner_id.id),
                ('move_type', 'in', ['in_invoice', 'in_refund']),
                ('state', '=', 'posted')
            ]).ids

    def _compute_payments(self):
        for record in self:
            record.payment_lines = self.env['account.payment'].search([
                ('partner_id', '=', record.partner_id.id),
                ('payment_type', '=', 'outbound')
            ]).ids

    def init(self):
        """ Initialize the SQL view """
        self.env.cr.execute("""
            DROP VIEW IF EXISTS supplier_debt_report;
            CREATE OR REPLACE VIEW supplier_debt_report AS (
                SELECT
                    ROW_NUMBER() OVER (ORDER BY am.partner_id) AS id,
                    am.partner_id AS partner_id,
                    SUM(am.amount_total) AS total_invoice,
                    SUM(am.amount_total - am.amount_residual) AS total_paid,
                    SUM(am.amount_residual) AS total_due,
                    am.currency_id AS currency_id,
                    am.state AS doc_state,
                    am.payment_state AS payment_status
                FROM account_move am
                WHERE am.move_type IN ('in_invoice', 'in_refund')
                  AND am.state = 'posted'
                GROUP BY am.partner_id, am.currency_id, am.state, am.payment_state
            )
        """)
