***Тестовое задание - Игра Сапёр (Minesweeper) (веб-сервер с REST API)**. 


**Описание**
На основе предоставленной спецификации раализована логика веб-сервера с REST API для игры "Сапер".
В базе данных имеется модель игры Game, в которой хранятся данные о поле, количестве и размещении мин, вносятся изменения при ходе игрока.

Конечные точки:
- http://127.0.0.1:8000/new (создание новой игры)

Создается новая запись об игре, проверяется, что введеные пользователей данные сооветсвуют ограничениям по размерам игрового поля и количеству мин. Мины расставляются на поле в случайном порядке. Возвращаются данные об игре в соовествии со спецификацией.

- http://127.0.0.1:8000/turn (обработка хода пользователя)

Реализовано изменение игрового поля на основе переданных данных пользователем - 'открытие ячек поля'. 
Проверка данных: игра с таким индентификатором существует, игра не завершена, ячека уже была открыта, о том, что в ячейке нет мины.
Открытие ячейки приводит к иммению данных об игровом поле.
Игра завершается, если пользователь 'нажал' на мины или открыл все ячейки не занятые минами.

Добавлен Docker для удобного тестирования, суперпользователь создается при сборке образа.

[Спецификация:](https://minesweeper-test.studiotg.ru/swagger/)

#### Стек
Стандартные библиотеки Python.
Django
Django REST framework


#### Запуск приложения.

Клонируйте репозиторий и перейдите в каталог проекта.

#### В коробке через Docker

Запускаем:

`docker-compose up`

После запуска контейнеров тестируем по [адресу](https://minesweeper-test.studiotg.ru/)

В поле 'URL API (можно относительный путь)' передаем: 
http://127.0.0.1:8000