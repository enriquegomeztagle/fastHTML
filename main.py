from fasthtml.common import *

app, rt = fast_app()

# Defining CSS styling
style = """
    body {
        font-family: Arial, sans-serif;
        background-color: #f0f0f5;
        color: #333;
        text-align: center;
        padding: 50px;
    }

    .container {
        background-color: #fff;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        padding: 20px;
        max-width: 600px;
        margin: 0 auto;
    }

    p {
        font-size: 20px;
        margin: 20px 0;
        transition: all 0.3s ease;
    }

    p:hover {
        color: #28a745;
        transform: scale(1.05);
    }

    button {
        padding: 10px 20px;
        font-size: 18px;
        background-color: #28a745;
        color: #fff;
        border: none;
        border-radius: 5px;
        cursor: pointer;
        transition: background-color 0.3s ease;
    }

    button:hover {
        background-color: #258738;
    }
"""

@rt('/')
def get():
    # Return styled container with introductory message and button to change it
    return Div(
        P('This is main message!'),
        Div(
            Button('Show New Message', hx_get="/change"),
            _class="container"
        ),
        Style(style)  # Including defined CSS styling
    )

@rt('/change')
def get():
    # When button is clicked, change message
    return Div(
        P('This is route /change'),
        _class="container"
    )

serve()
