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
            Category.total_product_count += quantity
        return new_product

    def __str__(self):
        """Строковое представление продукта."""
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."

    def __repr__(self):
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."

    def __add__(self, other):
        """Складывает стоимость текущего продукта с другим продуктом."""
        if isinstance(other, Product):
            return (self.price * self.quantity) + (other.price * other.quantity)
        return NotImplemented


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
        Category.total_product_count += len(self._products)

    def add_product(self, product: Product):
        """Добавляет продукт в категорию."""
        self._products.append(product)
        Category.total_product_count += 1

    @property
    def products(self):
        """Возвращает строку со всеми продуктами в категории."""
        return "\n".join(str(product) for product in self._products)

    @property
    def product_count(self):
        """Возвращает количество продуктов в категории."""
        return len(self._products)

    def __str__(self):
        """Строковое представление категории."""
        total_quantity = sum(product.quantity for product in self._products)
        return f"{self.name}, количество продуктов: {total_quantity} шт."

    def __iter__(self):
        """Возвращает итератор для продуктов в категории."""
        return ProductIterator(self)


class ProductIterator:
    """Итератор для перебора продуктов в категории."""

    def __init__(self, category):
        """Инициализирует итератор с категорией."""
        self._category = category
        self._index = 0

    def __iter__(self):
        """Возвращает сам итератор."""
        return self

    def __next__(self):
        """Возвращает следующий продукт в категории."""
        if self._index < len(self._category._products):  # Используем _products
            product = self._category._products[self._index]  # Используем _products
            self._index += 1
            return product
        else:
            raise StopIteration


# if __name__ == '__main__':
#     product1 = Product("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5)
#     product2 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
#     product3 = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)
#
#     print(str(product1))
#     print(str(product2))
#     print(str(product3))
#
#     category1 = Category(
#         "Смартфоны",
#         "Смартфоны, как средство не только коммуникации, но и получения дополнительных функций для удобства жизни",
#         [product1, product2, product3]
#     )
#
#     print(str(category1))
#
#     print(category1.products)
#
#     print(product1 + product2)
#     print(product1 + product3)
#     print(product2 + product3)
