from abc import ABC, abstractmethod


class BaseProduct(ABC):
    """Абстрактный базовый класс для продуктов."""

    @abstractmethod
    def __str__(self):
        """Метод для возврата строкового представления продукта."""
        pass

    @abstractmethod
    def price(self):
        """Метод для получения цены продукта."""
        pass

    @abstractmethod
    def quantity(self):
        """Метод для получения количества продукта."""
        pass


class MixinInitLogger:
    """Миксин для логирования инициализации объектов."""

    def __init__(self, *args, **kwargs):
        class_name = self.__class__.__name__
        params = ", ".join(map(str, args))
        print(f"Создан объект {class_name} с параметрами: {params}")


class Product(MixinInitLogger, BaseProduct):
    """Класс, представляющий продукт."""

    def __init__(self, name: str, description: str, price: float, quantity: int):
        super().__init__(name, description, price, quantity)
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


class BaseEntity(ABC):
    """Абстрактный базовый класс для сущностей с именем и описанием."""

    @abstractmethod
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

    @abstractmethod
    def get_description(self) -> str:
        """Метод для получения описания сущности."""
        pass


class Category(BaseEntity):
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

    def get_description(self) -> str:
        """Возвращает описание категории."""
        return self.description


class Order(BaseEntity):
    """Класс, представляющий заказ на продукт."""

    def __init__(self, product: Product, quantity: int):
        """Инициализирует заказ с продуктом и количеством."""
        super().__init__(product.name, product.description)
        self.product = product
        self.quantity = quantity
        self.total_price = self.product.price * self.quantity

    def get_description(self) -> str:
        """Возвращает детали заказа."""
        return (
            f"Заказ: {self.product.name}, Количество: {self.quantity}, Итоговая стоимость: {self.total_price:.2f} руб."
        )


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
#     product1 = Product("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5)
#     product2 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
#     product3 = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)
#
#     print(product1.name)
#     print(product1.description)
#     print(product1.price)
#     print(product1.quantity)
#
#     print(product2.name)
#     print(product2.description)
#     print(product2.price)
#     print(product2.quantity)
#
#     print(product3.name)
#     print(product3.description)
#     print(product3.price)
#     print(product3.quantity)
#
#     category1 = Category("Смартфоны",
#                          "Смартфоны, как средство не только коммуникации,
#                          но и получения дополнительных функций для удобства жизни",
#                          [product1, product2, product3])
#
#     print(category1.name == "Смартфоны")
#     print(category1.description)
#     print(len(category1.products))
#     print(category1.category_count)
#     print(category1.product_count)
#
#     product4 = Product("55\" QLED 4K", "Фоновая подсветка", 123000.0, 7)
#     category2 = Category("Телевизоры",
#                          "Современный телевизор,
#                          который позволяет наслаждаться просмотром, станет вашим другом и помощником",
#                          [product4])
#
#     print(category2.name)
#     print(category2.description)
#     print(len(category2.products))
#     print(category2.products)
#
#     print(Category.category_count)
#     print(Category.product_count)
