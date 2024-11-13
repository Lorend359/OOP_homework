class Product:
    """Класс, представляющий продукт."""

    def __init__(self, name: str, description: str, price: float, quantity: int):
        """Инициализирует продукт с данными."""
        self.name = name
        self.description = description
        self.__price = price
        self._quantity = quantity

    @property
    def quantity(self):
        """Возвращает количество продукта."""
        return self._quantity

    @property
    def price(self):
        """Возвращает цену продукта."""
        return self.__price

    @price.setter
    def price(self, value: float):
        """Устанавливает новую цену продукта."""
        print(f"Попытка установить цену: {value}")
        if value <= 0:
            print("Цена не должна быть нулевой или отрицательной")
            return
        if value < self.__price:
            confirm = input("Вы действительно хотите понизить цену? (y/n): ")
            if confirm.lower() != "y":
                return
        self.__price = value

    @classmethod
    def new_product(cls, product_info: dict, existing_products: list = None):
        """Создает новый продукт или обновляет существующий."""
        name = product_info.get("name")
        description = product_info.get("description")
        price = product_info.get("price", 0.0)
        quantity = product_info.get("quantity", 0)

        if existing_products:
            for existing_product in existing_products:
                if existing_product.name == name:
                    existing_product._quantity += quantity
                    if price > existing_product.price:
                        existing_product.price = price
                    return existing_product

        new_product = cls(name, description, price, quantity)
        if existing_products is not None:
            existing_products.append(new_product)
        return new_product


class Category:
    """Класс, представляющий категорию продуктов."""

    category_count = 0
    total_product_count = 0

    def __init__(self, name: str, description: str, products: list = None):
        """Инициализирует категорию с данными."""
        self.name = name
        self.description = description
        self._products = products if products is not None else []
        Category.category_count += 1

    def add_product(self, product: Product):
        """Добавляет продукт в категорию."""
        self._products.append(product)
        Category.total_product_count += 1

    @property
    def products(self):
        """Возвращает строку с продуктами в категории."""
        return "\n".join(
            f"{product.name}, {product.price} руб. Остаток: {product.quantity} шт." for product in self._products
        )

    @property
    def product_list(self):
        """Возвращает список всех продуктов в категории."""
        return self._products

    @property
    def product_count(self):
        """Возвращает количество продуктов в категории."""
        return len(self._products)


# if __name__ == "__main__":
#     product1 = Product("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5)
#     product2 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
#     product3 = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)
#
#     category1 = Category(
#         "Смартфоны",
#         "Смартфоны, как средство не только коммуникации, но и получения дополнительных функций для удобства жизни",
#         [product1, product2, product3]
#     )
#
#     print(category1.products)
#     product4 = Product("55\" QLED 4K", "Фоновая подсветка", 123000.0, 7)
#     category1.add_product(product4)
#     print(category1.products)
#     print(category1.product_count)
#
#     new_product = Product.new_product(
#         {"name": "Samsung Galaxy S23 Ultra", "description": "256GB, Серый цвет, 200MP камера", "price": 180000.0,
#          "quantity": 5})
#     print(new_product.name)
#     print(new_product.description)
#     print(new_product.price)
#     print(new_product.quantity)
#
#     new_product.price = 800
#     print(new_product.price)
#
#     new_product.price = -100
#     print(new_product.price)
#     new_product.price = 0
#     print(new_product.price)
