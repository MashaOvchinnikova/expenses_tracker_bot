"""
Инициализация моделей для удобного импорта
"""
from app.models.user import User
from app.models.category import Category
from app.models.expense import Expense
from app.models.budget import Budget
from app.models.notification import Notification

# Список всех моделей для Alembic
__all__ = [
    "User",
    "Category",
    "Expense",
    "Budget",
    "Notification"
]