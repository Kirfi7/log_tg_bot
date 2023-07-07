scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets",
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

access = {1831358099, 777198928, 1174671150, 1634625613}

token = "6133560304:AAGKJFWkCyRroXfd0YYNYl9meIj3ierGv-s"

req_types = {
    'Джаилы': {"description": "Посадил", "category": 41},
    'Муты': {"description": "Выдал мут", "category": 41},
    'Кики': {"description": "Кикнул", "category": 41},
    'Мероприятия': {"description": "Создал мероприятие", "category": 41},
    'Репорты': {"description": "(Вопрос:", "category": 40},
    'Вопросы': {"description": "] ответ", "category": 40},
}

date_message = "Укажите дату, за которую вы хотите получить выгрузку\nФормат: день.месяц | Пример: 31.05"
logs_message = "Укажите дату, с которой начинается неделя\nФормат: день.месяц | Пример: 31.05"
datetime_message = "Укажите дату и время, за которые вы хотите получить выгрузку\nФормат: день.месяц час:минута | Пример: 31.05 23:59"
param_message = "Укажите параметры в следующем формате: первое_место вычет | Пример: 500 100"
