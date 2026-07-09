import gspread
from oauth2client.service_account import ServiceAccountCredentials
from config import GSHEET_CREDENTIALS_FILE, SPREADSHEET_ID

class SheetDB:
    def __init__(self):
        """Подключаемся к Google Sheets"""
        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive"
        ]
        creds = ServiceAccountCredentials.from_json_keyfile_name(
            GSHEET_CREDENTIALS_FILE, scope
        )
        client = gspread.authorize(creds)
        self.sheet = client.open_by_key(SPREADSHEET_ID).sheet1
        
        # Проверяем, есть ли заголовки, если нет — создаём
        self._ensure_headers()

    def _ensure_headers(self):
        """Создаём заголовки, если таблица пустая"""
        try:
            # Пробуем прочитать первую строку
            headers = self.sheet.row_values(1)
            if not headers or len(headers) == 0:
                # Если пусто — пишем заголовки
                headers = [
                    "user_id",          # A
                    "username",         # B
                    "profession",       # C
                    "goal",             # D
                    "time_available",   # E
                    "morning_mood",     # F
                    "morning_time",     # G
                    "evening_mood",     # H
                    "evening_time",     # I
                    "task_completed",   # J
                    "current_task",     # K
                    "registered_at"     # L
                ]
                self.sheet.insert_row(headers, 1)
                print("✅ Заголовки таблицы созданы")
        except Exception as e:
            print(f"⚠️ Ошибка при создании заголовков: {e}")

    def add_user(self, user_id, username, profession, goal, time_available):
        """
        Добавляем нового пользователя в таблицу
        """
        import datetime
        
        row = [
            str(user_id),               # A: user_id
            username or "",             # B: username
            profession or "",           # C: profession
            goal or "",                 # D: goal
            time_available or "",       # E: time_available
            "",                         # F: morning_mood
            "",                         # G: morning_time
            "",                         # H: evening_mood
            "",                         # I: evening_time
            "",                         # J: task_completed
            "",                         # K: current_task
            datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # L: registered_at
        ]
        self.sheet.append_row(row)
        print(f"✅ Пользователь {user_id} добавлен в таблицу")

    def save_mood(self, user_id, mood, time_of_day):
        """
        Сохраняем настроение (утро/вечер)
        time_of_day: "morning" или "evening"
        """
        try:
            # Находим строку пользователя
            cell = self._find_user_row(user_id)
            if not cell:
                print(f"⚠️ Пользователь {user_id} не найден в таблице")
                return False
            
            row_num = cell
            
            if time_of_day == "morning":
                self.sheet.update_cell(row_num, 6, mood)      # колонка F
                self.sheet.update_cell(row_num, 7, "=NOW()")  # колонка G
                print(f"✅ Утреннее настроение {user_id}: {mood}")
            elif time_of_day == "evening":
                self.sheet.update_cell(row_num, 8, mood)      # колонка H
                self.sheet.update_cell(row_num, 9, "=NOW()")  # колонка I
                print(f"✅ Вечернее настроение {user_id}: {mood}")
            else:
                print(f"⚠️ Неизвестное время суток: {time_of_day}")
                return False
            
            return True
            
        except Exception as e:
            print(f"❌ Ошибка сохранения настроения: {e}")
            return False

    def save_task_result(self, user_id, completed):
        """
        Записываем, выполнил ли пользователь задание
        completed: True или False
        """
        try:
            row_num = self._find_user_row(user_id)
            if not row_num:
                print(f"⚠️ Пользователь {user_id} не найден")
                return False
            
            value = "Да" if completed else "Нет"
            self.sheet.update_cell(row_num, 10, value)  # колонка J
            print(f"✅ Результат задания {user_id}: {value}")
            return True
            
        except Exception as e:
            print(f"❌ Ошибка сохранения результата: {e}")
            return False

    def save_current_task(self, user_id, task):
        """
        Сохраняем текущее задание пользователя
        """
        try:
            row_num = self._find_user_row(user_id)
            if not row_num:
                print(f"⚠️ Пользователь {user_id} не найден")
                return False
            
            self.sheet.update_cell(row_num, 11, task)  # колонка K
            print(f"✅ Задание сохранено для {user_id}")
            return True
            
        except Exception as e:
            print(f"❌ Ошибка сохранения задания: {e}")
            return False

    def get_user_data(self, user_id):
        """
        Получаем все данные пользователя в виде словаря
        """
        try:
            all_records = self.sheet.get_all_records()
            for record in all_records:
                if str(record.get("user_id", "")) == str(user_id):
                    return record
            return None
        except Exception as e:
            print(f"❌ Ошибка получения данных пользователя: {e}")
            return None

    def get_all_users(self):
        """
        Получаем список всех пользователей
        """
        try:
            all_records = self.sheet.get_all_records()
            return all_records
        except Exception as e:
            print(f"❌ Ошибка получения списка пользователей: {e}")
            return []

    def _find_user_row(self, user_id):
        """
        Вспомогательный метод: ищем номер строки пользователя
        Возвращает номер строки (начиная с 1) или None
        """
        try:
            # Получаем все значения в колонке A (user_id)
            user_ids = self.sheet.col_values(1)
            for i, uid in enumerate(user_ids, start=1):
                if str(uid) == str(user_id):
                    return i
            return None
        except Exception as e:
            print(f"❌ Ошибка поиска пользователя: {e}")
            return None

    def update_user_field(self, user_id, field_name, value):
        """
        Универсальный метод обновления любого поля
        field_name: название колонки (как в заголовке)
        """
        try:
            # Маппинг названий колонок к номерам
            headers = self.sheet.row_values(1)
            if field_name not in headers:
                print(f"⚠️ Колонка '{field_name}' не найдена")
                return False
            
            col_num = headers.index(field_name) + 1
            row_num = self._find_user_row(user_id)
            
            if not row_num:
                print(f"⚠️ Пользователь {user_id} не найден")
                return False
            
            self.sheet.update_cell(row_num, col_num, value)
            print(f"✅ Поле '{field_name}' обновлено для {user_id}")
            return True
            
        except Exception as e:
            print(f"❌ Ошибка обновления поля: {e}")
            return False