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
        if not isinstance(other, Product):
            raise TypeError(f"Невозможно сложить объекты разных типов: {type(self).__name__} и {type(other).__name__}")

        if type(self) is not type(other):
            raise TypeError(f"Невозможно сложить {type(self).__name__} и {type(other).__name__}")

        return (self.price * self.quantity) + (other.price * other.quantity)


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

    def add_product(self, product):
        """Добавляет продукт в категорию."""
        if not isinstance(product, Product):
            raise TypeError(
                f"Нельзя добавить объект типа {type(product).__name__}. Ожидался продукт или его наследник."
            )

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
        if self._index < len(self._category._products):
            product = self._category._products[self._index]
            self._index += 1
            return product
        else:
            raise StopIteration


class Smartphone(Product):
    """Класс, представляющий смартфон."""

    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
        efficiency: str,
        model: str,
        memory: str,
        color: str,
    ):
        """Инициализирует смартфон с данными."""
        super().__init__(name, description, price, quantity)
        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color

    def __str__(self):
        """Строковое представление смартфона."""
        return (
            super().__str__() + f", Эффективность: {self.efficiency}, Модель: {self.model}, "
            f"Встроенная память: {self.memory}, Цвет: {self.color}"
        )


class LawnGrass(Product):
    """Класс, представляющий газонную траву."""

    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
        country: str,
        germination_period: int,
        color: str,
    ):
        """Инициализирует газонную траву с данными."""
        super().__init__(name, description, price, quantity)
        self.country = country
        self.germination_period = germination_period
        self.color = color

    def __str__(self):
        """Строковое представление газонной травы."""
        return (
            super().__str__()
            + f", Страна: {self.country}, Срок прорастания: {self.germination_period} дней, Цвет: {self.color}"
        )


# if __name__ == '__main__':
#     smartphone1 = Smartphone("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5, 95.5,
#                          "S23 Ultra", 256, "Серый")
#     smartphone2 = Smartphone("Iphone 15", "512GB, Gray space", 210000.0, 8, 98.2, "15", 512, "Gray space")
#     smartphone3 = Smartphone("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14, 90.3, "Note 11", 1024, "Синий")
#
#     print(smartphone1.name)
#     print(smartphone1.description)
#     print(smartphone1.price)
#     print(smartphone1.quantity)
#     print(smartphone1.efficiency)
#     print(smartphone1.model)
#     print(smartphone1.memory)
#     print(smartphone1.color)
#
#     print(smartphone2.name)
#     print(smartphone2.description)
#     print(smartphone2.price)
#     print(smartphone2.quantity)
#     print(smartphone2.efficiency)
#     print(smartphone2.model)
#     print(smartphone2.memory)
#     print(smartphone2.color)
#
#     print(smartphone3.name)
#     print(smartphone3.description)
#     print(smartphone3.price)
#     print(smartphone3.quantity)
#     print(smartphone3.efficiency)
#     print(smartphone3.model)
#     print(smartphone3.memory)
#     print(smartphone3.color)
#
#     grass1 = LawnGrass("Газонная трава", "Элитная трава для газона", 500.0, 20, "Россия", "7 дней", "Зеленый")
#     grass2 = LawnGrass("Газонная трава 2", "Выносливая трава", 450.0, 15, "США", "5 дней", "Темно-зеленый")
#
#     print(grass1.name)
#     print(grass1.description)
#     print(grass1.price)
#     print(grass1.quantity)
#     print(grass1.country)
#     print(grass1.germination_period)
#     print(grass1.color)
#
#     print(grass2.name)
#     print(grass2.description)
#     print(grass2.price)
#     print(grass2.quantity)
#     print(grass2.country)
#     print(grass2.germination_period)
#     print(grass2.color)
#
#     smartphone_sum = smartphone1 + smartphone2
#     print(smartphone_sum)
#
#     grass_sum = grass1 + grass2
#     print(grass_sum)
#
#     try:
#         invalid_sum = smartphone1 + grass1
#     except TypeError:
#         print("Возникла ошибка TypeError при попытке сложения")
#     else:
#         print("Не возникла ошибка TypeError при попытке сложения")
#
#     category_smartphones = Category("Смартфоны", "Высокотехнологичные смартфоны", [smartphone1, smartphone2])
#     category_grass = Category("Газонная трава", "Различные виды газонной травы", [grass1, grass2])
#
#     category_smartphones.add_product(smartphone3)
#
#     print(category_smartphones.products)
#
#     print(Category.product_count)
#
#     try:
#         category_smartphones.add_product("Not a product")
#     except TypeError:
#         print("Возникла ошибка TypeError при добавлении не продукта")
#     else:
#         print("Не возникла ошибка TypeError при добавлении не продукта")
