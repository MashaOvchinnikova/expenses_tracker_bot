from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core import Base, Currency, ExpenseCategory
from app.models import User, Expense, Budget

class Category(Base):
    """
    Модель категории расходов
    """
    __table_args__ = (
        UniqueConstraint('user_id', 'name', name='unique_category_per_user'),
    )
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    name: Mapped[str]
    type: Mapped[ExpenseCategory] = mapped_column(default=ExpenseCategory.FOOD)
    monthly_budget: Mapped[float | None]
    currency: Mapped[Currency] = mapped_column(default=Currency.RUB)
    is_default: Mapped[bool] = mapped_column(default=False)
    is_custom: Mapped[bool] = mapped_column(default=False)

    user = Mapped[User] = relationship(
        "User",
        back_populates="categories"
    )
    expenses: Mapped[list[Expense]] = relationship("Expense", back_populates="category")
    budgets: Mapped[list[Budget]] = relationship("Budget", back_populates="category")

    def __repr__(self) -> str:
        return f"<Category {self.name} - user:{self.user_id}>"

    @property
    def display_name(self) -> str:
        return self.name




