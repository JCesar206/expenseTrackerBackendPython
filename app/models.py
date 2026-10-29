from datetime import datetime
from sqlalchemy import (Boolean, DateTime, ForeignKey, Integer, Numeric, String, UniqueConstraint, func)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass
class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True
    )
    email: Mapped[str] = mapped_column(
        String(255), unique=True, index=True, nullable=False
    )
    password_hash: Mapped[str] = mapped_column(
        String(255), nullable=False
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean, default=True, nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False
    )

class Category(Base):
    __tablename__ = "categories"
    __table_args__ = (
        UniqueConstraint("user_id", "name", "kind"),
    )
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True
    )
    name: Mapped[str] = mapped_column(
        String(100), nullable=False
    )
    kind: Mapped[str] = mapped_column(
        String(10), nullable=False
    )
    user_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=True,
    )

class Transaction(Base):
    __tablename__ = "transactions"
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True
    )
    description: Mapped[str] = mapped_column(
        String(255), nullable=False
    )
    amount: Mapped[float] = mapped_column(
        Numeric(12, 2), nullable=False
    )
    kind: Mapped[str] = mapped_column(
        String(10), nullable=False
    )
    transaction_date: Mapped[datetime] = mapped_column(
        DateTime, nullable=False
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    category_id: Mapped[int | None] = mapped_column(
        ForeignKey("categories.id", ondelete="SET NULL"),
        nullable=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False
    )