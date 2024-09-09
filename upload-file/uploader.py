from fasthtml.common import *
from starlette.requests import Request
from multipart.exceptions import MultipartParseError

app, rt = fast_app(live=True)

@rt('/')
def get():
    return Div(
        P('Página principal!', style="font-size: 20px; font-family: Arial; color: darkblue;"),
        Div(
            Form(
                Input(type="file", name="archivo"),
                Button('Subir archivo', type="submit"),
                method="POST",
                enctype="multipart/form-data",
                hx_post="/upload",
                hx_target="#contenedor-principal",
                hx_swap="outerHTML"
            ),
            style="margin-top: 10px;"
        ),
        style="background-color: lightblue; padding: 20px;",
        id="contenedor-principal"
    )

@rt('/upload', methods=['POST'])
async def upload_file(request: Request):
    try:
        form = await request.form()  # Procesa el formulario que contiene el archivo
        archivo = form.get('archivo')  # Obtén el archivo subido

        if archivo:
            # Aquí imprimimos los atributos del archivo
            print("Nombre del archivo:", archivo.filename)
            print("Tipo MIME:", archivo.content_type)
            print("Tamaño del archivo:", archivo.__sizeof__())

            # Muestra los atributos en la respuesta
            return Div(
                P(f"Archivo subido con éxito: {archivo.filename}", style="font-size: 20px; color: black;"),
                P(f"Tipo MIME: {archivo.content_type}", style="color: black;"),
                P(f"Tamaño: {archivo.__sizeof__()} bytes", style="color: black;"),
                Div(
                    Button('Volver', hx_get='/', hx_target='#contenedor-principal', hx_swap='outerHTML')
                ),
                style="background-color: lightblue; padding: 20px;",
                id="contenedor-principal"
            )
        else:
            return Div(
                P('Error: No se ha seleccionado ningún archivo.', style="font-size: 20px; color: red;"),
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
