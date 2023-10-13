from odoo import http
from odoo.http import request

class MyController(http.Controller):
    @http.route('/webhook', type='json', auth='public', csrf=False)

    def custom_route_handler(self, refer, checkin, checkout, totalGuest, totalChildren, totalInfants, rooms, roomGross):
        # Esempio di manipolazione dei dati ricevuti dalla route personalizzata
        # Esegui le operazioni necessarie con i dati ricevuti

        # Esempio di creazione di un record nel modello "roombooking" con i dati ricevuti
        roombooking = request.env['account.move']
        new_booking = roombooking.create({
            'refer': refer,
            'checkin': checkin,
            'checkout': checkout,
            'totalGuest': totalGuest,
            'totalChildren': totalChildren,
            'totalInfants': totalInfants,
            'rooms': rooms,
            'roomGross': roomGross,
            # Altri campi necessari nel tuo modello "roombooking"
        })

        # Restituisci una risposta JSON o un messaggio di conferma
        return {'message': 'Dati della prenotazione creati con successo'}

