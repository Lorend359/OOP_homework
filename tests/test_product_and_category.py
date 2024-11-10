import pytest

from src.product_and_category import Category, Product


@pytest.fixture(autouse=True)
def reset_counts():
    Category.category_count = 0
    Category.product_count = 0


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
    category1, category2, product1, product2, product3, product4 = setup_categories_and_products
    assert len(category1.products) == 3
    assert len(category2.products) == 1
    assert Category.product_count == 4


def test_category_count(setup_categories_and_products):
    category1, category2, _, _, _, _ = setup_categories_and_products
    assert Category.category_count == 2
