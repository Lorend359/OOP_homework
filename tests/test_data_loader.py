import json

import pytest

from src.data_loader import load_data_from_json


@pytest.fixture
def sample_json_file(tmp_path):
    data = [
        {
            "name": "Электроника",
            "description": "Все о электронике",
            "products": [
                {"name": "Смартфон", "description": "Смартфон с высоким разрешением", "price": 500, "quantity": 20},
                {"name": "Ноутбук", "description": "Мощный ноутбук", "price": 1000, "quantity": 10},
            ],
        }
    ]
    json_file = tmp_path / "products.json"
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    return json_file


def test_load_data_from_json(sample_json_file):
    categories = load_data_from_json(sample_json_file)

    assert len(categories) == 1
    assert categories[0].name == "Электроника"
    assert categories[0].description == "Все о электронике"
    assert len(categories[0].products) == 2

    assert categories[0].products[0].name == "Смартфон"
    assert categories[0].products[0].description == "Смартфон с высоким разрешением"
    assert categories[0].products[0].price == 500
    assert categories[0].products[0].quantity == 20

    assert categories[0].products[1].name == "Ноутбук"
    assert categories[0].products[1].description == "Мощный ноутбук"
    assert categories[0].products[1].price == 1000
    assert categories[0].products[1].quantity == 10
