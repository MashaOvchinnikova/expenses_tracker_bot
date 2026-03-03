from enum import Enum, IntEnum
from typing import List


# Категории расходов
class ExpenseCategory(str, Enum):
    """
    Категории расходов пользователя.
    Используем str, чтобы в БД сохранялось строковое значение.
    """
    FOOD = "еда"
    TRANSPORT = "транспорт"
    ENTERTAINMENT = "развлечения"
    HEALTH = "здоровье"
    SHOPPING = "покупки"
    UTILITIES = "коммунальные"
    COMMUNICATION = "связь"
    CREDITS = "кредиты"
    EDUCATION = "образование"
    GIFTS = "подарки"
    TRAVEL = "путешествия"
    CLOTHES = "одежда"
    CAFE = "кафе"
    SPORT = "спорт"
    TAXES = "налоги"
    REPAIRS = "ремонт"
    OTHER = "прочее"

    @classmethod
    def get_defaults(cls) -> List['ExpenseCategory']:
        """Категории по умолчанию для нового пользователя"""
        return [
            cls.FOOD,
            cls.TRANSPORT,
            cls.ENTERTAINMENT,
            cls.HEALTH,
            cls.SHOPPING,
            cls.OTHER
        ]

# Типы уведомлений
class NotificationType(str, Enum):
    """
    Типы уведомлений для пользователя.
    Определяет, зачем было отправлено уведомление.
    """
    # Бюджет и лимиты
    BUDGET_EXCEEDED = "budget_exceeded"  # Превышен бюджет категории
    MONTHLY_LIMIT = "monthly_limit"  # Приближение к лимиту месяца
    DAILY_LIMIT = "daily_limit"  # Превышен дневной лимит

    # Отчеты и статистика
    DAILY_REPORT = "daily_report"  # Ежедневный отчет
    WEEKLY_REPORT = "weekly_report"  # Еженедельный отчет
    MONTHLY_REPORT = "monthly_report"  # Ежемесячный отчет

    # Напоминания
    REMINDER = "reminder"  # Напоминание о записи расходов
    REGULAR_EXPENSE = "regular_expense"  # Обычный расход (аренда, кредит)

    # Системные
    WELCOME = "welcome"  # Приветственное сообщение
    HELP = "help"  # Ответ на /help
    ERROR = "error"  # Ошибка в работе
    INFO = "info"  # Информационное сообщение

    @classmethod
    def get_priority(cls, notification_type: 'NotificationType') -> int:
        """
        Приоритет уведомления (1 - высокий, 3 - низкий)
        Высокоприоритетные показываем сразу, низкие можно собрать в дайджест
        """
        priority_map = {
            cls.BUDGET_EXCEEDED: 1,
            cls.ERROR: 1,
            cls.DAILY_LIMIT: 1,
            cls.WELCOME: 1,

            cls.MONTHLY_LIMIT: 2,
            cls.REMINDER: 2,

            cls.DAILY_REPORT: 3,
            cls.WEEKLY_REPORT: 3,
            cls.MONTHLY_REPORT: 3,
            cls.INFO: 3,
        }
        return priority_map.get(notification_type, 3)

    @classmethod
    def needs_immediate_delivery(cls, notification_type: 'NotificationType') -> bool:
        """Нужно ли отправить сразу (true) или можно в дайджесте (false)"""
        return cls.get_priority(notification_type) == 1


# Срочность уведомлений
class NotificationPriority(IntEnum):
    """
    Приоритет уведомления (числовой, чтобы сортировать)
    """
    CRITICAL = 1  # Критическое (превышение бюджета)
    HIGH = 2  # Высокий (напоминание о платеже)
    LOW = 3  # Низкий (еженедельный отчет)


# ---- Категории уведомлений для группировки ----

class NotificationCategory(str, Enum):
    """
    Категории уведомлений для группировки в интерфейсе
    """
    BUDGET = "budget"  # Бюджет и финансы
    REPORTS = "reports"  # Отчеты и статистика
    REMINDERS = "reminders"  # Напоминания
    SYSTEM = "system"  # Системные

    @classmethod
    def get_category(cls, notif_type: NotificationType) -> 'NotificationCategory':
        """Определить категорию по типу уведомления"""
        mapping = {
            NotificationType.BUDGET_EXCEEDED: cls.BUDGET,
            NotificationType.MONTHLY_LIMIT: cls.BUDGET,
            NotificationType.DAILY_LIMIT: cls.BUDGET,

            NotificationType.DAILY_REPORT: cls.REPORTS,
            NotificationType.WEEKLY_REPORT: cls.REPORTS,
            NotificationType.MONTHLY_REPORT: cls.REPORTS,

            NotificationType.REMINDER: cls.REMINDERS,
            NotificationType.REGULAR_EXPENSE: cls.REMINDERS,
        }
        return mapping.get(notif_type, cls.SYSTEM)


# Язык пользователя
class UserLanguage(str, Enum):
    """
    Язык интерфейса пользователя
    """
    RU = "ru"
    EN = "en"

    @classmethod
    def get_supported(cls) -> List[str]:
        """Список поддерживаемых языков"""
        return [lang.value for lang in cls]


# Валюта
class Currency(str, Enum):
    """
    Валюта для отображения
    """
    RUB = "RUB"
    USD = "USD"

    def get_symbol(self) -> str:
        """Получить символ валюты"""
        symbols = {
            Currency.RUB: "р",
            Currency.USD: "$",
        }
        return symbols.get(self, self.value)

    def get_decimal_places(self) -> int:
        """Количество знаков после запятой"""
        return 2 if self is Currency.USD else 0


# Период для отчетов
class ReportPeriod(str, Enum):
    """
    Период для формирования отчетов
    """
    DAY = "day"
    WEEK = "week"
    MONTH = "month"
    YEAR = "year"

    def get_russian(self) -> str:
        """Русское название периода"""
        names = {
            ReportPeriod.DAY: "день",
            ReportPeriod.WEEK: "неделя",
            ReportPeriod.MONTH: "месяц",
            ReportPeriod.YEAR: "год",
        }
        return names.get(self, self.value)


# Статус бюджета
class BudgetStatus(str, Enum):
    """
    Статус выполнения бюджета
    """
    OK = "ok"  # В пределах бюджета
    WARNING = "warning"  # Израсходовано > 50%
    CRITICAL = "critical"  # Израсходовано > 80%
    EXCEEDED = "exceeded"  # Превышен

    @classmethod
    def from_spent_percentage(cls, percentage: float) -> 'BudgetStatus':
        """
        Определить статус по проценту израсходованного бюджета
        """
        if percentage >= 100:
            return cls.EXCEEDED
        elif percentage >= 80:
            return cls.CRITICAL
        elif percentage >= 50:
            return cls.WARNING
        else:
            return cls.OK