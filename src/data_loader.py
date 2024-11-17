import json
import os

from src.product_and_category import Category, Product


def load_data_from_json(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    categories = []
    for category_data in data:
        products = [
            Product(
                name=product["name"],
                description=product["description"],
                price=product["price"],
                quantity=product["quantity"],
            )
            for product in category_data["products"]
        ]

        category = Category(name=category_data["name"], description=category_data["description"], products=products)

        categories.append(category)

    return categories


# if __name__ == "__main__":
#     base_dir = os.path.dirname(os.path.dirname(__file__))
#     json_file_path = os.path.join(base_dir, "data", "products.json")
#
#     categories = load_data_from_json(json_file_path)
#
#     for category in categories:
#         print(f"Категория: {category.name}")
#         print(f"Описание: {category.description}")
#         print("Продукты:")
#         print(category.products)  # Теперь правильно обращаемся к строке продуктов
#         print()
