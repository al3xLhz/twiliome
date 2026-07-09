
import time
from datetime import datetime
import pandas as pd
import requests
from tqdm import tqdm
from twilio.rest import Client
from twilio_config import *

def build_weather_url(city: str, api_key: str) -> str:
    """Genera la URL de consulta para la API del clima."""
    return f'http://api.weatherapi.com/v1/forecast.json?key={api_key}&q={city}&days=1&aqi=no&alerts=no'

def get_forecast(hour_data: dict) -> tuple:
    """
    Extrae información relevante de un bloque horario de la respuesta climática.
    """
    fecha = hour_data['time'].split()[0]
    hora = int(hour_data['time'].split()[1].split(':')[0])
    condicion = hour_data['condition']['text']
    tempe = float(hour_data['temp_c'])
    rain = hour_data['will_it_rain']
    prob_rain = hour_data['chance_of_rain']
    return fecha, hora, condicion, tempe, rain, prob_rain

def fetch_weather_data(query: str, api_key: str) -> pd.DataFrame:
    """Obtiene y procesa el pronóstico horario para una ciudad."""
    url = build_weather_url(query, api_key)
    response = requests.get(url).json()
    horas = response['forecast']['forecastday'][0]['hour']
    datos = [get_forecast(h) for h in tqdm(horas, colour='green')]
    columnas = ['Fecha', 'Hora', 'Condicion', 'Temperatura', 'Lluvia', 'prob_lluvia']
    df = pd.DataFrame(datos, columns=columnas)
    df = df.sort_values(by='Hora', ascending=True)
    return df

def filtrar_lluvias(df: pd.DataFrame) -> pd.DataFrame:
    """Filtra solo las horas con lluvia entre las 7 y las 21."""
    df_rain = df[(df['Lluvia'] == 1) & (df['Hora'] > 6) & (df['Hora'] < 22)]
    df_rain = df_rain[['Hora', 'Condicion']]
    df_rain.set_index('Hora', inplace=True)
    return df_rain

def horas_a_rangos(horas: list[int]) -> str:
    """Agrupa horas consecutivas en rangos (ej. [7, 8, 9, 14] -> '7-9, 14')."""
    if not horas:
        return ""
    horas = sorted(horas)
    rangos = []
    inicio = fin = horas[0]
    for h in horas[1:]:
        if h == fin + 1:
            fin = h
        else:
            rangos.append(f"{inicio}-{fin}" if inicio != fin else str(inicio))
            inicio = fin = h
    rangos.append(f"{inicio}-{fin}" if inicio != fin else str(inicio))
    return ", ".join(rangos)


def generar_mensaje(df: pd.DataFrame, df_rain: pd.DataFrame, ciudad: str) -> str:
    """Genera el texto del SMS a enviar según los datos procesados."""
    fecha = df['Fecha'].iloc[0]
    if df_rain.empty:
        horas_str = "sin lluvia esperada"
    else:
        horas_str = f"{horas_a_rangos(df_rain.index.tolist())}h"

    return f"Lluvia hoy {fecha} en {ciudad}: {horas_str}"

def enviar_sms(mensaje: str, to_number: str) -> None:
    """Envía un mensaje SMS usando Twilio."""
    time.sleep(2)  # Espera para evitar límites de rate
    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        message = client.messages.create(
            body=mensaje,
            from_=PHONE_NUMBER,
            to=to_number
        )
        print('Mensaje Enviado:', message.sid)
    except Exception as e:
        print(f"Error al enviar el mensaje: {e}")

def main():
    CIUDAD = 'Lima'
    DESTINATARIO = '+51923046453'  # Modifica este número según sea necesario

    df_clima = fetch_weather_data(CIUDAD, API_KEY_WAPI)
    df_lluvia = filtrar_lluvias(df_clima)
    cuerpo_sms = generar_mensaje(df_clima, df_lluvia, CIUDAD)
    enviar_sms(cuerpo_sms, DESTINATARIO)

if __name__ == '__main__':
    main()

