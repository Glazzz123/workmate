# Workmate

Workmate — это Python-утилита для работы с логами и генерацией отчётов.  
Проект включает основной скрипт, тесты, примеры логов и отчёт в формате JSON.

---

## 📦 Установка

```bash
# Клонируем репозиторий
git clone https://github.com/username/workmate.git
cd workmate

# Создаём виртуальное окружение (опционально)
python -m venv venv
source venv/bin/activate   # Linux / macOS
venv\Scripts\activate      # Windows

# Устанавливаем зависимости
pip install -r requirements.txt
```

---

## ▶️ Запуск

```bash
python workmate/main.py
```

В процессе выполнения создаются:
- Логи (см. директорию `logs/`)
- Отчёт в формате JSON (`report.json`)

---

## 🧪 Тестирование

```bash
pytest tests/
```

---

## 📂 Структура проекта

```
workmate/
├── workmate/
│   ├── main.py          # основной скрипт
│   ├── report.json      # пример отчёта
│   ├── requirements.txt # зависимости
│   ├── logs/            # примеры логов
│   └── tests/           # тесты
```

---

## 🔧 Использование

1. Поместите нужные входные данные в папку `logs/`.
2. Запустите `main.py`.
3. Проверьте результаты в `report.json`.

---

## 🚀 TODO / Улучшения

- [ ] Добавить CLI-аргументы для управления запуском  
- [ ] Расширить тестовое покрытие  
- [ ] Поддержка разных форматов отчётов (CSV, HTML)  

---

## 📜 Лицензия

MIT License © 2025  
