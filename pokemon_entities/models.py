from django.db import models
from django.utils import timezone

class Pokemon(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название")
    title_en = models.CharField(
    	max_length=200,
    	blank=True,
    	null=True,
    	verbose_name="Название (английский)"
    	)
    title_jp = models.CharField(
    	max_length=200,
    	blank=True,
    	null=True,
    	verbose_name="Название (японский)"
    	)
    image = models.ImageField(
        upload_to='pokemon_images/',
        blank=True,
        null=True,
        verbose_name="Изображение"
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Описание"
    )
    previous_evolution = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='next_evolutions',
        verbose_name="Из кого эволюционировал"
    )


    def __str__(self):
        return self.title



class PokemonEntity(models.Model):
	pokemon = models.ForeignKey(
		Pokemon,
		on_delete=models.CASCADE,
		related_name='entities',
		verbose_name="Покемон"
		)
	lat = models.FloatField(verbose_name="Широта")
	lon = models.FloatField(verbose_name="Долгота")
	appeared_at = models.DateTimeField(default=timezone.now, verbose_name="Время появления")
	disappeared_at = models.DateTimeField(default=timezone.now, verbose_name="Время исчезновения")

	level = models.IntegerField(default=0, verbose_name="Уровень")
	health = models.IntegerField(default=0, verbose_name="Здоровье")
	attack = models.IntegerField(default=0, verbose_name="Атака")
	defense = models.IntegerField(default=0, verbose_name="Защита")
	stamina = models.IntegerField(default=0, verbose_name="Выносливость")

	def __str__(self):
		return f"{self.pokemon.title} at ({self.lat}, {self.lon})"
