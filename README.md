
# FastHTML Web Application Templates

This repository contains basic templates for building web applications using the [FastHTML](https://fasthtml.vercel.app) framework, a Python-based, minimal, and scalable solution for modern web development. FastHTML is inspired by FastAPI and integrates seamlessly with HTMX to simplify building interactive web applications with minimal JavaScript. Whether you're building a simple webpage or a fully interactive SPA (Single Page Application), FastHTML allows for rapid development and easy scalability.

## Features

- **Pure Python:** Build your web apps entirely using Python with easy-to-read syntax.
- **HTMX Integration:** Use HTMX for dynamic content loading and interactivity without JavaScript.
- **Fast and Lightweight:** Designed to create fast-loading web applications with minimal overhead.
- **ASGI and Uvicorn support:** Seamlessly integrates with ASGI-based applications for high performance.
- **Reusable Components:** Simplify your development process with reusable and dynamic components.
  
## Getting Started

### Installation

You can install FastHTML via pip:

```bash
pip install python-fasthtml
```

### Usage

Here's a simple example of how to create a web app with FastHTML:

```python
from fasthtml.common import *

app, rt = fast_app()

@rt('/')
def get():
    return Div(P('Hello World!'), hx_get="/change")

@rt('/change')
def get_change():
    return P('Nice to be here!')

serve()
```

This creates a basic web page that loads "Hello World!" initially, and changes the content to "Nice to be here!" when clicked, thanks to HTMX integration.

### Template Overview

This repository contains the following templates:

1. **Chatbot with Amazon Bedrock Integration**:  
   A demo project showcasing a chatbot using FastHTML, DaisyUI (Tailwind CSS) for the UI, and Amazon Bedrock's API to generate automatic responses. It features real-time chat interaction using WebSockets, allowing users to chat with the bot, which responds with AI-generated answers hosted on Amazon Bedrock.

2. **FastHTML Basic Web Application**:  
   A simple web application built with the FastHTML framework. This project demonstrates dynamic content rendering, the integration of custom CSS, and interactive UI elements using HTMX for a seamless user experience.


### Running the App

To run any example, clone the repository and navigate to the desired example folder:

```bash
python main.py
```
After running the app, check the console output to see which port the server is running on (e.g., http://localhost:XXXX). Replace XXXX with the actual port number displayed in the console, and visit that URL in your browser to see the app in action.

## Autor
- [**Enrique Gómez Tagle**](https://github.com/enriquegomeztagle)


## Contributions

Feel free to contribute by submitting pull requests or reporting issues. Together, we can expand these templates and add more functionality to enhance the FastHTML ecosystem.

## Resources

- [FastHTML Documentation](https://fasthtml.vercel.app)
- [HTMX Documentation](https://htmx.org/)
- [PicoCSS](https://picocss.com)

## License

This project is licensed under the MIT License.
