import uuid 
from django.core.validators import MaxValueValidator
from django.db import models


class Game(models.Model):
    game_id = models.UUIDField(
        default=uuid.uuid4,
        primary_key=True,
        editable=False,
        unique=True
    )
    width = models.PositiveIntegerField(validators=[MaxValueValidator(30)])
    height = models.PositiveIntegerField(validators=[MaxValueValidator(30)])
    mines_count = models.PositiveIntegerField()
    field = models.JSONField(default=list)
    completed = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Игра'
        verbose_name_plural = 'Игры'

    def initialize_game(self):
        # Инициализация поля field
        self.field = [[" " for _ in range(self.width)] for _ in range(self.height)]
        self.save()


    # def to_json(self):
    #     return {
    #         "game_id": str(self.game_id),
    #         "width": self.width,
    #         "height": self.height,
    #         "mines_count": self.mines_count,
    #         "completed": self.completed,
    #         "field": self.field,
    #     }