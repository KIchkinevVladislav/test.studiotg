
import random
from rest_framework.response import Response
from rest_framework import status
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

        if mines_count > max_mines:
            return Response({'error': f'Количество мин должно быть не менее 1 и не более {max_mines}'},
                            status=status.HTTP_400_BAD_REQUEST)

        # Продолжаем создание игры, если проверка прошла успешно
        return super().create(request, *args, **kwargs)

 




# class TurnAPIView(APIView):
#     def post(self, request):
#         game_id = request.data.get('game_id')
#         row = request.data.get('row')
#         col = request.data.get('col')
        
#         try:
#             # Находим игру по game_id
#             game = Game.objects.get(game_id=game_id)
#         except Game.DoesNotExist:
#             return Response({'error': f'Игра с идентификатором {game_id} не была создана или устарела (неактуальна)'}, status=status.HTTP_404_NOT_FOUND)
        
#         # Проверяем, что игра не завершена
#         if game.completed:
#             return Response({'error': 'Игра уже завершена'}, status=status.HTTP_400_BAD_REQUEST)
        
#         field = game.field
        
#         # Проверяем, была ли уже открыта указанная ячейка
#         if game.field[row][col] != ' ':
#             return Response({'error': 'Ячейка уже была открыта'}, status=status.HTTP_400_BAD_REQUEST)
        
#         # Проверяем, что в указанной ячейке нет мины
#         if field[row][col] == 'X':
#             game.completed = True
#             game.save()
#             return Response({'message': 'Игра завершена. Вы попали на мину!', 'field': game.field}, status=status.HTTP_200_OK)
        
#         # Открываем ячейки рядом с указанной
#         self.open_adjacent_cells(game, row, col)
        
#         # Проверяем, завершена ли игра
#         if self.check_game_completed(game):
#             game.completed = True
#             game.save()
#             return Response({'message': 'Игра завершена. Вы открыли все ячейки, не занятые минами!', 'field': game.field}, status=status.HTTP_200_OK)
        
#         print("Field after opening cells:", field)        
        
#         # Возвращаем обновленные данные об игре
#         serializer = GameSerializer(game)
#         return Response(serializer.data)


#     def open_adjacent_cells(self, game, row, col):
#         # Открываем ячейки рядом с указанной, если они не заняты минами
#         # Рекурсивно открываем смежные ячейки с нулевым значением
#         field = game.field
#         if field[row][col] == '0':
#             for i in range(max(0, row - 1), min(row + 2, game.height)):
#                 for j in range(max(0, col - 1), min(col + 2, game.width)):
#                     if field[i][j] == ' ':
#                         field[i][j] = self.get_adjacent_mines_count(game, i, j)
#                         if field[i][j] == '0':
#                             self.open_adjacent_cells(game, i, j)
#                     elif field[i][j].isdigit():
#                         field[i][j] = field[i][j]
#         else:
#             field[row][col] = self.get_adjacent_mines_count(game, row, col)

#         game.save()
class TurnAPIView(APIView):
    def post(self, request):
        game_id = request.data.get('game_id')
        row = int(request.data.get('row'))
        col = int(request.data.get('col'))
        
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
        
        # Если это первый ход, размещаем мины
        if not game.field:
            game.initialize_game()
            game.place_mines(row, col)  # Размещаем мины после первого хода
        
        # Проверяем, что в указанной ячейке нет мины
        if game.field[row][col] == 'X':
            game.completed = True
            game.save()
            return Response({'message': 'Игра завершена. Вы попали на мину!', 'field': game.field}, status=status.HTTP_200_OK)
        
        # Открываем ячейки рядом с указанной
        self.open_adjacent_cells(game, row, col)
        
        # Проверяем, завершена ли игра
        if self.check_game_completed(game):
            game.completed = True
            game.save()
            return Response({'message': 'Игра завершена. Вы открыли все ячейки, не занятые минами!', 'field': game.field}, status=status.HTTP_200_OK)
        
        # Возвращаем обновленные данные об игре
        serializer = GameSerializer(game)
        return Response(serializer.data)
    
    def open_adjacent_cells(self, game, row, col):
        # Открываем ячейки рядом с указанной, если они не заняты минами
        # Рекурсивно открываем смежные ячейки с нулевым значением
        field = game.field
        if field[row][col] == '0':
            for i in range(max(0, row - 1), min(row + 2, game.height)):
                for j in range(max(0, col - 1), min(col + 2, game.width)):
                    if field[i][j] == ' ':
                        field[i][j] = self.get_adjacent_mines_count(game, i, j)
                        if field[i][j] == '0':
                            self.open_adjacent_cells(game, i, j)
                    elif field[i][j].isdigit():
                        field[i][j] = field[i][j]
        else:
            field[row][col] = self.get_adjacent_mines_count(game, row, col)

        game.field = field  # Обновляем поле игры
        game.save()


    def get_adjacent_mines_count(self, game, row, col):
        # Возвращает количество мин в смежных ячейках
        count = 0
        field = game.field
        for i in range(max(0, row - 1), min(row + 2, game.height)):
            for j in range(max(0, col - 1), min(col + 2, game.width)):
                if field[i][j] == 'X':
                    count += 1
        return str(count)

    def check_game_completed(self, game):
        # Проверяем, завершена ли игра (все не мины открыты)
        field = game.field
        for row in field:
            for cell in row:
                if cell == ' ':
                    return False
        return True