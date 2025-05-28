# 🌤️ Weather Forecast Web App

Веб-приложение для получения прогноза погоды по городам с автодополнением, историей поиска и статистикой. Данные прогноза берутся из OpenWeatherMap API. Реализована поддержка авторизованных и неавторизованных пользователей, история поиска сохраняется в базу данных.

---

## 🚀 Технологии

* **Python 3.12**
* **Django 5**
* **Django REST Framework** — для API
* **Swagger** - для документации API
* **PostgreSQL** — хранение пользователей, истории и городов
* **Docker + Docker Compose** — контейнеризация
* **Bootstrap 5** — для "фронтенда"
* **GeoNames** — данные о городах (TSV-файл)

---

## 📦 Как запустить

### 1. Клонировать репозиторий

```bash
git clone https://github.com/Pu104ver/weather.git
cd weather
```

### 2. Получи API ключ OpenWeatherMap

Зарегестируйся на сайте [OWM](https://home.openweathermap.org/users/sign_up), после чего в [профиле](https://home.openweathermap.org/api_keys) создай новый API ключ.

```
weather-app/
└── data/
    └── cities.tsv
```

> ⚠️ Файл должен быть в формате TSV с заголовками, подходящими для модели `City`.

---

### 3. Создать `.env` файл

Создайте `.env` на основе `.env_example` и укажите ключи:

```
DEBUG=True
SECRET_KEY='SECRET_KEY'
DB_NAME=your_weather_db
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
WEATHER_API_KEY=API_KEY
ALLOWED_HOSTS="0.0.0.0,127.0.0.1"
```

---

### 4. Построить и запустить контейнеры

```bash
docker compose build
docker compose up
```

---

### 5. Импорт городов и создание супер-пользователя

Для работы автоподсказок требуется наличие городов в БД. Для этого после запуска проекта через докер можно воспользоваться следующей командой:

```bash
docker-compose.exe exec web python manage.py load_cities data/cities500.txt
```

Чтобы получить доступ к админ-панели, нужно создать супер-пользователя:

```bash
docker-compose.exe exec web python manage.py createsuperuser
```

---

### 6. Готово!

Приложение будет доступно по адресу:

📍 [http://127.0.0.1:8000](http://127.0.0.1:8000/)

Админ-панель и сваггер доступны по соответсвующим адресам:

🖥️[http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

🖥️[http://127.0.0.1:8000/api/swagger/](http://127.0.0.1:8000/api/swagger/)

---

## 📚 Полезные команды

Очистка старых Docker-образов:

```bash
docker system prune -a
```

Остановка контейнеров:

```bash
docker compose down
```

Тесты:

```bash
docker-compose.exe exec web pytest
```

---

## 📌Что было сделано

* Реализована регистрация и поиск городов с автодополнением
* Сохраняется история и статистика поиска
* Поддержка авторизации
* Контейнеризация с помощью Docker
* Импорт данных о городах из GeoNames

---



## 📝 Лицензия

MIT — используй проект, как хочешь.
