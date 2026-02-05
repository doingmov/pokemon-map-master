from django.db import models
from django.utils import timezone

class Pokemon(models.Model):
    title = models.CharField(max_length=200)
    title_en = models.CharField(
    	max_length=200,
    	blank=True,
    	null=True,
    	verbose_name="Name is English"
    	)
    title_jp = models.CharField(
    	max_length=200,
    	blank=True,
    	null=True,
    	verbose_name="Name is Japanese"
    	)
    image = models.ImageField(
        upload_to='pokemon_images/',
        blank=True,
        null=True,
    )
    description = models.TextField(
        blank=True,
        null=True,
    )
    previous_evolution = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='next_evolutions'
    )


    def __str__(self):
        return self.title



class PokemonEntity(models.Model):
	pokemon = models.ForeignKey(
		Pokemon,
		on_delete=models.CASCADE,
		related_name='entities'
		)
	lat = models.FloatField()
	lon = models.FloatField()
	appeared_at = models.DateTimeField(default=timezone.now)
	disappeared_at = models.DateTimeField(default=timezone.now)

	level = models.IntegerField(default=0)
	health = models.IntegerField(default=0)
	attack = models.IntegerField(default=0)
	defense = models.IntegerField(default=0)
	stamina = models.IntegerField(default=0)

	def __str__(self):
		return f"{self.pokemon.title} at ({self.lat}, {self.lon})"
