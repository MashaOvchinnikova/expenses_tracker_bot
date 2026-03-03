from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core import Base, uniq_str_an, UserLanguage, Currency
from app.models import Expense, Budget, Notification, Category

class User(Base):
    """
    Модель пользователя с поддержкой JWT авторизации
    """
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False)

    # Личная информация
    username: Mapped[uniq_str_an]
    name: Mapped[str | None]
    surname: Mapped[str | None]

    #Авторизация по JWT токенам
    email: Mapped[uniq_str_an]
    password: Mapped[str]

    # Настройки
    language: Mapped[str] = mapped_column(default=UserLanguage.RU.value)
    currency: Mapped[str] = mapped_column(default=Currency.RUB.value)

    # Статус и роли
    is_active: Mapped[bool] = mapped_column(default=True)
    is_admin: Mapped[bool] = mapped_column(default=False)

    # Связи с другими таблицами
    categories: Mapped[list[Category]] = relationship(
        "Category",
        back_populates="user",
        cascade="all, delete-orphan"
    )
    expenses: Mapped[list[Expense]] = relationship (
        "Expense",
        back_populates="user",
        cascade="all, delete-orphan" # Удаляет расходы при удалении пользователя
    )
    budgets: Mapped[list[Budget]] = relationship(
        "Budget",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    notifications: Mapped[list[Notification]] = relationship(
        "Notification",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<User {self.id}: {self.email or self.telegram_id}>"