from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from django.http import HttpResponseNotFound

from piforever.settings import BASE_DIR

DIGIT_COUNT = 1_000_000_000
CHUNK_SIZE = 100
PI_FILE_PATH = BASE_DIR / 'pi-billion.txt'

def home(request):
    f = open(PI_FILE_PATH, 'rb')
    first_chunk = f.read(CHUNK_SIZE).decode("utf-8")
    f.close()

    return HttpResponse(loader.get_template("home.django.html").render({ "first_chunk": first_chunk }, request))

def digits(request, start_range):
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

