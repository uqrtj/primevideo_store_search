import psycopg2
from psycopg2 import Error

try:
    connection = psycopg2.connect(user="postgres",
                                  password="",
                                  host="127.0.0.1",
                                  port="5432",
                                  database="primevideo")

    cursor = connection.cursor()

    for i in range(20):
        sql = """
            select response->'items'->%s->>'heading', response->'items'->%s->>'imdbRating', response->'items'->%s->>'releaseYear'
            from search_response_json_dump 
            where response->'items'->%s->>'imdbRating' is not null
            and (response->'items'->%s->>'imdbRating')::float >= 9.0
            order by response->'items'->%s->>'imdbRating' desc
            LIMIT 30
        """ % (i, i, i, i, i, i)
        #print(sql)
        cursor.execute(sql)

        rows = cursor.fetchall()
        for row in rows:
            print(row)

except (Exception, psycopg2.DatabaseError) as error:
    print("Error while searching PostgreSQL table", error)
finally:
    # closing database connection.
    if (connection):
        cursor.close()
        connection.close()
        #print("PostgreSQL connection is closed")