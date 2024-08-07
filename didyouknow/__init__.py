from httpx import AsyncClient
from jinja2 import Environment, DictLoader
from sanic import Sanic
from sanic.response import html

WIKIPEDIA_RANDOM_API_URL = "https://en.wikipedia.org/api/rest_v1/page/random/summary"

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
    <body class="bg-gradient-to-r from-sky-500 to-indigo-500 dark:from-slate-950 dark:to-black m-28">
        <div class="block-htmx-indicator max-w-sm mx-auto text-center p-28 text-2xl font-bold text-white">
            <img src="http://samherbert.net/svg-loaders/svg-loaders/oval.svg" class="inline-block w-28 h-28 pb-10">
            Loading
        </div>
        {% include "card.html" %}
        <div class="max-w-lg mx-auto px-12 pb-10 pt-10 text-center">
            <a
                href="."
                hx-get="/another"
                hx-target="#card"
                hx-swap="outerHTML"
                hx-indicator=".block-htmx-indicator"
                hx-on:click="document.getElementById('card').innerHTML = '';"
                class="inline-block border border-sky-100 text-sky-100 hover:bg-sky-100 hover:text-sky-900 active:bg-slate-800 active:text-sky-100 text-sm font-semibold py-2 px-4 rounded-md">
                Another
            </a>
        </div>
    </body>
</html>""",
    "card.html": """
<div id="card" class="max-w-lg mx-auto overflow-hidden rounded shadow-lg bg-white dark:bg-slate-800">
    <img src="{{ originalimage.source }}" class="w-full h-80 object-cover object-top">
    <div class="p-12 text-sm text-slate-700 dark:text-slate-100">
        {{ extract_html }}
        <a class="underline text-slate-500 dark:text-slate-200 hover:text-slate-900" href="{{ content_urls.desktop.page }}">See more...</a>
    </div>
</div>"""
})

app = Sanic(__name__)
app.ctx.jinja = Environment(loader=template_loader)

async def random_wikipedia_extract():
    async with AsyncClient() as client:
        response = await client.get(WIKIPEDIA_RANDOM_API_URL, follow_redirects=True)
        response.raise_for_status()
        return response.json()

def render_template(template, data):
    return html(app.ctx.jinja.get_template(template).render(**data))

@app.get("/")
async def index(request):
    data = await random_wikipedia_extract()
    return render_template("index.html", data)

@app.get("/another")
async def another(request):
    data = await random_wikipedia_extract()
    return render_template("card.html", data)
