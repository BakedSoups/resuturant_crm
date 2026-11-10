from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from models import Base, Ingredient, MenuRecipe, MenuItemPricing, OrderedItem
from cost import calculate_item_cost


engine = create_engine("sqlite:///resutaurntcrm.db", echo=True)
Base.metadata.create_all(engine)

def add_ingredients(name, price_per_pound):
    with Session(engine) as session:
        ingredient = Ingredient(name=name, price_per_pound=price_per_pound)
        session.add(ingredient)
        session.commit()

def get_ingredients():
    with Session(engine) as session:
        return session.query(Ingredient).all()

def update_ingredient_price(name, new_price):
    with Session(engine) as session:
        ingredient = session.query(Ingredient).filter_by(name=name).first()
        if ingredient:
            ingredient.price_per_pound = new_price
            session.commit()
        else:
            raise ValueError(f"Ingredient not found: {name}")
        
def delete_ingredient(name):
    with Session(engine) as session: 
        ingredient = session.query(Ingredient).filter_by(name=name).first()
        if ingredient:
            session.delete(ingredient)
            session.commit()
        else:
            raise ValueError(f"Ingredient not found: {name}")


def add_menu_recipe(menu_item_name, ingredient_name, quantity_pounds):
    with Session(engine) as session:
        menu_recipe = MenuRecipe(
            menu_item_name=menu_item_name,
            name=ingredient_name,
            quantity_pounds=quantity_pounds
        )
        session.add(menu_recipe)
        session.commit()

def get_menu_recipes(menu_item_name):
    with Session(engine) as session:
        return session.query(MenuRecipe).filter_by(menu_item_name=menu_item_name).all()

    

def add_menu_item_pricing(menu_item_name, price, labor_cost):
    with Session(engine) as session:
        menu_item_pricing = MenuItemPricing(
            name=menu_item_name,
            price=price,
            labor_cost=labor_cost
        )
        session.add(menu_item_pricing)
        session.commit()
def update_menu_item_pricing(menu_item_name, new_price, new_labor_cost):
    with Session(engine) as session:
        menu_item = session.query(MenuItemPricing).filter_by(name=menu_item_name).first()
        if menu_item:
            menu_item.price = new_price
            menu_item.labor_cost = new_labor_cost
            session.commit()
        else:
            raise ValueError(f"Menu item not found: {menu_item_name}")

def add_ordered_item(transaction_id, menu_item_name, unit_price):

    with Session(engine) as session:
        total_cost = calculate_item_cost(session, menu_item_name)
        ordered_item = OrderedItem(
            transaction_id=transaction_id,
            menu_item_name=menu_item_name,
            unit_price=unit_price,
            total_cost=total_cost
        )
        session.add(ordered_item)
        session.commit()





if __name__ == "__main__":
    # add ingredients
    # add_ingredients("Lettuce", 1.64)
    # add_ingredients("Tomato", 2.0)
    # add_ingredients("Hamburger Patty", 4.5)
    # add_ingredients("Bread", 1.2)

    # # add burger
    # Burger_recipe = [
    #     ("Burger", "Lettuce", 0.1),
    #     ("Burger", "Tomato", 0.2),
    #     ("Burger", "Hamburger Patty", 0.5),
    #     ("Burger", "Bread", 0.3)
    # ]

    # for menu_item_name, ingredient_name, quantity_pounds in Burger_recipe:
    #     add_menu_recipe(menu_item_name, ingredient_name, quantity_pounds)

    # avaiable_recipe = get_menu_recipes("Burger")
    # needed_ingredients = []

    # for recipe in avaiable_recipe:
    #     needed_ingredients.append((recipe.name, recipe.quantity_pounds))
    #     # print(f"Menu Item: {recipe.menu_item_name}, Ingredient: {recipe.name}, Quantity (pounds): {recipe.quantity_pounds}")
    # print(f"Ingredients needed for Burger:{needed_ingredients}")

    add_menu_item_pricing("Burger", 10.0, 2.0)
    add_ordered_item("TXN123", "Burger", 10.0)
    print("Ordered item added successfully.")

    all_ordered_items = []

    with Session(engine) as session:
        all_ordered_items = session.query(OrderedItem).all()

    pass
