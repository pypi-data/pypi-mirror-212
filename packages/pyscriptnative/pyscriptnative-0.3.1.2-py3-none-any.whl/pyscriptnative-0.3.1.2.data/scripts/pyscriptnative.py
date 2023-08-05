from flask import Flask, render_template_string

__version__ = "0.3.1.2"

def template_html(body):
    template = '''
    <!DOCTYPE html>
    <html>

        <head>

            <link rel="stylesheet" href="https://pyscript.net/latest/pyscript.css" />

            <script defer src="https://pyscript.net/latest/pyscript.js"></script>

            {% block script %}

                <py-script>

                    {{ script }}

                </py-script>

            {% endblock %}

            {% block css %}

                <style>

                    {{ css }}
                
                </style>
            
            {% endblock %}
            
        </head>
        
        <body>

            {% block body %}

                ''' + body + '''

            {% endblock %}
                
        </body>

    </html>
    '''

    return template

class Router:
    def __init__(self):
        self.script_content = ""
        self.style_content = ""
        self.body_content = ""

    def script(self, func):
        self.script_content = func

    def html(self, func):
        self.body_content = func

    def css(self, func):
        self.style_content = func

    def run(self, host='localhost', port=8080, debug=False):
        app = Flask(__name__)

        @app.route('/')
        def index():
            return render_template_string(template_html(body=self.body_content), host=host, port=port, debug=debug, script=self.script_content, style=self.style_content)

        app.run(host=host, port=port, debug=debug)
