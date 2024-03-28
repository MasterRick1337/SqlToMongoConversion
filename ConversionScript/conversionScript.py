import pymysql
import pymongo


def connect_to_mysql(host, port, user, password, database):
    conn = pymysql.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        database=database
    )
    return conn


def connect_to_mongodb(uri, username, password):
    client = pymongo.MongoClient(uri, username=username, password=password)
    return client


def convert_and_insert_data(mysql_conn, mongo_client):
    mysql_cursor = mysql_conn.cursor()

    db = mongo_client.get_database("orders")

    tables = ["suppliers", "categories", "customers", "employees", "shippers", "orders", "products", "order_details"]

    for table in tables:
        mysql_cursor.execute(f"SELECT * FROM {table}")
        collection_data = []
        for row in mysql_cursor.fetchall():
            result = {}
            for i, entry in enumerate(row):
                if mysql_cursor.description[i][0] == "BirthDate" or mysql_cursor.description[i][0] == "OrderDate":
                    entry = entry.strftime('%Y-%m-%dT%H:%M:%S')
                result[mysql_cursor.description[i][0]] = entry
            collection_data.append(result)

        db[table].insert_many(collection_data)

    mysql_conn.close()


def main():
    mysql_host = 'localhost'
    mysql_port = 3306
    mysql_user = 'root'
    mysql_password = 'password'
    mysql_database = 'w3schools'

    mongodb_uri = "mongodb://localhost:27778/"
    mongodb_username = "root"
    mongodb_password = "password"

    mysql_conn = connect_to_mysql(mysql_host, mysql_port, mysql_user, mysql_password, mysql_database)

    mongo_client = connect_to_mongodb(mongodb_uri, mongodb_username, mongodb_password)

    convert_and_insert_data(mysql_conn, mongo_client)


if __name__ == "__main__":
    main()
