## README - Chatbot basado en FastHTML con integración de Amazon Bedrock

### Descripción
Este proyecto es una demostración de un chatbot sencillo utilizando **FastHTML**, **DaisyUI** (Tailwind CSS) para el diseño, y la API de Amazon Bedrock para generar respuestas automáticas del chatbot. La aplicación presenta un chat en tiempo real mediante WebSockets, donde el usuario puede interactuar con el bot y recibir respuestas generadas por un modelo alojado en Amazon Bedrock.

### Cómo ejecutar el código

#### Requisitos previos:
1. Instalar Python 3.9 o superior.
2. Instalar las dependencias necesarias ejecutando:
   ```bash
   pip install fasthtml boto3
   ```
3. Configurar las credenciales de AWS para utilizar la API de Amazon Bedrock. Esto se puede hacer utilizando el archivo `~/.aws/credentials` o configurando las variables de entorno `AWS_ACCESS_KEY_ID` y `AWS_SECRET_ACCESS_KEY`.

#### Ejecutar la aplicación:
1. Navega al directorio raíz del proyecto.
2. Inicia el servidor de FastHTML ejecutando:
   ```bash
   python main.py
   ```
3. La aplicación estará disponible en `http://localhost:8000`.

### Descripción de las funciones

1. **`MensajeChat(indice_mensaje, **kwargs)`**:
   - Genera una burbuja de chat en el HTML, formateada según el rol (usuario o asistente).
   - Usa las clases de DaisyUI para mostrar las burbujas de manera visualmente atractiva.

2. **`EntradaChat()`**:
   - Renderiza un campo de entrada para que el usuario ingrese su mensaje.
   - Utiliza un `input` de tipo texto con estilos predefinidos de Tailwind.

3. **`mostrar()`**:
   - Genera la página principal del chatbot. Muestra los mensajes anteriores y el campo de entrada para nuevos mensajes.
   - Utiliza un formulario que envía datos mediante WebSockets a la conexión establecida.

4. **`obtener_respuesta_bedrock(entrada_usuario)`**:
   - Envía el mensaje del usuario a la API de Amazon Bedrock y recibe la respuesta generada.
   - Maneja la autenticación con AWS, la invocación del modelo, y extrae el texto de la respuesta JSON devuelta.

5. **`ws(mensaje, enviar)`**:
   - Maneja la conexión WebSocket, recibiendo el mensaje del usuario y devolviendo la respuesta generada por Bedrock en tiempo real.
   - Simula un pequeño retraso antes de enviar la respuesta.

### Componentes utilizados
- **FastHTML**: Framework para renderizado HTML y manejo de rutas y WebSockets.
- **DaisyUI**: Extensión de Tailwind CSS para componentes estilizados.
- **Amazon Bedrock**: Servicio de AWS utilizado para generar las respuestas del chatbot mediante modelos preentrenados.

### Funcionalidad general
El usuario ingresa un mensaje en el chat, que se envía a través de WebSockets a un backend que utiliza **FastHTML**. El mensaje es procesado y se invoca el servicio de **Amazon Bedrock** para generar una respuesta. Esta respuesta es devuelta al cliente y se muestra como una burbuja de chat. Todo el sistema funciona de manera interactiva y en tiempo real.

## Autor
- **Enrique Gómez Tagle** - [Perfil de GitHub](https://github.com/enriquegomeztagle)
  
