from django.shortcuts import render
from django.template import loader
from django.http import StreamingHttpResponse
from django.http import HttpResponse
from django.http import HttpResponseNotFound

from piforever.settings import BASE_DIR

DIGIT_COUNT = 1_000_000_000
CHUNK_SIZE = 2048
PI_FILE_PATH = BASE_DIR / 'pi-billion.txt'

async def digits_of_pi():
    yield "<span id='digits' style='font-family: monospace;'>"
    f = open(PI_FILE_PATH, 'rb')
    next_chunk = f.read(CHUNK_SIZE).decode("utf-8")
    while len(next_chunk) > 0:
        yield f'{next_chunk}\n'
        next_chunk = f.read(CHUNK_SIZE).decode("utf-8")
    f.close()
    yield "</span>"

async def home(_):
    # return HttpResponse(loader.get_template("home.django.html").render({ "first_chunk": first_chunk }, request))
    return StreamingHttpResponse(digits_of_pi())

async def digits(request, start_range):
    if int(start_range) > DIGIT_COUNT - CHUNK_SIZE:
        return HttpResponseNotFound()
    f = open(PI_FILE_PATH, 'rb')
    f.seek(int(start_range))
    next_chunk = f.read(CHUNK_SIZE).decode("utf-8")
    f.close()
    template = loader.get_template("digits.django.html")
    context = {
        "digits": next_chunk,
        "next_index": int(start_range) + CHUNK_SIZE,
    }

    return HttpResponse(template.render(context, request))

