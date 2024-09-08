from fasthtml.common import *

app, rt = fast_app(live=True)

@rt('/')
def get():
    return Div(
        P('Página principal!', style="font-size: 20px; font-family: Arial; color: darkblue;"),
        Div(
            Button('Cambiar mensaje', hx_get='/mensaje2', hx_target='#contenedor-principal', hx_swap='outerHTML')
        ),
        style="background-color: lightblue; padding: 20px;",
        id="contenedor-principal"
    )

@rt('/mensaje2')
def new_message():
    return Div(
        P('Mensaje 2 con otro estilo!', style="font-size: 22px; font-family: Verdana; color: darkgreen;"),
        Div(
            Button('Volver', hx_get='/', hx_target='#contenedor-principal', hx_swap='outerHTML')
        ),
        style="background-color: lightgreen; padding: 20px;",
        id="contenedor-principal" 
    )

serve()
