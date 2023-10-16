import json
from odoo import http
from odoo.http import request

class MyController(http.Controller):
    @http.route('/webhook', type='json', auth='public', csrf=False)
    def custom_route_handler(self, content, type):
        if type in ["RESERVATION_CREATED", "RESERVATION_CHANGE"]:
            # Decodifica il contenuto JSON
            data = json.loads(content)
            refer = data.get('refer', '')
            checkin = data.get('checkin', '')
            checkout = data.get('checkout', '')
            totalGuest = data.get('totalGuest', 0)
            totalChildren = data.get('totalChildren', 0)
            totalInfants = data.get('totalInfants', 0)
            rooms = data.get('rooms', 0)
            roomGross = data.get('roomGross', 0)
            familyName = data.get('guests', [{}])[0].get('familyName', '')
            guestsList = data.get('guestsList', '')

            # Trova la fattura esistente in base al campo "refer"
            account_move = request.env['account.move'].search([('refer', '=', refer)])

            if account_move:
                # Aggiorna i campi desiderati della fattura e imposta lo stato in "Draft"
                account_move.write({
                    'partner_id': guestsList,
                    'refer': refer,
                    'checkin': checkin,
                    'checkout': checkout,
                    'totalGuest': totalGuest,
                    'totalChildren': totalChildren,
                    'totalInfants': totalInfants,
                    'rooms': rooms,
                    'roomGross': roomGross,
                    'state': 'draft'  # Imposta lo stato in "Draft"
                })

                # Restituisci una risposta JSON o un messaggio di conferma
                return {'message': f'Aggiornamento della fattura con refer {refer} effettuato con successo in stato "Draft"'}
            else:
                return {'message': f'Fattura con refer {refer} non trovata'}
        else:
            return {'message': 'Tipo di webhook non supportato'}

        if type in ["RESERVATION_CONFIRM", "RESERVATION_CANCELLED"]:
            # Decodifica il contenuto JSON
            data = json.loads(content)
            refer = data['refer']

            # Trova la fattura esistente in base al campo "refer"
            account_move = request.env['account.move'].search([('refer', '=', refer)])

            if account_move:
                # Aggiorna lo stato della fattura
                account_move.write({'state': 'posted' if type == "RESERVATION_CONFIRM" else 'cancel'})

                # Restituisci una risposta JSON o un messaggio di conferma
                return {'message': f'Fattura con refer {refer} aggiornata con successo a stato {type}'}
            else:
                return {'message': f'Fattura con refer {refer} non trovata'}
        else:
            return {'message': 'Tipo di webhook non supportato'}