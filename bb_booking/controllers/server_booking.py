# from flask import Flask, request, jsonify
# from api_key import get_access_token, get_access_token2, fetch_accommodations, fetch_reservations_for_accommodation_id, fetch_webhooks
#
# app = Flask(__name__)
#
#
# # Dizionario per tenere traccia delle prenotazioni per ciascun accommodation
# accommodation_reservations = {}
#
# @app.route('/webhook', methods=['POST'])
# def webhook():
#     data = request.json  # Ricevi la notifica inviata da Octorate tramite webhook
#     event_type = data.get("event_type")
#     accommodation_id = data.get("accommodation_id")
#     new_reservation = data.get("reservation")
#
#     if event_type in ["RESERVATION_CREATED", "RESERVATION_CHANGE", "RESERVATION_CANCELLED", "RESERVATION_CONFIRMED"]:
#         if accommodation_id in accommodation_reservations:
#             accommodation_reservations[accommodation_id].append(new_reservation)
#         else:
#             accommodation_reservations[accommodation_id] = [new_reservation]
#
#         # Ora puoi chiamare una funzione da api_key.py per ulteriori azioni (ad esempio, salvare i dati nel database)
#         access_token = get_access_token()  # Esempio di chiamata a una funzione di api_key.py
#         if access_token:
#             accommodations = fetch_accommodations(access_token)
#             # Esegui ulteriori azioni con i dati ottenuti
#         else:
#             print("Errore nell'ottenere il token di accesso da api_key.py")
#
#     return "OK", 200
#
# @app.route('/get_reservations/<accommodation_id>', methods=['GET'])
# def get_reservations(accommodation_id):
#     if accommodation_id in accommodation_reservations:
#         reservations = accommodation_reservations[accommodation_id]
#
#         # Ora puoi chiamare una funzione da api_key.py per ottenere ulteriori dati sulle prenotazioni
#         access_token_a = get_access_token2()  # Esempio di chiamata a una funzione di api_key.py
#         if access_token_a:
#             reservations_data = fetch_reservations_for_accommodation_id(access_token_a, accommodation_id)
#             # Esegui ulteriori azioni con i dati ottenuti
#         else:
#             print("Errore nell'ottenere il token per le prenotazioni da api_key.py")
#
#         return jsonify(reservations)
#     else:
#         return "Accommodation non trovato", 404
#
#
#
#
#
# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=80)
