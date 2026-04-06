import sys
import json
import requests

def main():
    if len(sys.argv) < 2:
        print("<MaltegoMessage><MaltegoTransformResponseMessage><Entities><Entity Type='maltego.Phrase'><Value>Error: Falta dominio</Value></Entity></Entities></MaltegoTransformResponseMessage></MaltegoMessage>")
        sys.exit(0)
    
    target_domain = sys.argv[1]
    
    # URL LOCAL (más adelante será AWS)
    API_URL = "http://localhost:9000/2015-03-31/functions/function/invocations"
    
    payload = {"target": target_domain}

    try:
        # Enviar petición (servidor local)
        respuesta = requests.post(API_URL, json=payload, timeout=70)
        datos_api = respuesta.json()
        
        # Extraer datos
        if 'body' in datos_api:
            resultados = json.loads(datos_api['body'])
        else:
            resultados = {}

        if 'error' in resultados:
            print(f"<MaltegoMessage><MaltegoTransformResponseMessage><Entities><Entity Type='maltego.Phrase'><Value>Error en Lambda: {resultados['error']}</Value></Entity></Entities></MaltegoTransformResponseMessage></MaltegoMessage>")
            sys.exit(0)

        emails = resultados.get('emails', [])
        hosts = resultados.get('hosts', [])

        # Formatear
        xml_output = "<MaltegoMessage>\n<MaltegoTransformResponseMessage>\n<Entities>\n"
        for email in emails:
            xml_output += f"  <Entity Type='maltego.EmailAddress'><Value>{email}</Value></Entity>\n"
        for host in hosts:
            xml_output += f"  <Entity Type='maltego.DNSName'><Value>{host}</Value></Entity>\n"
        xml_output += "</Entities>\n</MaltegoTransformResponseMessage>\n</MaltegoMessage>"
        
        print(xml_output)

    except Exception as e:
        print(f"<MaltegoMessage><MaltegoTransformResponseMessage><Entities><Entity Type='maltego.Phrase'><Value>Error: {str(e)}</Value></Entity></Entities></MaltegoTransformResponseMessage></MaltegoMessage>")

if __name__ == "__main__":
    main()