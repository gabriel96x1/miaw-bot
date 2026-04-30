from tools.web_search_tool import web_search

MODELO = "gpt-oss:20b"
ASSISTANT_NAME = "miaw-bot"

# --- BUCLE DE CONVERSACIÓN ---
def chat_loop(client) -> None:
    """ Core loop para interactuar con el chat. """
    # --- CONFIGURACIÓN INICIAL ---

    mensajes = []

    print(f"Chat con {ASSISTANT_NAME}\n")

    # Mapeo físico para poder ejecutar la función cuando el modelo la llame
    available_tools = {
        "web_search": web_search
    }

    while True:
        try:
            user_input = input("Tu: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nHasta luego!")
            break

        if not user_input or user_input.lower() in ("exit", "quit", "q", "salir"):
            print("\nAhí nos vidrios :D")
            break

        # Añadimos el mensaje del usuario limpio
        mensajes.append({"role": "user", "content": user_input + "Responde Breve"})

        print(f"\n{ASSISTANT_NAME}: \n", end="", flush=True)
        print("Pensanding...\n\n", end="", flush=True)

        # Primera llamada: El modelo decide si responde directo o llama a la herramienta [1]
        response = client.chat(
            model=MODELO,
            messages=mensajes,
            tools=[web_search],  # <--- Le pasamos la función nativa aquí [1]
            options={"think": "medium"}  # En Ollama el 'think' suele ir dentro de options
        )

        # Si el modelo decide que NO necesita buscar en la web:
        if not response.message.tool_calls:
            print(response.message.content)
            mensajes.append(response.message)
            print("\n")
            continue

        # Si el modelo SI decide que necesita buscar en la web:
        mensajes.append(response.message)  # Guardamos su decisión de llamar a la herramienta [1]

        for tool_call in response.message.tool_calls:
            func_name = tool_call.function.name
            func_args = tool_call.function.arguments

            if func_name in available_tools:
                print(f"🛠️ [Herramienta activada: {func_name}]...", flush=True)

                # Ejecutamos la búsqueda física
                tool_output = available_tools[func_name](query=func_args.get("query"))
                # print(f"🔍 [output: {str(tool_output)}]...", flush=True)

                # ¡CLAVE! Añadimos el resultado enlazándolo al nombre de la función
                mensajes.append({
                    "role": "tool",
                    "name": func_name,  # Obligatorio para que sepa qué herramienta fue
                    "content": str(tool_output)
                })

        # SEGUNDA LLAMADA:
        clean_messages = []

        for msg in mensajes:
            if msg.get("role") == "tool":
                clean_messages.append({
                    "role": "user",
                    "content": f"[Información obtenida]: {msg.get('content')}"
                })
            else:
                clean_messages.append(msg)

        # 2. Forzamos la llamada SIN herramientas y con stream
        final_response = client.chat(
            model=MODELO,
            messages=clean_messages,
            stream=True
        )

        full_response = ""
        for chunk in final_response:
            # 1. SI el bloque trae pensamiento, lo ignoramos para que no congele la pantalla
            if hasattr(chunk.message, 'thinking') and chunk.message.thinking:
                continue

            # 2. SI trae texto limpio, lo imprimimos y acumulamos
            token = chunk.message.content
            if token:
                print(token, end="", flush=True)
                full_response += token

        print("\n")

        # Guardamos la respuesta final como 'assistant'
        mensajes.append({"role": "assistant", "content": full_response})
