import folium
import json

from django.http import HttpResponseNotFound
from django.shortcuts import render
from .models import Pokemon, PokemonEntity
from django.utils.timezone import localtime, now
from django.utils import timezone

MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    pokemons = Pokemon.objects.all()
    now = localtime(timezone.now())

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)

    entities = PokemonEntity.objects.filter(
        appeared_at__lte=now,
        disappeared_at__gte=now)

    for entity in entities:
        if entity.pokemon.image:
            img_url = request.build_absolute_uri(entity.pokemon.image.url)
        else:
            img_url = DEFAULT_IMAGE_URL

        add_pokemon(folium_map, entity.lat, entity.lon, img_url)

    pokemons_on_page = []
    for pokemon in pokemons:
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': request.build_absolute_uri(pokemon.image.url) if pokemon.image else None,
            'title_ru': pokemon.title,
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })



from django.utils.timezone import localtime, now
from django.http import HttpResponseNotFound
from django.shortcuts import render
from .models import Pokemon, PokemonEntity

def show_pokemon(request, pokemon_id):
    try:
        pokemon = Pokemon.objects.get(id=pokemon_id)
    except Pokemon.DoesNotExist:
        return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')

    now_time = localtime(now())
    entities = pokemon.entities.filter(
        appeared_at__lte=now_time,
        disappeared_at__gte=now_time
    )

    folium_map = folium.Map(location=[55.751244, 37.618423], zoom_start=12)

    for entity in entities:
        if entity.pokemon.image:
            img_url = request.build_absolute_uri(entity.pokemon.image.url)
        else:
            img_url = (
                'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
                '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
                '&fill=transparent'
            )
        add_pokemon(folium_map, entity.lat, entity.lon, img_url)

    pokemon_data = {
        'pokemon_id': pokemon.id,
        'img_url': request.build_absolute_uri(pokemon.image.url) if pokemon.image else None,
        'title_ru': pokemon.title,
        'level': entities.first().level if entities.exists() else None,
        'health': entities.first().health if entities.exists() else None,
        'attack': entities.first().attack if entities.exists() else None,
        'defense': entities.first().defense if entities.exists() else None,
        'stamina': entities.first().stamina if entities.exists() else None,
    }

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(),
        'pokemon': pokemon_data
    })
