import pytest
from src.product_and_category import Product, Category  # Замените путь на свой

@pytest.fixture
def setup_categories_and_products():
    product1 = Product("iPhone 13", "128GB, Черный", 80000.0, 5)
    product2 = Product("Samsung Galaxy S21", "256GB, Серебряный", 70000.0, 3)
    category1 = Category("Смартфоны", "Все смартфоны", [product1, product2])
    return category1, product1, product2

def test_new_product_creation(setup_categories_and_products):
    category1, product1, product2 = setup_categories_and_products

    product_info = {
        "name": "iPhone 13",
        "description": "128GB, Черный",
        "price": 85000.0,
        "quantity": 2
    }

    new_product = Product.new_product(product_info, existing_products=category1._products)

    assert new_product.name == product1.name
    assert product1.quantity == 7
    assert product1.price == 85000.0

def test_add_new_product(setup_categories_and_products):
    category1, product1, product2 = setup_categories_and_products

    product_info = {
        "name": "Xiaomi Mi 11",
        "description": "256GB, Черный",
        "price": 60000.0,
        "quantity": 5
    }

    new_product = Product.new_product(product_info, existing_products=category1._products)

    assert new_product.name == "Xiaomi Mi 11"
    assert len(category1._products) == 3
    assert category1.products.splitlines()[-1].startswith("Xiaomi Mi 11")

def test_price_setter(setup_categories_and_products, monkeypatch):
    category1, product1, _ = setup_categories_and_products

    product1.price = 90000.0
    assert product1.price == 90000.0

    monkeypatch.setattr('builtins.input', lambda _: 'n')
    product1.price = 50000.0
    assert product1.price == 90000.0

def test_add_product_to_category(setup_categories_and_products):
    category1, product1, _ = setup_categories_and_products

    product3 = Product("OnePlus 9", "256GB, Серебряный", 55000.0, 10)
    category1.add_product(product3)

    assert len(category1._products) == 3
    assert category1.products.splitlines()[-1].startswith("OnePlus 9")