from fasthtml.common import *
import asyncio
import boto3
import json
import logging

logging.basicConfig(level=logging.INFO)

# Configuración de daisyui y tailwind para el componente
tlink = Script(src="https://cdn.tailwindcss.com"),
dlink = Link(rel="stylesheet", href="https://cdn.jsdelivr.net/npm/daisyui@4.11.1/dist/full.min.css")
app = FastHTML(hdrs=(tlink, dlink, picolink), ws_hdr=True)

mensajes = []

# Burbuja de chat
def MensajeChat(indice_mensaje, **kwargs):
    """
    Función que genera la burbuja de chat, formateando el mensaje según el rol del usuario.
    """
    mensaje = mensajes[indice_mensaje]
    clase_burbuja = "chat-bubble-primary" if mensaje['role'] == 'user' else 'chat-bubble-secondary'
    clase_chat = "chat-end" if mensaje['role'] == 'user' else 'chat-start'
    return Div(Div(mensaje['role'], cls="chat-header"),
               Div(mensaje['content'],
                   id=f"contenido-chat-{indice_mensaje}",
                   cls=f"chat-bubble {clase_burbuja}"),
               id=f"mensaje-chat-{indice_mensaje}",
               cls=f"chat {clase_chat}", **kwargs)

# Campo de entrada del mensaje del usuario
def EntradaChat():
    """
    Función que genera el campo de entrada de texto para que el usuario ingrese el mensaje.
    """
    return Input(type="text", name='mensaje', id='entrada-mensaje',
                 placeholder="Escribe un mensaje",
                 cls="input input-bordered w-full", hx_swap_oob='true')

# Pantalla principal
@app.route("/")
def mostrar():
    """
    Genera la página principal del chatbot, mostrando los mensajes anteriores y el campo de entrada.
    """
    pagina = Body(H1('Demostración de Chatbot'),
                Div(*[MensajeChat(indice_mensaje) for indice_mensaje, mensaje in enumerate(mensajes)],
                    id="lista-chat", cls="chat-box h-[73vh] overflow-y-auto"),
                Form(Group(EntradaChat(), Button("Enviar", cls="btn btn-primary")),
                    ws_send=True, hx_ext="ws", ws_connect="/wscon",
                    cls="flex space-x-2 mt-2"),
                cls="p-4 max-w-lg mx-auto")
    return Title('Demostración de Chatbot'), pagina


# Función para obtener la respuesta de Amazon Bedrock usando la API de Mensajes y devolver solo el texto
def obtener_respuesta_bedrock(entrada_usuario):
    """
    Envía el mensaje del usuario a Amazon Bedrock y obtiene la respuesta del asistente.

    :param entrada_usuario: El mensaje del usuario enviado al chatbot.
    :return: El texto de la respuesta generada por el asistente.
    """
    cliente = boto3.client('bedrock-runtime', region_name='us-east-1')
    
    # Registrar el mensaje que se envió
    logging.info(f"Mensaje enviado: {entrada_usuario}")
    
    # Preparar el historial de mensajes para la API de Mensajes
    mensajes_api = [
        {"role": "user", "content": entrada_usuario},  # Mensaje del usuario
    ]
    
    # Preparar el payload con los parámetros requeridos
    carga_util = {
        "messages": mensajes_api,
        "max_tokens": 30,
        "anthropic_version": "bedrock-2023-05-31",  
    }
    
    # Convertir el payload a JSON y codificarlo como bytes
    carga_bytes = json.dumps(carga_util).encode('utf-8')
    
    respuesta = cliente.invoke_model(
        modelId='anthropic.claude-3-haiku-20240307-v1:0',
        body=carga_bytes,
        accept='application/json',
        contentType='application/json'
    )
    
    # Leer y decodificar la respuesta
    cuerpo_respuesta = respuesta['body'].read().decode('utf-8')
    json_respuesta = json.loads(cuerpo_respuesta)  # Convertir la respuesta a JSON
    
    # Extraer el contenido de texto de la respuesta del asistente
    contenido_texto = ''.join([parte['text'] for parte in json_respuesta['content'] if parte['type'] == 'text'])
    
    # Registrar la salida obtenida
    logging.info(f"Respuesta obtenida: {contenido_texto}")
    
    return contenido_texto  # Devolver solo el contenido del texto

# Conexión WebSocket para manejar la conversación
@app.ws('/wscon')
async def ws(mensaje: str, enviar):
    """
    Función que maneja los mensajes del usuario y las respuestas en el WebSocket.
    
    :param mensaje: Mensaje enviado por el usuario.
    :param enviar: Función para enviar la respuesta al cliente.
    """
    # Registrar el mensaje del usuario
    mensajes.append({"role": "user", "content": mensaje.rstrip()})
    await enviar(Div(MensajeChat(len(mensajes)-1), hx_swap_oob='beforeend', id="lista-chat"))

    # Limpiar el campo de entrada
    await enviar(EntradaChat())

    # Simular una espera antes de obtener la respuesta
    await asyncio.sleep(1)

    # Obtener la respuesta de Amazon Bedrock
    respuesta_bedrock = obtener_respuesta_bedrock(mensaje.rstrip())

    # Responder con la respuesta generada por Bedrock
    mensajes.append({"role": "assistant", "content": respuesta_bedrock})
    await enviar(Div(MensajeChat(len(mensajes)-1), hx_swap_oob='beforeend', id="lista-chat"))

if __name__ == '__main__':
    uvicorn.run("main:app", host='0.0.0.0', port=8000, reload=True)
