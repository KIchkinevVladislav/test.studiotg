from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView

from .serializers import GameSerializer
from .models import Game


class GameCreateView(CreateAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer


    def create(self, request, *args, **kwargs):
        # Получаем данные из запроса
        data = request.data

        # Проверяем, чтобы количество мин не превышало (width * height - 1)
        width = int(data.get('width', 0))
        height = int(data.get('height', 0))
        mines_count = int(data.get('mines_count', 0))
        max_mines = width * height - 1

        if width > 30 or height > 30:
            return Response({'error': 'Размер игрового поля не может быть больше 30 в высоту или ширину'},
                            status=status.HTTP_400_BAD_REQUEST)

        if mines_count > max_mines:
            return Response({'error': f'Количество мин должно быть не менее 1 и не более {max_mines}'},
                            status=status.HTTP_400_BAD_REQUEST)

        # Продолжаем создание игры, если проверка прошла успешно
        return super().create(request, *args, **kwargs)

    
class TurnAPIView(APIView):

    def post(self, request):
        game_id = request.data.get('game_id')
        col = int(request.data.get('col'))
        row = int(request.data.get('row'))
        
        
        try:
            # Находим игру по game_id
            game = Game.objects.get(game_id=game_id)
        except Game.DoesNotExist:
            return Response({'error': f'Игра с идентификатором {game_id} не была создана или устарела (неактуальна)'}, status=status.HTTP_404_NOT_FOUND)
        
        # Проверяем, что игра не завершена
        if game.completed:
            return Response({'error': 'Игра уже завершена'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Проверяем, была ли уже открыта указанная ячейка
        if game.field[row][col] != ' ':
            return Response({'error': 'Ячейка уже была открыта'}, status=status.HTTP_400_BAD_REQUEST)
        
        
        # Проверяем, что в указанной ячейке нет мины
        if game.mine_field[row][col] == 'X':
            for i in range(game.height):
                for j in range(game.width):
                    if game.field[i][j] == ' ':
                        game.field[i][j] = game.mine_field[i][j]  # Открываем ячейку
            game.completed = True
            game.save()
            return Response({'message': 'Вы проиграли', 'field': game.field}, status=status.HTTP_200_OK)
                

        # Открываем ячейки рядом с указанной
        self.open_adjacent_cells(game, row, col)
        
        # Проверяем, завершена ли игра
        if self.check_win_game(game):
            game.completed = True
            game.save()
            return Response({'message': 'Вы победили', 'field': game.field}, status=status.HTTP_200_OK)
        
        # Возвращаем обновленные данные об игре
        serializer = GameSerializer(game)
        return Response(serializer.data)
    
    def open_adjacent_cells(self, game, row, col):
        # Открываем ячейки рядом с указанной, если они не заняты минами
        # Рекурсивно открываем смежные ячейки с нулевым значением
        field = game.field
        if game.mine_field[row][col] == '0':
            for i in range(max(0, row - 1), min(row + 2, game.height)):
                for j in range(max(0, col - 1), min(col + 2, game.width)):
                    if field[i][j] == ' ':
                        field[i][j] = game.mine_field[i][j]  # Открываем ячейку
                        if field[i][j] == '0':
                            self.open_adjacent_cells(game, i, j)
                    elif field[i][j].isdigit():
                        field[i][j] = field[i][j]
        else:
            field[row][col] = game.mine_field[row][col]  # Открываем ячейку

        game.field = field  # Обновляем поле игры
        game.save()


    def check_win_game(self, game):
        # Проверяем, завершена ли игра (все не-мины открыты)
        closed_cells_count = 0
        for row in game.field:
            for cell in row:
                if cell == ' ':
                    closed_cells_count += 1

        # Проверяем, что количество закрытых ячеек равно количеству мин
        if closed_cells_count == game.mines_count:
            # Заменяем закрытые ячейки с минами на 'M' в поле field
            for i in range(game.height):
                for j in range(game.width):
                    if game.field[i][j] == ' ' and game.mine_field[i][j] == 'X':
                        game.field[i][j] = 'M'
            return True

        return False