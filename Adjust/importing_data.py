import sqlite3, csv

connection = sqlite3.connect("adjust.db")
cursor = connection.cursor()

sql_query = """
            CREATE TABLE AdjustData (
            date TEXT,
            channel TEXT,
            country TEXT,
            os TEXT,
            impressions INTEGER,
            clicks INTEGER,
            installs INTEGER,
            spend REAL,
            revenue REAL
            )"""

cursor.execute(sql_query)
connection.commit()
print(f"AdjustData has been created.")

with open("dataset.csv") as file:
    number_of_records = 0
    for row in file:
        cursor.execute("INSERT INTO AdjustData VALUES (?,?,?,?,?,?,?,?,?)", row.split(","))
        connection.commit()
        number_of_records += 1

connection.close()
print(f"{number_of_records} records have been inserted.")