import sys
import json
import requests

def print_error(msg):
    print(f"<MaltegoMessage><MaltegoTransformResponseMessage><Entities><Entity Type='maltego.Phrase'><Value>{msg}</Value></Entity></Entities></MaltegoTransformResponseMessage></MaltegoMessage>")
    sys.exit(0)

def main():
    if len(sys.argv) < 2:
        print_error("Error: Falta dominio")
    
    target_domain = sys.argv[1]
    API_URL = "https://1oyld5mea3.execute-api.eu-north-1.amazonaws.com/prod/scan"
    payload = {"target": target_domain}

    try:
        respuesta = requests.post(API_URL, json=payload, timeout=70)
        
        # Si AWS devuelve error (ej. 500 o 504) se muestra en Maltego
        if respuesta.status_code != 200:
            print_error(f"Error AWS ({respuesta.status_code}): {respuesta.text}")
            
        datos_api = respuesta.json()

        # Manejo dual: Por si API Gateway no está en modo Proxy y devuelve el 'body' literal
        if 'body' in datos_api and isinstance(datos_api['body'], str):
            resultados = json.loads(datos_api['body'])
        else:
            resultados = datos_api # Si es modo Proxy, los datos ya están aquí

        emails = resultados.get('emails', [])
        hosts = resultados.get('hosts', [])

        # Formatear
        xml_output = "<MaltegoMessage>\n<MaltegoTransformResponseMessage>\n<Entities>\n"
        
        if not emails and not hosts:
            xml_output += f"  <Entity Type='maltego.Phrase'><Value>No se encontraron resultados en theHarvester</Value></Entity>\n"
            
        for email in emails:
            xml_output += f"  <Entity Type='maltego.EmailAddress'><Value>{email}</Value></Entity>\n"
        for host in hosts:
            xml_output += f"  <Entity Type='maltego.DNSName'><Value>{host}</Value></Entity>\n"
        xml_output += "</Entities>\n</MaltegoTransformResponseMessage>\n</MaltegoMessage>"
        
        print(xml_output)

    except requests.exceptions.Timeout:
        print_error("Error: Timeout de la conexión (API Gateway tardó más de 70s)")
    except Exception as e:
        print_error(f"Error local: {str(e)}")

if __name__ == "__main__":
    main()