# PRACTICA_AWS

Práctica de integración con APIs (clima, Twilio SMS) usando Python y Jupyter.

## Requisitos

- Python 3.10+
- Cuenta en [Twilio](https://www.twilio.com/) (trial o paga)
- API key de [WeatherAPI](https://www.weatherapi.com/)

```bash
pip install twilio requests pandas beautifulsoup4 tqdm
```

## Configuración

1. Copia la plantilla de credenciales:

   ```bash
   copy twilio_config.example.py twilio_config.py
   ```

2. Edita `twilio_config.py` con tus valores reales (este archivo **no** se sube a Git).

3. En cuentas trial de Twilio, verifica tu número destino en **Console → Phone Numbers → Verified Caller IDs**.

4. Abre `Mensajes_Twilio+-+Template.ipynb` y ejecuta las celdas.

## Archivos sensibles (no versionados)

| Archivo | Motivo |
|---------|--------|
| `twilio_config.py` | Credenciales Twilio y API keys |
| `*.pem` | Claves privadas AWS/SSH |

## Notebooks

- `Mensajes_Twilio+-+Template.ipynb` — pronóstico del clima y envío de SMS con Twilio
- `draft.ipynb` — borrador local
