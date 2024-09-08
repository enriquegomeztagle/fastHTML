from fasthtml.common import *

app , rt = fast_app()


@rt('/')
def get():
    return Div(
        P('This is main message!'),
        Div(
            # Button should get to nex route
            Button('Show New Message', hx_get="/change"),
    ))


@rt('/change')
def get():
    return Div(
        P('This is route /change'),
    )

if __name__ == "__main__":
    uvicorn.run("button:app", host='0.0.0.0', port=8000, reload=True)

serve()
