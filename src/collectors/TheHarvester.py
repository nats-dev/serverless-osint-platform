import subprocess
import json

def run_theharvester(domain):
    try:
        command = [
            "theHarvester",
            "-d", domain,
            "-b", "all",
            "-f", "output"
        ]

        subprocess.run(command, check=True)

        with open("output.json", "r") as file:
            data = json.load(file)

        return data

    except Exception as e:
        print(f"Error running TheHarvester: {e}")
        return None