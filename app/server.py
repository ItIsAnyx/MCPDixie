from mcp.server import MCPServer

mcp = MCPServer("DixieMCP")

# Заглушка для проверки работы mcp-инструмента
@mcp.tool()
def get_product(id: int) -> dict:
    return {
        "products": {
            "id": id,
            "name": "Молоко - тестовый товар",
            "description": "Тестовое описание Молока",
            "nutritional_specs": [
                {
                    "title": "Калории",
                    "subtitle": "420"
                }
            ],
            "grouped_info": [
                {
                    "type": str,
                    "name": str,
                    "data": object
                }
            ],
            "images": {
                "product": {
                    "main_image": {
                        "versions": {
                            "medium": str
                        }
                    }
                }
            }
        }
    }

if __name__ == "__main__":
    mcp.run(
        transport="streamable-http",
        host="127.0.0.1",
        port=8000,
        stateless_http=True,
        json_response=True,
    )