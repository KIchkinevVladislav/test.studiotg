import uuid 
import random

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
    mine_field = models.JSONField(default=list)

    class Meta:
        verbose_name = 'Игра'
        verbose_name_plural = 'Игры'


    def initialize_game(self):
        # Инициализация поля с закрытыми ячейками
        self.field = [[" " for _ in range(self.width)] for _ in range(self.height)]

        # Инициализация поля с минами и смежными ячейками
        self.mine_field = [["0" for _ in range(self.width)] for _ in range(self.height)]

        # Размещение мин
        mines_to_place = self.mines_count
        while mines_to_place > 0:
            row = random.randint(0, self.height - 1)
            col = random.randint(0, self.width - 1)
            if self.mine_field[row][col] != "X":  # Проверка, что в ячейке еще нет мины
                self.mine_field[row][col] = "X"
                mines_to_place -= 1

        # Подсчет количества мин в смежных ячейках и заполнение поля mine_field
        for row in range(self.height):
            for col in range(self.width):
                if self.mine_field[row][col] != "X":  # Пропускаем ячейки с минами
                    adjacent_mines_count = 0
                    for i in range(max(0, row - 1), min(row + 2, self.height)):
                        for j in range(max(0, col - 1), min(col + 2, self.width)):
                            if self.mine_field[i][j] == "X":
                                adjacent_mines_count += 1
                    self.mine_field[row][col] = str(adjacent_mines_count)

        # Сохранение игры
        self.save()