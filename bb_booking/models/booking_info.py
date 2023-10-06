from odoo import models, fields, api

class roombooking(models.Model):
    _inherit = "account.move"

    refer = fields.Char(string='ID Prenotazione')
    checkin = fields.Date(string='Data di Check-in')
    checkout = fields.Date(string='Data di Check-out')
    totalGuest = fields.Integer(string='Ospiti Totali')
    totalChildren = fields.Integer(string='Totali Ragazzi')
    totalInfants = fields.Integer(string='Totali Neonati')
    soggiorno_input = fields.Html(string='Soggiorno', compute='_compute_soggiorno_input', sanitize=False, store=False)
    rooms = fields.Float(string='Numero stanza')
    roomGross = fields.Float(string='Costo stanza')

    @api.depends('checkin', 'checkout', 'totalGuest')
    def _compute_soggiorno_input(self):
        for record in self:
            if record.checkin and record.checkout:
                # Imposta l'orario di check-in e check-out a mezzanotte
                checkin_date = fields.Date.from_string(record.checkin)
                checkout_date = fields.Date.from_string(record.checkout)
                delta = checkout_date - checkin_date
                num_notti = delta.days
                num_ospiti = record.totalGuest
                record.soggiorno_input = 2 * num_notti * num_ospiti

class prenotadettagli(models.Model):
    _inherit = "account.move.line"

    product_id = fields.Many2one('product.product', string="Nome stanza")
    quantity = fields.Float(string="Numero notti")
    move_id = fields.Many2one('account.move', string='Fattura')

    @api.onchange('product_id')
    def _onchange_product_id(self):
        for record in self:
            if record.product_id and record.product_id.name == "Tassa soggiorno":
                # Trova l'oggetto account.move associato alla riga di fattura
                invoice = record.move_id  # Supponendo che il campo 'move_id' collega la riga di fattura alla fattura
                if invoice:
                    # Ora puoi accedere agli attributi come 'checkin' e 'checkout' dalla fattura
                    # Imposta l'orario di check-in e check-out a mezzanotte
                    checkin_date = fields.Date.from_string(invoice.checkin)
                    checkout_date = fields.Date.from_string(invoice.checkout)
                    delta = checkout_date - checkin_date
                    num_notti = delta.days
                    num_ospiti = invoice.totalGuest
                    record.quantity = num_notti * num_ospiti

    name = fields.Char(string="Descrizione")
    #price_unit = fields.Float(string="Prezzo unitario")

    @api.onchange('product_id')
    def _onchange_product_id(self):
        for record in self:
            if record.product_id and record.product_id.name == "PERNOTTO":
                # Trova l'oggetto account.move associato alla riga di fattura
                invoice = record.move_id  # Supponendo che il campo 'move_id' collega la riga di fattura alla fattura
                if invoice:
                    # Calcola i valori dei campi name, quantity e price_unit
                    name = f"Prenotazione {invoice.refer} dal {invoice.checkin} al {invoice.checkout}"
                    quantity = invoice.rooms  # Assumi che rooms sia il numero di stanze
                    price_unit = invoice.roomGross  # Assumi che roomGross sia il costo della stanza
                    # Imposta i valori nei campi corrispondenti
                    record.name = name
                    record.quantity = quantity
                    record.price_unit = price_unit