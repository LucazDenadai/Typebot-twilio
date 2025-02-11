import sys
import os
import threading
from app import create_app
from pyngrok import ngrok, conf
import requests

# Adiciona o diretório raiz do projeto ao sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

app = create_app()

def get_ngrok_tunnel():
    try:
        tunnels = requests.get("http://localhost:4040/api/tunnels").json()
        for tunnel in tunnels['tunnels']:
            if tunnel['proto'] == 'http':
                return tunnel['public_url']
    except requests.exceptions.ConnectionError:
        return None

def run_ngrok():
    # Verifica se o ngrok já está rodando
    public_url = get_ngrok_tunnel()
    if not public_url:
        # Inicia o ngrok se não estiver rodando
        public_url = ngrok.connect(5000)
    
    print(f" * ngrok tunnel \"{public_url}\" -> \"http://127.0.0.1:5000\"")

if __name__ == "__main__":
    # Cria uma thread para rodar o ngrok
    ngrok_thread = threading.Thread(target=run_ngrok)
    
    # Inicia a thread do ngrok
    ngrok_thread.start()
    
    # Inicia o Flask na thread principal
    try:
        app.run(debug=True, use_reloader=False)
    except KeyboardInterrupt:
        print(" * Shutting down server...")
        ngrok.kill()
        ngrok_thread.join()