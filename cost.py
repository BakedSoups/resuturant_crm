from sqlalchemy.orm import Session
from models import MenuItemPricing, MenuRecipe, Ingredient

def calculate_item_cost(session: Session, menu_item_name: str) -> float:
    """Return current ingredient and labor costs without saving any changes."""
    menu_item = session.query(MenuItemPricing).filter_by(name=menu_item_name).first()
   
    if menu_item is None:
        raise ValueError(f"Menu item not found: {menu_item_name}")

    available_recipe = (
        session.query(MenuRecipe).filter_by(menu_item_name=menu_item_name).all()
    )

    if not available_recipe:
        raise ValueError(f"No recipe found for {menu_item_name}")

    total_ingredient_cost = 0.0

    for recipe in available_recipe:
        ingredient = session.query(Ingredient).filter_by(name=recipe.name).first()
        if ingredient is None:
            raise ValueError(f"Missing ingredient: {recipe.name}")
        total_ingredient_cost += ingredient.price_per_pound * recipe.quantity_pounds
    
    return total_ingredient_cost + menu_item.labor_cost
