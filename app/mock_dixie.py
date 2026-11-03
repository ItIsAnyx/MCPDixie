from typing import Literal

PRODUCTS = {
    123: {
        "id": 123,
        "name": "Молоко — тестовый товар",
        "description": "Молоко пастеризованное, 1 л.",
        "nutritional_specs": [
            {
                "title": "Энергетическая ценность на 100 г",
                "subtitle": "60 ккал",
            }
        ],
        "grouped_info": [
            {
                "type": "composition",
                "name": "Состав",
                "data": {"text": "Молоко нормализованное"},
            }
        ],
        "images": {
            "product": {
                "main_image": {
                    "versions": {"medium": ""}
                }
            }
        },
    }
}
PRODUCTS[123].update({
    "gold_erp_id": "mock-123",
    "price": 99.90,
    "old_price": 119.90,
    "discount": 17,
    "in_stock": True,
    "product_reviews": {"average_score": 4.7},
    "category_id": 10,
    "popularity": 100,
    "new_order": 1,
})
PRODUCTS[124] = {
    "id": 124,
    "gold_erp_id": "mock-124",
    "name": "Молоко 2,5% — тестовый товар",
    "description": "Тестовое молоко, 900 мл.",
    "price": 79.90,
    "old_price": None,
    "discount": 0,
    "in_stock": True,
    "product_reviews": {"average_score": 4.5},
    "nutritional_specs": [],
    "grouped_info": [],
    "images": {
        "product": {
            "main_image": {
                "versions": {"medium": ""}
            }
        }
    },
    "category_id": 10,
    "popularity": 80,
    "new_order": 2,
}

# Инструмент для получения продукта по id
def get_product(id: int) -> dict:
    """Get product details by ID.
    Use for composition, nutrition, and detailed descriptions.
    Obtain the ID from search_products; do not guess IDs.
    """
    products = PRODUCTS.get(id)

    if products is None:
        return {
            "products": None,
            "message": f"The product with the ID {id} was not found. Try to find the product using search_products()."
        }

    return {"products": products}

# Инструмент для поиска продукта по совпадению названия с различными сортировками
def search_products(
        q: str,
        shop_id: int | None = None,
        sort: Literal["popular_first", "popularity", "price_asc", "price_desc", "rating", "new", "discounts_first"] = "popular_first",
        category_id: int | None = None,
        limit: int = 10,
        page: int = 1,
) -> dict:
    """Search products by name and return a short list for selection.
    Use to find or compare products.
    For composition, nutrition, or descriptions, call get_product
    with an ID from the results.
    This mock supports only shop 123 and dairy category 10.
    """
    q = q.strip()
    if not q:
        return {
            "products": [],
            "message": "Enter the product name to search for",
        }

    if not 1 <= limit <= 50 or page < 1:
        return {
            "products": [],
            "message": "The page limit should be in the range from 1 to 50 and the page number is at least 1"
        }

    if shop_id is not None and shop_id != 123:
        return {
            "products": [],
            "message": f"The specified store does not exist. Available store is only 123."
        }

    products = [
        product for product in PRODUCTS.values()
        if q.casefold() in product["name"].casefold() and (
            category_id is None or product["category_id"] == category_id
        )
    ]

    if not products:
        return {
            "products": [],
            "total": 0,
            "message": f'Nothing was found for the query "{q}" with the specified filters. Try to change product name or category.'
        }

    sort_rules = {
        "popular_first": ("popularity", True),
        "popularity": ("popularity", True),
        "price_asc": ("price", False),
        "price_desc": ("price", True),
        "new": ("new_order", True),
        "discounts_first": ("discount", True),
        "rating": ("rating", True),
    }
    field, reverse = sort_rules[sort]

    def sort_value(product: dict):
        if field == "rating":
            return product["product_reviews"]["average_score"]

        return product[field]

    products.sort(key=sort_value, reverse=reverse)

    total = len(products)
    start = (page - 1) * limit
    selected = products[start:start + limit]

    result = [
        {
            "id": product["id"],
            "gold_erp_id": product["gold_erp_id"],
            "name": product["name"],
            "price": product["price"],
            "old_price": product["old_price"],
            "discount": product["discount"],
            "in_stock": product["in_stock"],
            "product_reviews": product["product_reviews"],
        }
        for product in selected
    ]
    return {
        "products": result,
        "total": total,
        "page": page,
        "limit": limit,
        "has_more": start + limit < total,
        "message": (
            "There are no products on that page. Specify a smaller page number."
            if not selected else ""
        ),
    }
