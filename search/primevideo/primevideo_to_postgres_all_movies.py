import requests
import psycopg2
from psycopg2 import Error
import json

r = requests.post('https://www.primevideo.com/gp/video/api/search?phrase=*&startIndex=20')
r_dictionary = r.json()

# print(r_dictionary)
# print(r_dictionary['totalItems'])
# TODO: take db bak up and truncate tale here
try:
    connection = psycopg2.connect(user="postgres",
                                  password="",
                                  host="127.0.0.1",
                                  port="5432",
                                  database="primevideo")

    cursor = connection.cursor()
    for pagination_start in range(0, r_dictionary['totalItems'], 20):
        prime_url = "https://www.primevideo.com/gp/video/api/search?phrase=*&startIndex=" + str(pagination_start)
        print(prime_url)
        response = requests.post(prime_url)
        response_dictionary = response.json()
        ### response_dictionary = r_dictionary

        sql = "INSERT INTO search_response_json_dump (  response ) VALUES (%s)"
        cursor.execute(sql, (json.dumps(response_dictionary),))

        connection.commit()
        print("Row created successfully in PostgreSQL ")

except (Exception, psycopg2.DatabaseError) as error:
    print("Error while inserting into PostgreSQL table", error)
finally:
    # closing database connection.
    if (connection):
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")

