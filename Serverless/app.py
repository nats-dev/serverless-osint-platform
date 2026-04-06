import sys
import subprocess
import json
import os

def handler(event, context):
    print(f"--- Evento recibido: {event} ---")
    target = None
    
    # Extraer dominio (target)
    if isinstance(event, dict):
        if 'target' in event:
            target = event['target']
        elif 'body' in event:
            try:
                # Caso por si viene como string (API Gateway)
                body = json.loads(event['body']) if isinstance(event['body'], str) else event['body']
                target = body.get('target', '')
            except:
                pass

    if not target:
        print("Error: No se recibió el target")
        return {"statusCode": 400, "body": json.dumps({"error": "Falta el dominio"})}

    output_file = "/tmp/resultados"
    
    # Configuración theHarvester (prueba sencilla)
    cmd = [
        "theHarvester", 
        "-d", target,
        "-b", "crtsh,duckduckgo,brave", 
        "-l", "500",
        "-f", output_file
    ]

    try:
        # Cambiar el directorio HOME a /tmp para evitar problemas en Lambda
        my_env = os.environ.copy()
        my_env["HOME"] = "/tmp"

        # Ejecutar theHarvester
        print(f"Ejecutando comando: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=600, env=my_env)

        # Imprimir todo para evitar errores en Cloudwatch
        print("STDOUT:", result.stdout)
        print("STDERR:", result.stderr)
        
        # Leer resultados
        json_path = output_file + ".json"
        if not os.path.exists(json_path):
            #Debug
            debug_info = f"STDOUT: {result.stdout} | STDERR: {result.stderr}"
            return {
                "statusCode": 404, 
                "body": json.dumps({"error": f"theHarvester falló y no creó el JSON. Logs: {debug_info}"})
            }

        with open(json_path, 'r') as f:
            data = json.load(f)
            
        emails = data.get('emails', [])
        hosts = data.get('hosts', [])
        clean_hosts = [h.split(':')[0] if ':' in h else h for h in hosts]
        
        # Devolver resultados en HTTP
        print(f"Éxito: {len(emails)} emails, {len(clean_hosts)} hosts.")
        return {
            "statusCode": 200,
            "body": json.dumps({
                "target": target,
                "emails": emails,
                "hosts": clean_hosts
            })
        }

    except Exception as e:
        print(f"Error: {str(e)}")
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}