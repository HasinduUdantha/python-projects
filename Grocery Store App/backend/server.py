from flask import Flask, jsonify, request
import products_DAO
from sql_connection import get_sql_connection
import mysql.connector
import json


app = Flask(__name__)

connection = get_sql_connection()

@app.route('/getProducts' , methods=['GET'])
def get_Products():
    
    products = products_DAO.get_all_products(connection)
    response = jsonify(products)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

if __name__ == "__main__":
    print("Starting Python Flask Server For Grocery Store App....")
    app.run(port='5000')
       
    
