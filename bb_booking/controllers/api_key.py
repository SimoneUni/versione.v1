import requests
import json

from odoo import http
from odoo.http import request, _logger

# Dati del client per ottenere il token
CLIENT_ID = "public_a3a3b3c2278b4deabd9108e74c5e8af2"
CLIENT_SECRET = "secret_47ff49e5533047a994869a012a94eecfTOIUDRGXYK"


# Funzione per ottenere il token di accesso
def get_access_token():
    endpoint = "https://api.octorate.com/connect/rest/v1/identity/apilogin"

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    payload = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    }

    response = requests.post(endpoint, data=payload, headers=headers)
    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        print(f"Errore nell'ottenere il token di accesso: {response.status_code} - {response.text}")
        return None


# Ottieni il token di accesso
access_token = get_access_token()
if access_token:
    print(f"Token di accesso ottenuto con successo: {access_token}")
else:
    print("Errore nell'ottenere il token di accesso.")


def get_access_token2():
    endpoint = "https://api.octorate.com/connect/rest/v1/identity/token"

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    payload = {
        "grant_type": "authorization_code",
        "code": "d1703baf4ce84119aae1fb57d230eb13521e944bd1f445b69459d97d84b9692f",
        "client_id": CLIENT_ID,  # Assicurati di aver definito CLIENT_ID
        "client_secret": CLIENT_SECRET,  # Assicurati di aver definito CLIENT_SECRET
        "redirect_uri": "https://api.octorate.com/connect/docs/oauth2-redirect.html"
    }

    response = requests.post(endpoint, data=payload, headers=headers)

    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        print(f"Errore nell'ottenere il token di accesso: {response.status_code} - {response.text}")
        return None


# Ottieni il token di accesso
access_token_a = get_access_token2()

if access_token_a:
    print(f"Token per visionare le reservation è : {access_token_a}")
else:
    print("Errore nell'ottenere il token di accesso.")


# def refresh_token():
#    endpoint = "https://api.octorate.com/connect/rest/v1/identity/refresh"

#    headers = {
#        "Accept": "application/json",
#        "Content-Type": "application/x-www-form-urlencoded"
#    }

#    payload = {
# "grant_type": "authorization_code",
# "code": "073ce7c8790c493bbeba060c5a7b011d564daffb291a4bf78c79da56ed8144d1",
#        "client_id": CLIENT_ID,  # Assicurati di aver definito CLIENT_ID
#        "client_secret": CLIENT_SECRET,  # Assicurati di aver definito CLIENT_SECRET
# "redirect_uri": "https://api.octorate.com/connect/docs/oauth2-redirect.html"
#        'refresh_token': '2acf003360ea4ebca6871b5d7e56efe2'
#    }

#    response = requests.post(endpoint, data=payload, headers=headers)

#    if response.status_code == 200:
#        print("refresh avvenuto con successo")
#        return response.json().get("access_token")
#    else:
#        print(f"Errore nell'ottenere il token di accesso: {response.status_code} - {response.text}")
#        return None


def fetch_accommodations(token):
    endpoint = "https://api.octorate.com/connect/rest/v1/accommodation"
    # print(token)

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(endpoint, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Errore nell'ottenere gli accommodation: {response.headers}, {headers}")
        return []


# Esempio di utilizzo:
# Ottieni il token di accesso (già ottenuto precedentemente)
access_token = get_access_token()
# Ottenere gli accommodation
accommodations = fetch_accommodations(access_token)
if accommodations:
    print(f"Gli accommodation ottenuti con successo: {accommodations}")
else:
    print("Nessun accommodation disponibile o errore nell'ottenimento.")


def fetch_reservations_for_accommodation_id(access_token_a, accommodation_id):
    reservation_endpoint = f"https://api.octorate.com/connect/rest/v1/reservation/{accommodation_id}"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {access_token_a}"
    }
    response = requests.get(reservation_endpoint, headers=headers)

    if response.status_code == 200:
        reservations = response.json()
        return reservations
    else:
        print(
            f"Errore nell'ottenere le prime prenotazioni per l'alloggio {accommodation_id}, {headers}, {response.status_code}, {response.text}")
        return []


# Esempio di utilizzo:
# Ottieni il token di accesso (già ottenuto precedentemente)

# access_token_a = get_access_token2()
# print(access_token_a)
# Inserisci l'ID dell'alloggio per cui desideri ottenere le prenotazioni
accommodation_id = "557782"

# Ottieni le prenotazioni per l'alloggio selezionato utilizzando il token ottenuto
reservations = fetch_reservations_for_accommodation_id(access_token_a, accommodation_id)

# Controlla se ci sono prenotazioni
if reservations:
    print(f"{accommodation_id}: {reservations}")

    # Converti le prenotazioni in formato JSON
    reservations_json = json.dumps(reservations)

    # Definisci l'URL del webhook al quale inviare le prenotazioni
    webhook_url = "https://webhook.site/7562c12d-e21c-402c-8faa-b6c08e9e564d"

    # Invia i dati al webhook
    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(webhook_url, data=reservations_json, headers=headers)

    # Verifica la risposta del webhook
    if response.status_code == 200:
        print("Dati inviati con successo al webhook.")
    else:
        print(f"Errore nell'invio dei dati al webhook: {response.status_code} - {response.text}")
else:
    print("Nessuna prenotazione disponibile o errore nell'ottenimento.")

print(f"{accommodation_id}:{reservations}")


def fetch_webhooks(access_token_a):
    endpoint = "https://api.octorate.com/connect/rest/v1/subscription"

    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {access_token_a}"
    }

    response = requests.get(endpoint, headers=headers)
    if response.status_code != 200:
        print(f"Errore nell'ottenere i webhooks configurati: {response.status_code} - {response.text} - {headers}")
        return []

    return response.json()


webhook_url = "https://webhook.site/7562c12d-e21c-402c-8faa-b6c08e9e564d"

# Ottieni i webhooks configurati
# Assicurati di avere un access token valido
webhooks = fetch_webhooks(access_token_a)

# Invia i dati al webhook
for webhook_data in webhooks:
    response = requests.post(webhook_url, json=webhook_data)
    if response.status_code == 200:
        print(f"Dati inviati con successo al webhook: {webhook_url}")
    else:
        print(f"Errore nell'invio dei dati al webhook: {response.status_code} - {response.text}")




