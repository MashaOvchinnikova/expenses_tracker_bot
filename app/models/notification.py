from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core import Base, NotificationType, NotificationPriority, NotificationCategory
from app.models import User, Expense, Budget

class Notification(Base):
    """
    Модель уведомления
    """
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    type: Mapped[NotificationType] = mapped_column(default=NotificationType.INFO)
    priority: Mapped[NotificationPriority] = mapped_column(default=NotificationPriority.LOW)
    category: Mapped[NotificationCategory]
    title: Mapped[str]
    message: Mapped[str]

    is_read: Mapped[bool] = mapped_column(default=False)
    is_delivered: Mapped[bool] = mapped_column(default=False)
    delivered_at: Mapped[datetime | None]
    read_at: Mapped[datetime | None]

    expense_id: Mapped[int] = mapped_column(
        ForeignKey("expenses.id", ondelete="SET NULL"),
        nullable=True
    )

    budget_id: Mapped[int] = mapped_column(
        ForeignKey("budgets.id", ondelete="SET NULL"),
        nullable=True
    )

    user: Mapped[User] = relationship("User", back_populates="notifications")
    expense: Mapped[Expense | None] = relationship("Expense")
    budget: Mapped[Budget | None] = relationship("Budget")

    def __repr__(self) -> str:
        return f"<Notification {self.type}: {self.title}>"

    @property
    def age_minutes(self) -> int:
        delta = datetime.utcnow() - self.created_at
        return int(delta.total_seconds() / 60)