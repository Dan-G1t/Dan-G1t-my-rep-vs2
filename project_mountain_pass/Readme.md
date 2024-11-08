# REST API для мобильного приложения ФСТР

## Описание
Этот REST API разработан для упрощения процесса подачи данных о горных перевалах туристами. Оно позволяет пользователям отправлять информацию о перевалах, а модераторам верифицировать и обрабатывать эти данные.

## Начало работы

### Предварительные требования
- Python (v3.6 или выше)
- Django (v3.0 или выше)
- Django REST Framework
- PostgreSQL

### Установка
1. Клонируйте репозиторий и перейдите в директорию проекта:
   git clone 
   cd project_mountain_pass

2. Создайте виртуальное окружение и активируйте его: 
   python -m venv venv
   source venv/bin/activate  # Для Linux/Mac
   venv\Scripts\activate  # Для Windows

3. Установите зависимости:
   pip install -r requirements.txt

4. Настройте базу данных:
   - Убедитесь, что у вас установлен PostgreSQL.
   - Создайте базу данных с именем `db_mountain_pass`.
   - Обновите переменные среды в файле `.env`:
     SECRET_KEY=<ваш_секретный_ключ>
     DB_USER=<имя_пользователя_бд>
     DB_PASSWORD=<пароль_пользователя_бд>
     DB_HOST=<адрес_бд>
     DB_PORT=<порт_бд>

5. Примените миграции:
   python manage.py migrate

6. Запустите сервер:
   python manage.py runserver


## Конфигурация

### Настройки

Проект использует следующие настройки в `settings.py`:
- `AUTH_USER_MODEL`: задан для использования кастомной модели пользователя `CustomUser`.

## Эндпоинты API

### 1. Создание нового перевала

- **URL**: `/submit_data/`
- **Метод**: `POST`
- **Тело запроса**:
 {
      "beauty_title": "пер. ",
      "title": "Пхия",
      "other_titles": "Триев",
      "connect": "Абишира-Ахуба и Аркасара",

      "add_time": "2021-09-22 13:18:13",
      "user": {
          "email": "user@example.com",
          "fam": "Фамилия",
          "name": "Имя",
          "otc": "Отчество",
          "phone": "1234567890"
      },
      "coords": {
          "latitude": 45.3842,
          "longitude": 7.1525,
          "height": 1200
      },
      "level": {
          "winter": "Сложность зимой",
          "summer": "Сложность летом",
          "autumn": "Сложность осенью",
          "spring": "Сложность весной"
      },
      "images": [
          {
              "data": "файл_изображения",
              "title": "Изображение 1"
          }
      ]
  }

- **Ответ**:
  {
      "status": 200,
      "message": null,
      "id": 1
  }

  ### 2. Получение перевала по ID

- **URL**: `/submit_data/<id>/`
- **Метод**: `GET`
- **Ответ**:
  {
      "beauty_title": "пер. ",
      "title": "Пхия",
      ...
  }

### 3. Редактирование перевала

- **URL**: `/submit_data/<id>/edit/`
- **Метод**: `PATCH`
- **Тело запроса**: (обновите только необходимые поля)
  {
      "title": "Обновленный перевал"
  }

  - **Ответ**:
  {
      "state": 1,
      "message": "Успешно обновлено."
  }

  ### 4. Получение перевалов пользователя по email

- **URL**: `/user_passes/`
- **Метод**: `GET`
- **Параметр запроса**: `user__email`
- **Ответ**:
  [
      {
          "beauty_title": "пер. ",
          "title": "Пхия",
          ...
      }
  ]


### Тесты
В проекте реализованы следующие тесты:

1. **Тестирование моделей**
   - `CustomUserModelTest`: Проверяет создание пользователя.
   - `CoordinatesModelTest`: Проверяет создание координат.
   - `LevelModelTest`: Проверяет создание уровня.
   - `PassModelTest`: Проверяет создание перевала.
   - `ImageModelTest`: Проверяет создание изображения.

2. **Тестирование API**
   - `PassAPITest`: Тестирует создание перевала и получение перевала по ID.
     - В тестах для создания перевала используется заранее определенный пользователь и координаты.
     - Тест API отправляет список изображений вместе с данными перевала.

### Пример тестов
Ниже описаны основные тесты API:

- **Создание перевала**: Тест проверяет успешное создание перевала с необходимыми данными. 
- **Получение перевала по ID**: Тест проверяет успешный запрос и правильные данные при получении перевала по его ID.

Каждый тест регистрирует статус ответа и проверяет, что созданный перевал действительно существует и к нему можно получить доступ.