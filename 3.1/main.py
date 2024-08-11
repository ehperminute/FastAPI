#https://stepik.org/lesson/1044668/step/16?unit=1053242

from fastapi import FastAPI

app = FastAPI()

product_names = ["Iphone", "Phone Case", "Smartphone", "Headphones", "Smartwatch", "Microscope", "Acer Aspire", "Chair", "Keyboard", "Toffifee", "Kirieshki"]
categories = ["Electronics", "Accessories", "Electronics", "Accessories", "Electronics", "Electronics", "Electronics", "Accessories", "Accessories", "Snack", "Snack"]
prices = [1199, 25, 230, 250, 40, 59, 399, 1399, 29, 19, 9]

sample_products = [{"id": id,
                    "name": name,
                    "category": cat,
                    "price": price} for id, (name, cat, price) in enumerate(zip(product_names, categories, prices), 100)]

@app.get("/product/{product_id}")
def get_product_id(product_id: int):
    for product in sample_products:
        if product["id"] == product_id:
            return product
    return {"error": f"product with id={product_id} not found"}

@app.get("/products/search")
def search_product(keyword: str="", category: str="", limit: int|None=None):
    response = []
    for product in sample_products:
        if len(response) == limit:
            break
        if (keyword.lower() in product["name"].lower() and (not category or category.lower() == product["category"].lower())):
            response.append(product)
    return response or {"error": "empty query result"}
