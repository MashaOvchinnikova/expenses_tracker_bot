from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models import User, Category
from app.core import Base


class Expense(Base):
    """
    Модель расхода
    """
    amount: Mapped[float]
    description: Mapped[str | None]
    expense_date: Mapped[datetime] = mapped_column(default=datetime.now)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete="CASCADE"))
    category_id: Mapped[int] = mapped_column(ForeignKey('categories.id', ondelete="SET NULL"))

    user: Mapped[User] = relationship(
        "User",
        back_populates="expenses"
    )
    category: Mapped[Category] = relationship(
        "Category",
        back_populates="expenses")

    def __repr__(self) -> str:
        return f"<Expense {self.amount} - {self.expense_date}>"

    @property
    def category_type(self):
        """Получить тип категории расхода"""
        return self.category.type if self.category else None
