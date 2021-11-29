import psycopg2

#establishing the connection
conn = psycopg2.connect(
   database="aggieeats", user='postgres', password='admin', host='127.0.0.1', port= '5432'
)
conn.autocommit = True

#Creating a cursor object using the cursor() method
cursor = conn.cursor()

#Preparing query to create a database
create_db = '''CREATE database AggieEats''';
create_table = '''CREATE TABLE test1 (key INTEGER, value INTEGER)''';
insert = '''INSERT INTO test1 (key,value) VALUES (5,6) ''';
search = '''SELECT * FROM test1''';

try:
    cursor.execute(insert)
    cursor.execute(search)
    results = cursor.fetchall()
    for r in results:
        print(r)
except Exception as err:
    print(err)
finally:
    pass

#Closing the connection
conn.close()