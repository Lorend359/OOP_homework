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
        if quantity == 0:
            raise ValueError("Товар с нулевым количеством не может быть добавлен")

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
        try:
            if product.quantity <= 0:
                raise ZeroQuantityError("Товар с нулевым или отрицательным количеством не может быть добавлен")
            if product in self._products:
                print(f"Продукт '{product.name}' уже существует в категории.")
                return
            self._products.append(product)
            Category.total_product_count += 1
            print(f"Товар '{product.name}' успешно добавлен в категорию.")
        except ZeroQuantityError as e:
            print(f"Ошибка: {e}")
            raise
        finally:
            print("Обработка добавления товара в категорию завершена.")

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

    def middle_price(self):
        """Метод для подсчета средней цены всех товаров в категории."""
        try:
            total_price = sum(product.price * product.quantity for product in self._products)
            total_quantity = sum(product.quantity for product in self._products)

            if total_quantity == 0:
                raise ZeroDivisionError("В категории нет товаров или товары с нулевым количеством.")

            return total_price / total_quantity

        except ZeroDivisionError:
            return 0.0
        except Exception as e:
            print(f"Произошла ошибка: {e}")
            return 0.0


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

    def add_product(self, product):
        """Добавляет продукт в заказ."""
        try:
            if product.quantity == 0:
                raise ZeroQuantityError()
            print(f"Товар '{product.name}' успешно добавлен в заказ.")
        except ZeroQuantityError as e:
            print(f"Ошибка: {e}")
        else:
            print("Товар был добавлен в заказ без ошибок.")
        finally:
            print("Обработка добавления товара в заказ завершена.")


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


class ZeroQuantityError(Exception):
    """Исключение, которое возникает при попытке добавить товар с нулевым количеством."""

    def __init__(self, message="Товар с нулевым количеством не может быть добавлен"):
        self.message = message
        super().__init__(self.message)


# if __name__ == '__main__':
#     try:
#         product_invalid = Product("Бракованный товар", "Неверное количество", 1000.0, 0)
#     except ValueError as e:
#         print(
#             "Возникла ошибка ValueError прерывающая работу программы при попытке добавить продукт с нулевым количеством")
#     else:
#         print("Не возникла ошибка ValueError при попытке добавить продукт с нулевым количеством")
#
#     product1 = Product("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5)
#     product2 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
#     product3 = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)
#
#     category1 = Category("Смартфоны", "Категория смартфонов", [product1, product2, product3])
#
#     print(category1.middle_price())
#
#     category_empty = Category("Пустая категория", "Категория без продуктов", [])
#     print(category_empty.middle_price())
