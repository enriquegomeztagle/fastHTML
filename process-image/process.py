from fasthtml.common import *
from starlette.requests import Request
from multipart.exceptions import MultipartParseError
import boto3
import json
import base64
import os

# Configuración del cliente de Bedrock
cliente_bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')

# Función para enviar una imagen a Bedrock y obtener una respuesta
def generar_mensaje(cliente_bedrock, modelo_id, mensajes, max_tokens, top_p, temperatura):
    cuerpo = json.dumps(
        {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": max_tokens,
            "messages": mensajes,
            "temperature": temperatura,
            "top_p": top_p
        }
    )

    respuesta = cliente_bedrock.invoke_model(body=cuerpo, modelId=modelo_id)
    cuerpo_respuesta = json.loads(respuesta.get('body').read())

    return cuerpo_respuesta

# Función para procesar la imagen con Bedrock
def procesar_imagen_con_bedrock(ruta_imagen):
    with open(ruta_imagen, "rb") as archivo_imagen:
        contenido_imagen = base64.b64encode(archivo_imagen.read()).decode('utf8')

    mensaje_multimodal = [
        { 
            "role": "user",
            "content": [
                {"type": "image", "source": { "type": "base64", "media_type": "image/jpeg", "data": contenido_imagen }},
                {"type": "text", "text": "¿Qué hay en esta imagen?"}
            ]
        }
    ]

    # Llamada a Bedrock
    respuesta = generar_mensaje(
        cliente_bedrock, 
        modelo_id="anthropic.claude-3-sonnet-20240229-v1:0",  # Cambia este ID si es necesario
        mensajes=mensaje_multimodal, 
        max_tokens=512, 
        temperatura=0.5, 
        top_p=0.9
    )
    return respuesta

# Aplicación FastHTML
app, rt = fast_app(live=True)

@rt('/')
def inicio():
    return Div(
        P('Página principal!', style="font-size: 20px; font-family: Arial; color: darkblue;"),
        Div(
            Form(
                Input(type="file", name="archivo", accept="image/*"),  # Solo permitir imágenes
                Button('Subir archivo', type="submit"),
                method="POST",
                enctype="multipart/form-data",
                hx_post="/subir",
                hx_target="#contenedor-principal",
                hx_swap="outerHTML"
            ),
            style="margin-top: 10px;"
        ),
        style="background-color: lightblue; padding: 20px;",
        id="contenedor-principal"
    )

@rt('/subir', methods=['POST'])
async def subir_archivo(request: Request):
    try:
        formulario = await request.form()  # Procesa el formulario que contiene el archivo
        archivo = formulario.get('archivo')  # Obtén el archivo subido

        # Verifica si el archivo es una imagen
        if archivo and archivo.content_type in ["image/jpeg", "image/png", "image/jpg"]:
            # Definimos el directorio donde se guardarán los archivos
            directorio = '/mnt/data/'
            
            # Verificar si el directorio existe, si no, crearlo
            if not os.path.exists(directorio):
                os.makedirs(directorio)

            # Definir la ruta completa del archivo
            ruta_archivo = f'{directorio}{archivo.filename}'
            
            # Guardamos el archivo en el sistema de archivos temporalmente
            with open(ruta_archivo, 'wb') as f:
                f.write(archivo.file.read())

            # Procesamos la imagen con Bedrock
            resultado_bedrock = procesar_imagen_con_bedrock(ruta_archivo)
            resultado_bedrock_texto = resultado_bedrock['content'][0]['text']  # Obtenemos el texto del resultado

            # Muestra los atributos y el resultado de Bedrock
            return Div(
                P(f"Archivo subido con éxito: {archivo.filename}", style="font-size: 20px; color: black;"),
                P(f"Tipo MIME: {archivo.content_type}", style="color: black;"),
                Div(
                    P(f"Resultado del análisis de Bedrock:", style="font-size: 20px; color: black;"),
                    P(resultado_bedrock_texto, style="white-space: pre-wrap; line-height: 1.5; color: black;"),  # Preservamos saltos de línea y espacio
                    style="background-color: #f0f0f0; padding: 10px; border-radius: 5px;"
                ),
                Div(
                    Button('Volver', hx_get='/', hx_target='#contenedor-principal', hx_swap='outerHTML')
                ),
                style="background-color: lightblue; padding: 20px;",
                id="contenedor-principal"
            )
        else:
            # Retornar error si el archivo no es una imagen
            return Div(
                P('Error: Solo se permiten archivos de imagen (jpeg, png).', style="font-size: 20px; color: red;"),
                Div(
                    Button('Volver', hx_get='/', hx_target='#contenedor-principal', hx_swap='outerHTML')
                ),
                style="background-color: lightpink; padding: 20px;",
                id="contenedor-principal"
            )

    except MultipartParseError as e:
        print("Error al analizar el archivo:", e)
        return Div(
            P('Error al analizar el archivo subido. Asegúrate de que el archivo esté correcto.', style="font-size: 20px; color: red;"),
            Div(
                Button('Volver', hx_get='/', hx_target='#contenedor-principal', hx_swap='outerHTML')
            ),
            style="background-color: lightpink; padding: 20px;",
            id="contenedor-principal"
        )

serve()
