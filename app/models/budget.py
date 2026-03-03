from datetime import datetime, date

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core import Base, ReportPeriod, Currency
from app.models import User, Category


class Budget(Base):
    """
    Модель бюджета
    """
    __table_args__ = (
        UniqueConstraint('user_id', 'category_id', 'period_start', name='unique_budget_per_period'),
    )
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))
    category_id: Mapped[int] = mapped_column(ForeignKey('categories.id', ondelete='CASCADE'))

    period: Mapped[ReportPeriod] = mapped_column(default=ReportPeriod.MONTH)
    period_start: Mapped[date]
    period_end: Mapped[date]

    amount: Mapped[float]
    currency: Mapped[Currency] = mapped_column(default=Currency.RUB)

    notify_at: Mapped[int]
    last_notification_sent: Mapped[datetime | None]

    user: Mapped[User] = relationship(
        "User",
        back_populates="budgets"
    )
    category: Mapped[Category] = relationship(
        "Category",
        back_populates="budgets"
    )

    def __repr__(self) -> str:
        return f"<Budget {self.category.name}: {self.amount} for {self.period_start}>"

    @property
    def is_active(self) -> bool:
        return self.period_end >= date.today()

    @property
    def days_remaining(self) -> int:
        return (self.period_end - date.today()).days