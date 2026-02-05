from django.db import models

class Pokemon(models.Model):
	title = models.CharField(max_length=200)
	image = models.ImageField(
		upload_to='pokemon_images/',
		blank=True,
		null=True,
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

	def __str__(self):
		return f"{self.pokemon.title} at ({self.lat}, {self.lon})"