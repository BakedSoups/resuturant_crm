from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

# for inidivual ingredients 
class Ingredient(Base):
    __tablename__ = "ingredients"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    price_per_pound: Mapped[float]


# ingrdients needed for menu items(open to changing overtime)
class MenuRecipe(Base):
    __tablename__ = "menu_recipes"

    menu_item_name: Mapped[str] = mapped_column(
        ForeignKey("menu_items_pricing.name"), primary_key=True
    )
    name: Mapped[str] = mapped_column(
        ForeignKey("ingredients.name"), primary_key=True
    )
    quantity_pounds: Mapped[float]


    # recipe_line = session.get(
    # MenuRecipe, ("Burger", "Beef")
    # )
    # Lets Python access the associated MenuItemPricing object.
    # Example: recipe_line.menu_item.name -> "Burger"
    menu_item: Mapped["MenuItemPricing"] = relationship()
    ingredient: Mapped[Ingredient] = relationship()

# total value of price + laborcost
class MenuItemPricing(Base):
    __tablename__ = "menu_items_pricing"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    price: Mapped[float]
    labor_cost: Mapped[float]


class OrderedItem(Base):
    __tablename__ = "ordered_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    # Items purchased together share the same transaction ID.
    transaction_id: Mapped[str] = mapped_column(index=True)
    menu_item_name: Mapped[str] = mapped_column(ForeignKey("menu_items_pricing.name"))
    unit_price: Mapped[float]
    ordered_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    total_cost: Mapped[float] = mapped_column(default=0.0)

    menu_item: Mapped[MenuItemPricing] = relationship()
