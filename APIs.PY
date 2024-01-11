import pandas as pd
import requests

# Cargar el dataframe currency_codes.csv
df_currency = pd.read_csv('currency_codes.csv')

# Extraer los códigos ISO
iso_codes = df_currency['AlphabeticCode'].tolist()

# Realizar consultas para obtener tipos de cambio USD_<ISO_CODE>
exchange_rates = []
api_url = 'https://api-ninjas.com/api/exchangerate'

for iso_code in iso_codes:
    query_params = {'from': 'USD', 'to': iso_code}
    response = requests.get(api_url, params=query_params)
    
    if response.status_code == 200:
        data = response.json()
        exchange_rates.append({'iso_code': iso_code, 'exchange_rate': data['rate']})
    else:
        print(f"Error en la consulta para {iso_code}: {response.text}")

# Crear dataframe con los resultados
df_exchange_rates = pd.DataFrame(exchange_rates)

# Exportar el dataframe como monedas.csv
df_exchange_rates.to_csv('monedas.csv', index=False)

# Función para convertir el monto de una moneda a otra
def convert_currency(from_iso, to_iso, amount):
    # Obtener tipos de cambio de USD a ambas monedas
    usd_to_from = df_exchange_rates[df_exchange_rates['iso_code'] == from_iso]['exchange_rate'].values[0]
    usd_to_to = df_exchange_rates[df_exchange_rates['iso_code'] == to_iso]['exchange_rate'].values[0]
    
    # Convertir de la moneda de origen a USD y luego a la moneda de destino
    amount_usd = amount / usd_to_from
    converted_amount = amount_usd * usd_to_to
    
    return converted_amount

# Ejemplo de uso de la función
amount_to_convert = 100
converted_amount = convert_currency('EUR', 'USD', amount_to_convert)
print(f'{amount_to_convert} EUR es igual a {converted_amount:.2f} USD')
