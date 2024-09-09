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
def generar_mensaje(cliente_bedrock, modelo_id, mensajes, tokens_max, temperatura):
    # Prepara el cuerpo de la solicitud en formato JSON
    cuerpo = json.dumps(
        {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": tokens_max,
            "messages": mensajes,
            "temperature": temperatura
        }
    )

    # Llama al modelo especificado en Bedrock con el contenido del cuerpo
    respuesta = cliente_bedrock.invoke_model(body=cuerpo, modelId=modelo_id)
    
    # Procesa la respuesta y la devuelve como un diccionario de Python
    cuerpo_respuesta = json.loads(respuesta.get('body').read())

    return cuerpo_respuesta

# Función para procesar la imagen con Bedrock
def procesar_imagen_con_bedrock(ruta_imagen):
    # Lee el archivo de imagen y lo codifica en base64
    with open(ruta_imagen, "rb") as archivo_imagen:
        contenido_imagen = base64.b64encode(archivo_imagen.read()).decode('utf8')

    # Crea el mensaje multimodal que incluye la imagen codificada y un mensaje de texto
    mensaje_multimodal = [
        { 
            "role": "user",
            "content": [
                {"type": "image", "source": { "type": "base64", "media_type": "image/jpeg", "data": contenido_imagen }},
                {"type": "text", "text": "¿Qué ves en esta imagen?"}
            ]
        }
    ]

    # Llama a la función para generar la respuesta usando Bedrock
    respuesta = generar_mensaje(
        cliente_bedrock, 
        modelo_id="anthropic.claude-3-sonnet-20240229-v1:0",
        mensajes=mensaje_multimodal,
        max_tokens=300,  # Máximo de tokens a generar
        temperatura=0.7  # Grado de aleatoriedad en la respuesta
    )
    return respuesta

# Aplicación FastHTML
app, rt = fast_app(live=True)

# Ruta para mostrar la página principal con el formulario de subida de imágenes
@rt('/')
def inicio():
    return Div(
        P('Página principal!', style="font-size: 20px; font-family: Arial; color: darkblue;"),
        Div(
            # Formulario para subir una imagen
            Form(
                Input(type="file", name="archivo", accept="image/*"),  # Solo permite imágenes
                Button('Subir archivo', type="submit", onclick="mostrarCarga()"),  # Muestra barra de carga al enviar
                method="POST",
                enctype="multipart/form-data",
                hx_post="/subir",  # Envía el archivo a la ruta /subir
                hx_target="#contenedor-principal",  # Actualiza el contenedor principal con la respuesta
                hx_swap="outerHTML"  # Reemplaza el contenido actual con el nuevo
            ),
            style="margin-top: 10px;"
        ),
        Div(
            "",  # Espacio para mostrar la barra de carga
            id="barra-carga",
            style="display: none; text-align: center; margin-top: 20px;"
        ),
        # Inyección de JavaScript para controlar la barra de carga
        Script("""
        function mostrarCarga() {
            var barraCarga = document.getElementById("barra-carga");
            barraCarga.style.display = "block";
            barraCarga.innerHTML = '<div style="width: 100%; background-color: #f3f3f3; border-radius: 5px;"><div style="width: 50%; height: 20px; background-color: #4CAF50; animation: carga 2s infinite;"></div></div><p>Procesando...</p>';
        }

        // Animación para la barra de carga
        var estilo = document.createElement('style');
        estilo.innerHTML = `
        @keyframes carga {
            0% { width: 0%; }
            100% { width: 100%; }
        }
        `;
        document.head.appendChild(estilo);
        """),
        style="background-color: lightblue; padding: 20px;",
        id="contenedor-principal"
    )

# Ruta que maneja la subida de archivos y procesa la imagen
@rt('/subir', methods=['POST'])
async def subir_archivo(request: Request):
    try:
        # Obtiene el formulario y el archivo enviado
        formulario = await request.form() 
        archivo = formulario.get('archivo')

        # Verifica si el archivo es una imagen válida
        if archivo and archivo.content_type in ["image/jpeg", "image/png", "image/jpg"]:
            # Directorio temporal para almacenar el archivo
            directorio = '/mnt/data/'
            
            # Verificar si el directorio existe, si no, crearlo
            if not os.path.exists(directorio):
                os.makedirs(directorio)

            # Definir la ruta completa del archivo
            ruta_archivo = f'{directorio}{archivo.filename}'
            
            # Guardamos el archivo en el sistema de archivos temporalmente
            with open(ruta_archivo, 'wb') as f:
                f.write(archivo.file.read())

            # Procesamos la imagen con Bedrock y obtenemos el resultado
            resultado_bedrock = procesar_imagen_con_bedrock(ruta_archivo)
            resultado_bedrock_texto = resultado_bedrock['content'][0]['text']  # Obtenemos el texto de la respuesta

            # Muestra los atributos del archivo y el resultado de Bedrock
            return Div(
                P(f"Archivo subido con éxito: {archivo.filename}", style="font-size: 20px; color: black;"),
                P(f"Tipo: {archivo.content_type}", style="color: black;"),
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
            # Retorna un mensaje de error si el archivo no es una imagen válida
            return Div(
                P('Error: Solo se permiten archivos de imagen (jpeg, png).', style="font-size: 20px; color: red;"),
                Div(
                    Button('Volver', hx_get='/', hx_target='#contenedor-principal', hx_swap='outerHTML')
                ),
                style="background-color: lightpink; padding: 20px;",
                id="contenedor-principal"
            )

    except MultipartParseError as e:
        # Maneja cualquier error en el análisis del archivo
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
