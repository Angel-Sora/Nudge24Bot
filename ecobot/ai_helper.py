import google.generativeai as genai
from config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

def generate_task(mood_score, profession, goal):
    """Генерируем одно простое действие на основе настроения"""
    
    if mood_score >= 8:
        prompt = f"""
        Пользователь — {profession}. Его цель: {goal}.
        Настроение сегодня: {mood_score}/10 (отлично).
        Придумай ОДНО короткое действие (1-2 минуты), которое поможет:
        - Закрепить хорошее состояние
        - Сделать маленький шаг к цели
        Дай ответ в формате: "🔥 [название] — [описание действия]"
        """
    elif mood_score >= 5:
        prompt = f"""
        Пользователь — {profession}. Его цель: {goal}.
        Настроение сегодня: {mood_score}/10 (средне).
        Придумай ОДНО простое действие (1-2 минуты), которое:
        - Немного поднимет энергию
        - Не требует усилий
        Дай ответ в формате: "🌿 [название] — [описание действия]"
        """
    else:
        prompt = f"""
        Пользователь — {profession}. Его цель: {goal}.
        Настроение сегодня: {mood_score}/10 (низкое).
        Придумай ОДНО супер-лёгкое действие (30 секунд), которое:
        - Не требует вставания с места
        - Успокаивает
        Дай ответ в формате: "🫂 [название] — [описание действия]"
        """
    
    response = model.generate_content(prompt)
    return response.text.strip()