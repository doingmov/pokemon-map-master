import folium
from django.http import HttpResponseNotFound
from django.shortcuts import render
from django.utils.timezone import localtime
from .models import Pokemon, PokemonEntity


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
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    pokemons = Pokemon.objects.all()
    now = localtime()

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)

    entities = PokemonEntity.objects.filter(
        appeared_at__lte=now,
        disappeared_at__gte=now
    )

    for entity in entities:
        img_url = (
            request.build_absolute_uri(entity.pokemon.image.url)
            if entity.pokemon.image else DEFAULT_IMAGE_URL
        )
        add_pokemon(folium_map, entity.lat, entity.lon, img_url)

    pokemons_on_page = []
    for pokemon in pokemons:
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': (
                request.build_absolute_uri(pokemon.image.url)
                if pokemon.image else None
            ),
            'title_ru': pokemon.title,
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    try:
        pokemon = Pokemon.objects.get(id=pokemon_id)
    except Pokemon.DoesNotExist:
        return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')

    now_time = localtime()
    entities = pokemon.entities.filter(
        appeared_at__lte=now_time,
        disappeared_at__gte=now_time
    )

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)

    for entity in entities:
        img_url = (
            request.build_absolute_uri(entity.pokemon.image.url)
            if entity.pokemon.image else DEFAULT_IMAGE_URL
        )
        add_pokemon(folium_map, entity.lat, entity.lon, img_url)

    first_entity = entities.first()

    pokemon_data = {
        'pokemon_id': pokemon.id,
        'img_url': (
            request.build_absolute_uri(pokemon.image.url)
            if pokemon.image else None
        ),
        'title_ru': pokemon.title,
        'title_en': pokemon.title_en,
        'title_jp': pokemon.title_jp,
        'level': first_entity.level if first_entity else None,
        'health': first_entity.health if first_entity else None,
        'attack': first_entity.attack if first_entity else None,
        'defense': first_entity.defense if first_entity else None,
        'stamina': first_entity.stamina if first_entity else None,
        'description': pokemon.description
    }

    if pokemon.previous_evolution:
        prev = pokemon.previous_evolution
        pokemon_data['previous_evolution'] = {
            'pokemon_id': prev.id,
            'title_ru': prev.title,
            'img_url': (
                request.build_absolute_uri(prev.image.url)
                if prev.image else None
            ),
        }

    next_entity = pokemon.next_evolutions.first()
    pokemon_data['next_evolution'] = (
        {
            'pokemon_id': next_entity.id,
            'title_ru': next_entity.title,
            'img_url': (
                request.build_absolute_uri(next_entity.image.url)
                if next_entity.image else None
            ),
        }
        if next_entity else None
    )

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(),
        'pokemon': pokemon_data
    })
