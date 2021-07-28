from flask import Flask, request, make_response
import json
import sqlite3
from request_to_sql_query import *


app = Flask(__name__)
app.config["DEBUG"] = True

@app.route('/analyze_data', methods=['GET'])
def analyze_data():
    try:
        data = json.loads(request.data)
        sql_query = select_statement_parsing(**data) + condition_statement_parsing(**data) + group_statement_parsing(**data) + order_statement_parsing(**data)
        if(sql_query == ""):
            sql_query = "select * from AdjustData"
        try:
            connection = sqlite3.connect("adjust.db")
            cursor = connection.cursor()
        except:
            return {
                "message" : "An error occured while connecting to this database."
            }

        result = cursor.execute(sql_query)
    except:
        return {
            "message" : "Error, could not execute this query."
        }
    result = result.fetchall()
    return {
        "message": "The operation was successful.",
        "sql query" : sql_query,
        "result": result,
        "satus": 200
    }


if(__name__ == "__main__"):
    app.run(debug= True)