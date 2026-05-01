import argparse
from miaw_bot.chat_loop import chat_loop
import ollama


def client_initializer(ip_servidor: str = None) -> ollama.Client:
    """
    Inicializa el cliente de Ollama apuntando a una PC remota o a localhost por defecto.
    """
    if ip_servidor:
        print(f"📡 Conectando a Ollama remoto en: http://{ip_servidor}:11434")
        return ollama.Client(host=f"http://{ip_servidor}:11434")
    else:
        print("💻 Conectando a Ollama en modo local (localhost)")
        return ollama.Client()

def main():
    """
    El main del proyecto
    """
    # --- CONFIGURACIÓN DE ARGUMENTOS DE TERMINAL ---
    parser = argparse.ArgumentParser(description="Asistente con soporte para red local.")
    parser.add_argument(
        "--ip", 
        type=str,
        default=None,
        help="IP de la computadora remota donde corre Ollama. Si no se pasa, usa localhost."
    )
    args = parser.parse_args()

    # Creamos el cliente usando el argumento capturado de la terminal
    client = client_initializer(args.ip)

    chat_loop(client)


if __name__ == "__main__":
    main()
