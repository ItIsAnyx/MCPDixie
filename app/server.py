from mcp.server import MCPServer
from typing import Literal
import logging

import cache_layer
import mock_dixie

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s %(message)s")
mcp = MCPServer("DixieMCP")

# Инструмент для получения продукта по id
@mcp.tool()
def get_product(id: int) -> dict:
    """Get product details by ID.
    Use for composition, nutrition, and detailed descriptions.
    Obtain the ID from search_products; do not guess IDs.
    """
    return cache_layer.get_or_load(
        operation="get_product",
        params={"id": id},
        ttl=cache_layer.PRODUCT_TTL,
        loader=lambda: mock_dixie.get_product(id=id),
    )

# Инструмент для поиска продукта по совпадению названия с различными сортировками
@mcp.tool()
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
    params = {
        "q": q,
        "shop_id": shop_id,
        "sort": sort,
        "category_id": category_id,
        "limit": limit,
        "page": page,
    }

    return cache_layer.get_or_load(
        operation="search_products",
        params=params,
        ttl=cache_layer.SEARCH_TTL,
        loader=lambda: mock_dixie.search_products(**params),
    )

if __name__ == "__main__":
    mcp.run(
        transport="streamable-http",
        host="127.0.0.1",
        port=8000,
        stateless_http=True,
        json_response=True,
    )