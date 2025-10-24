from sql_connection import get_sql_connection

def get_all_products(connection):
    cursor = connection.cursor()

    query = ("SELECT p.product_id, p.name, p.unitMessure_id, p.price_per_unit, u.uomName "
             "FROM products p JOIN uom u ON p.unitMessure_id = u.unitMessure_id;")

    cursor.execute(query)

    response = []
    
    for (product_id, name, unitMessure_id, price_per_unit, uomName) in cursor:
        response.append({
            "product_id": product_id,
            "name": name,
            "unitMessure_id": unitMessure_id,
            "price_per_unit": price_per_unit,
            "uomName": uomName
        })

    return response

def insert_new_product(connection, product):
    cursor = connection.cursor()

    query = ("INSERT INTO products (name, unitMessure_id, price_per_unit) "
             "VALUES (%s, %s, %s)")
    
    data = (product['name'], product['unitMessure_id'], product['price_per_unit'])

    cursor.execute(query, data)
    connection.commit()
    
    return cursor.lastrowid

def delete_product(connection, product_id):
    cursor = connection.cursor()

    query = ("DELETE FROM products WHERE product_id =" + str(product_id))
    
    cursor.execute(query)
    connection.commit()
    
    return cursor.lastrowid

if __name__ == "__main__":
    connection = get_sql_connection()
    