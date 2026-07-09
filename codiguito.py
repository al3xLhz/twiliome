
import time
import requests
from twilio.rest import Client
from twilio_config import *

def obtener_tasa_cambio(apikey: str) -> dict:
    """
    Obtiene las tasas de cambio actualizadas desde CurrencyFreaks API.
    """
    url = f"https://api.currencyfreaks.com/v2.0/rates/latest?apikey={apikey}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error al obtener tasas de cambio: {e}")
        return None

def generar_mensaje_cambio(api_key_cambio: str) -> str:
    """
    Genera el mensaje SMS solo con la tasa de cambio PEN a USD.
    """
    resultado_cambio = obtener_tasa_cambio(api_key_cambio)
    if resultado_cambio and 'rates' in resultado_cambio and 'PEN' in resultado_cambio['rates']:
        pen_usd = resultado_cambio['rates']['PEN']
        msg_cambio = f"1 USD = {pen_usd} PEN"
    else:
        msg_cambio = "(No se pudo obtener el tipo de cambio)"
    return msg_cambio

def enviar_sms(mensaje: str, to_number: str) -> None:
    """Envía un mensaje SMS usando Twilio."""
    time.sleep(2)  # Espera para evitar límites de rate
    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        message = client.messages.create(
            from_='whatsapp:+14155238886',
            body=mensaje,
            to=f'whatsapp:{to_number}'
        )
        print('Mensaje Enviado:', message.sid)
    except Exception as e:
        print(f"Error al enviar el mensaje: {e}")

def main():
    DESTINATARIO = '+51923046453'  # Modifica este número según sea necesario

    cuerpo_sms = generar_mensaje_cambio(API_KEY_WAPI)
    enviar_sms(cuerpo_sms, DESTINATARIO)

if __name__ == '__main__':
    main()

