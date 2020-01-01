import psycopg2
from psycopg2 import Error


# TODO: this will require another table that records start and end time
try:
    connection = psycopg2.connect(user="postgres",
                                  password="",
                                  host="127.0.0.1",
                                  port="5432",
                                  database="primevideo")

    cursor = connection.cursor()

    rows_today = []
    rows_yesterday = []
    for i in range(20):
        sql = """
            select response->'items'->%s->>'heading' 
            from search_response_json_dump 
            where response->'items'->%s->>'releaseYear' = '%s' 
            and response->'title'->>'string' like '%s%s%s'
            and created_date::date = current_date 
        """ % (i, i, '2019', '%', 'malayalam', '%')
        #print(sql)
        cursor.execute(sql)

        rows = cursor.fetchall()
        for row in rows:
            rows_today.append(row[0])

    for i in range(20):
        sql = """
            select response->'items'->%s->>'heading' 
            from search_response_json_dump 
            where response->'items'->%s->>'releaseYear' = '%s' 
            and response->'title'->>'string' like '%s%s%s'
            and created_date::date = current_date - 1
        """ % (i, i, '2019', '%', 'malayalam', '%')
        #print(sql)
        cursor.execute(sql)

        rows = cursor.fetchall()
        for row in rows:
            rows_yesterday.append(row[0])

    #print(rows_today)
    print(set(rows_today).symmetric_difference(set(rows_yesterday)))

except (Exception, psycopg2.DatabaseError) as error:
    print("Error while searching PostgreSQL table", error)
finally:
    # closing database connection.
    if (connection):
        cursor.close()
        connection.close()
        #print("PostgreSQL connection is closed")
