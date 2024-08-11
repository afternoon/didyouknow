from random import choice

from jinja2 import Environment, DictLoader
from sanic import Sanic
from sanic.response import html

from .facts import load

template_loader = DictLoader({
    "index.html": """
<!DOCTYPE html>
<html lang="en">
    <head>
        <title>Did You Know?</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <script src="https://cdn.tailwindcss.com"></script>
        <script src="https://unpkg.com/htmx.org@2.0.1"></script>
        <style>
            .block-htmx-indicator{
                display: none;
            }
            .htmx-request.block-htmx-indicator {
                display: block;
            }
        </style>
    </head>
    <body class="bg-white dark:bg-slate-800 sm:bg-gradient-to-r sm:from-sky-500 sm:to-indigo-500 sm:dark:from-slate-950 sm:dark:to-black sm:m-28">
        <div class="block-htmx-indicator sm:max-w-sm sm:mx-auto text-center p-28 text-2xl font-bold text-white">
            <img src="http://samherbert.net/svg-loaders/svg-loaders/oval.svg" class="inline-block w-28 h-28 pb-10">
            Loading
        </div>
        {% include "card.html" %}
        <div class="sm:max-w-lg sm:mx-auto sm:px-12 sm:py-10 text-center">
            <a
                href="."
                hx-get="/another"
                hx-target="#card"
                hx-swap="outerHTML"
                hx-indicator=".block-htmx-indicator"
                hx-on:click="document.getElementById('card').innerHTML = '';"
                class="inline-block border hover:border-gray-500 hover:bg-gray-400
                active:border-gray-600 active:bg-gray-600 active:text-gray-100
                sm:border-sky-100 sm:text-sky-100 sm:hover:bg-sky-100 sm:hover:text-sky-900 sm:active:bg-slate-800 sm:active:text-sky-100
                dark:border-sky-100 dark:text-sky-100 dark:hover:bg-sky-100 dark:hover:text-sky-900 dark:active:bg-slate-800 dark:active:text-sky-100
                text-sm font-semibold py-2 px-4 rounded-md">
                Another
            </a>
        </div>
    </body>
</html>""",
    "card.html": """
<div id="card" class="sm:max-w-lg sm:mx-auto overflow-hidden sm:rounded sm:shadow-lg bg-white dark:bg-slate-800">
    <img src="{{ originalimage.source }}" class="w-full h-80 object-cover object-top">
    <div class="p-12 text-sm text-slate-700 dark:text-slate-100">
        {{ extract_html }}
        <a class="underline text-slate-500 dark:text-slate-200 hover:text-slate-900" href="{{ content_urls.desktop.page }}">See more...</a>
    </div>
</div>"""
})

app = Sanic("didyouknow")

app.ctx.jinja = Environment(loader=template_loader)

app.ctx.facts = load()

def render_template(template, data):
    return html(app.ctx.jinja.get_template(template).render(**data))

@app.get("/")
async def index(request):
    return render_template("index.html", choice(app.ctx.facts))

@app.get("/another")
async def another(request):
    return render_template("card.html", choice(app.ctx.facts))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
