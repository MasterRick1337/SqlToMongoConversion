import json
import pymongo
import pymysql


def connect_mysql(host, port, user, password, database):
    conn = pymysql.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        database=database
    )
    return conn


def connect_mongodb(uri, username, password):
    client = pymongo.MongoClient(uri)
    db = client.get_database()
    if username and password:
        db.authenticate(username, password)
    return db


def fetch_data_from_mysql(conn, table_name):
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table_name}")
    columns = [column[0] for column in cursor.description]
    data = cursor.fetchall()
    cursor.close()
    return columns, data


def convert_data_to_json(columns, data):
    results = []
    for row in data:
        result = {}
        for i, value in enumerate(row):
            result[columns[i]] = value
        results.append(result)
    return results


def insert_data_into_mongodb(db, collection_name, data):
    collection = db[collection_name]
    collection.insert_many(data)


def main():
    mysql_host = 'localhost'
    mysql_port = 3306
    mysql_user = 'root'
    mysql_password = 'password'
    mysql_database = 'w3schools'

    mongodb_uri = 'mongodb://localhost:27778/'
    mongodb_username = 'root'
    mongodb_password = 'password'

    mysql_conn = connect_mysql(mysql_host, mysql_port, mysql_user, mysql_password, mysql_database)

    # Connect to MongoDB
    mongodb_db = connect_mongodb(mongodb_uri, mongodb_username, mongodb_password)

    tables = ["suppliers", "categories", "customers", "employees", "shippers", "orders", "products", "order_details"]

    for table in tables:
        columns, data = fetch_data_from_mysql(mysql_conn, table)
        json_data = convert_data_to_json(columns, data)
        insert_data_into_mongodb(mongodb_db, table, json_data)

    mysql_conn.close()


if __name__ == "__main__":
    main()
