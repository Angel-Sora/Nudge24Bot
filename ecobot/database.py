import gspread
import json
import os
from oauth2client.service_account import ServiceAccountCredentials
from config import SPREADSHEET_ID

class SheetDB:
    def __init__(self):
        """Подключаемся к Google Sheets через Secrets"""
        creds_json = os.environ.get("CREDENTIALS_JSON")
        if not creds_json:
            raise Exception("❌ CREDENTIALS_JSON не найдена в Secrets! Добавь её в Replit Secrets.")
        
        creds_dict = json.loads(creds_json)
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
        self.client = gspread.authorize(creds)
        
        # Пытаемся открыть таблицу
        try:
            self.sheet = self.client.open_by_key(SPREADSHEET_ID).sheet1
            print("✅ Таблица найдена")
        except gspread.exceptions.SpreadsheetNotFound:
            print("⚠️ Таблица не найдена, создаю новую...")
            self.sheet = self.client.create("Nudge24Bot Data")
            print("✅ Новая таблица создана!")
        
        # 🔥 ГЛАВНОЕ ИСПРАВЛЕНИЕ: Проверяем и создаём заголовки ДО того, как бот попытается читать данные
        self._ensure_headers()

    def _ensure_headers(self):
        """Проверяет, есть ли заголовки. Если таблица пустая - создаёт их."""
        try:
            # Пробуем получить все записи (чтобы проверить, есть ли хоть что-то)
            all_data = self.sheet.get_all_values()
            
            # Если таблица полностью пустая (даже заголовков нет)
            if not all_data:
                print("⚠️ Таблица пустая, создаю заголовки...")
                headers = [
                    "user_id", "username", "profession", "goal", 
                    "time_available", "morning_mood", "morning_time", 
                    "evening_mood", "evening_time", "task_completed", 
                    "current_task", "registered_at"
                ]
                self.sheet.insert_row(headers, 1)
                print("✅ Заголовки созданы!")
                return
            
            # Проверяем первую строку (она должна быть заголовком)
            first_row = all_data[0]
            # Если первая ячейка НЕ user_id, значит заголовков нет
            if not first_row or first_row[0] != "user_id":
                print("⚠️ Нет правильных заголовков, добавляю...")
                headers = [
                    "user_id", "username", "profession", "goal", 
                    "time_available", "morning_mood", "morning_time", 
                    "evening_mood", "evening_time", "task_completed", 
                    "current_task", "registered_at"
                ]
                # Если в первой строке есть какие-то данные, сдвигаем их вниз
                if first_row:
                    self.sheet.insert_row(headers, 1)
                else:
                    self.sheet.insert_row(headers, 1)
                print("✅ Заголовки добавлены!")
            else:
                print("✅ Заголовки уже есть")
                
        except Exception as e:
            print(f"⚠️ Критическая ошибка при создании заголовков: {e}")
            # Пробуем создать с нуля, если всё сломалось
            try:
                headers = [
                    "user_id", "username", "profession", "goal", 
                    "time_available", "morning_mood", "morning_time", 
                    "evening_mood", "evening_time", "task_completed", 
                    "current_task", "registered_at"
                ]
                self.sheet.insert_row(headers, 1)
                print("✅ Заголовки созданы принудительно!")
            except:
                print("❌ Не удалось создать заголовки. Проверь права доступа к таблице.")

    def get_user_data(self, user_id):
        """Получаем данные пользователя. Если таблица пустая - возвращаем None."""
        try:
            # Безопасно получаем все записи
            all_records = self.sheet.get_all_records()
            if not all_records:
                return None
            for record in all_records:
                if str(record.get("user_id", "")) == str(user_id):
                    return record
            return None
        except Exception as e:
            print(f"⚠️ Ошибка получения данных: {e}")
            return None

    def add_user(self, user_id, username, profession, goal, time_available):
        """Добавляем нового пользователя"""
        import datetime
        
        # Проверяем, есть ли уже такой пользователь
        existing = self.get_user_data(user_id)
        if existing:
            return True
        
        row = [
            str(user_id), username or "", profession or "", goal or "", 
            time_available or "", "", "", "", "", "", 
            datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ]
        self.sheet.append_row(row)
        print(f"✅ Пользователь {user_id} добавлен")
        return True

    def _find_user_row(self, user_id):
        """Ищем номер строки пользователя"""
        try:
            user_ids = self.sheet.col_values(1)
            for i, uid in enumerate(user_ids, start=1):
                if str(uid) == str(user_id):
                    return i
            return None
        except Exception as e:
            print(f"❌ Ошибка поиска: {e}")
            return None

    def save_mood(self, user_id, mood, time_of_day):
        try:
            row_num = self._find_user_row(user_id)
            if not row_num:
                self.add_user(user_id, "", "дизайнер", "повысить продуктивность", "")
                row_num = self._find_user_row(user_id)
                if not row_num:
                    return False
            
            if time_of_day == "morning":
                self.sheet.update_cell(row_num, 6, mood)
                self.sheet.update_cell(row_num, 7, "=NOW()")
            elif time_of_day == "evening":
                self.sheet.update_cell(row_num, 8, mood)
                self.sheet.update_cell(row_num, 9, "=NOW()")
            return True
        except Exception as e:
            print(f"❌ Ошибка сохранения настроения: {e}")
            return False

    def save_task_result(self, user_id, completed):
        try:
            row_num = self._find_user_row(user_id)
            if not row_num:
                return False
            value = "Да" if completed else "Нет"
            self.sheet.update_cell(row_num, 10, value)
            return True
        except Exception as e:
            print(f"❌ Ошибка сохранения результата: {e}")
            return False

    def save_current_task(self, user_id, task):
        try:
            row_num = self._find_user_row(user_id)
            if not row_num:
                return False
            self.sheet.update_cell(row_num, 11, task)
            return True
        except Exception as e:
            print(f"❌ Ошибка сохранения задания: {e}")
            return False

    def get_all_users(self):
        try:
            return self.sheet.get_all_records()
        except Exception as e:
            print(f"❌ Ошибка получения списка: {e}")
            return []

    def update_user_field(self, user_id, field_name, value):
        try:
            headers = self.sheet.row_values(1)
            if field_name not in headers:
                return False
            col_num = headers.index(field_name) + 1
            row_num = self._find_user_row(user_id)
            if not row_num:
                return False
            self.sheet.update_cell(row_num, col_num, value)
            return True
        except Exception as e:
            print(f"❌ Ошибка обновления поля: {e}")
            return False
