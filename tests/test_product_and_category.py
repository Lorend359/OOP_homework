from unittest.mock import patch

import pytest

from src.product_and_category import Category, Product


@pytest.fixture(autouse=True)
def reset_counts():
    Category.category_count = 0
    Category.total_product_count = 0


@pytest.fixture
def setup_categories_and_products():
    product1 = Product("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5)
    product2 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
    product3 = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)
    product4 = Product('55" QLED 4K', "Фоновая подсветка", 123000.0, 7)

    category1 = Category(
        "Смартфоны",
        "Смартфоны, как средство не только коммуникации, но и получения дополнительных функций для удобства жизни",
        [product1, product2, product3],
    )
    category2 = Category(
        "Телевизоры",
        "Современный телевизор, который позволяет наслаждаться просмотром, станет вашим другом и помощником",
        [product4],
    )

    return category1, category2, product1, product2, product3, product4


def test_category_initialization():
    category = Category("Books", "All kinds of books")
    assert category.name == "Books"
    assert category.description == "All kinds of books"
    assert Category.category_count == 1


def test_product_initialization():
    product = Product("Tablet", "Touchscreen tablet", 399.99, 8)
    assert product.name == "Tablet"
    assert product.description == "Touchscreen tablet"
    assert product.price == 399.99
    assert product.quantity == 8


def test_product_count(setup_categories_and_products):
    category1, category2, _, _, _, _ = setup_categories_and_products
    assert category1.product_count == 3
    assert category2.product_count == 1
    assert Category.total_product_count == 4


def test_category_count(setup_categories_and_products):
    category1, category2, _, _, _, _ = setup_categories_and_products
    assert Category.category_count == 2


def test_product_addition(setup_categories_and_products):
    product1, product2, product3 = setup_categories_and_products[2:5]
    assert product1 + product2 == (180000.0 * 5) + (210000.0 * 8)  # 2580000.0
    assert product1 + product3 == (180000.0 * 5) + (31000.0 * 14)  # 1334000.0
    assert product2 + product3 == (210000.0 * 8) + (31000.0 * 14)  # 2114000.0


def test_price_setter():
    product = Product("Test Product", "Description", 100.0, 10)

    product.price = 150.0
    assert product.price == 150.0

    with patch("builtins.print") as mock_print:
        product.price = -50.0
        mock_print.assert_called_with("Цена не должна быть нулевой или отрицательной")
        assert product.price == 150.0

    with patch("builtins.input", return_value="n"):
        product.price = 75.0
        assert product.price == 150.0

    with patch("builtins.input", return_value="y"):
        product.price = 50.0
        assert product.price == 50.0


def test_new_product():
    product_info = {
        "name": "Test Product",
        "description": "Description",
        "price": 100.0,
        "quantity": 5,
    }
    existing_products = []

    new_product = Product.new_product(product_info, existing_products)
    assert len(existing_products) == 1
    assert existing_products[0].name == "Test Product"

    product_info_update = {
        "name": "Test Product",
        "description": "Updated Description",
        "price": 150.0,
        "quantity": 3,
    }

    updated_product = Product.new_product(product_info_update, existing_products)
    assert existing_products[0]._quantity == 8
    assert existing_products[0].price == 150.0


def test_product_count_property(setup_categories_and_products):
    category1, category2, _, _, _, _ = setup_categories_and_products
    assert category1.product_count == 3
    assert category2.product_count == 1


def test_category_str_method(setup_categories_and_products):
    category1, category2, _, _, _, _ = setup_categories_and_products
    assert str(category1) == "Смартфоны, количество продуктов: 27 шт."
    assert str(category2) == "Телевизоры, количество продуктов: 7 шт."


def test_string_representation():
    product = Product("Test Product", "Description", 100.0, 10)
    assert str(product) == "Test Product, 100.0 руб. Остаток: 10 шт."
    assert repr(product) == "Test Product, 100.0 руб. Остаток: 10 шт."


def test_product_iterator(setup_categories_and_products):
    category1, _, _, _, _, _ = setup_categories_and_products
    iterator = iter(category1)

    assert next(iterator) == category1._products[0]  # Используйте _products
    assert next(iterator) == category1._products[1]
    assert next(iterator) == category1._products[2]

    with pytest.raises(StopIteration):
        next(iterator)
