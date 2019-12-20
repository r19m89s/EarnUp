from werkzeug.wrappers import Request, Response
import csv
import MySQLdb
import os
import datetime
import simplejson as json

def obtain_location_rows(cursor,request_body):
    location_rows = []
    location = {}
    if request_body.has_key("latitude") and request_body.has_key("longitude") and request_body.has_key("query"):
        location['latitude'] = request_body['latitude']
        location['longitude'] = request_body['longitude']
        location['distance'] = request_body['distance']
    if(location):
         cursor.execute("SELECT * FROM (SELECT apt_info.*, ROUND(3959 * acos(cos(radians(latitude)) * cos("+str(location['latitude'])+")) * cos( radians("+str(location['longitude'])+") - radians(longitude)) + sin(radians(latitude)) * sin(radians("+str(location['latitude'])+")), 3) AS distance FROM apt_info) AS subq WHERE distance <= 1000 ORDER BY distance ASC")
         location_rows = cursor.fetchall()
    return location_rows

def obtain_query_rows(cursor,request_body,location_ids):
    query_rows = []
    query_string = request_body['query']
    if (query_string):
        query_str = 'SELECT * FROM apt_info WHERE MATCH(name) AGAINST ("'+query_string+'") > 1'
        if (location_ids):
            query_str += " AND id IN ("+','.join(map(str,location_ids))+")"
        cursor.execute(query_str)
        query_rows = cursor.fetchall()
    return query_rows
    
@Request.application
def application(request):
    conn = MySQLdb.connect(host='localhost',user='root',passwd='',db='earnup')
    cursor = conn.cursor()
    response = ""
    try:
        print request.data
        request_body = json.loads(request.data)
        location_rows = obtain_location_rows(cursor,request_body)
        location_ids = [row[0] for row in location_rows]
        query_rows = obtain_query_rows(cursor,request_body,location_ids)
        final_rows = []
        if(query_rows):
            final_rows = query_rows
        elif (location_rows):
            final_rows = location_rows
        else:
            cursor.execute("SELECT * FROM apt_info limit 25")
            final_rows = cursor.fetchall()
        response = json.dumps(final_rows, use_decimal=True, default=str)
    except Exception as e:
        print(e)
        response = "You have attempted a request with incorrectly formatted JSON data. Please try again."
    cursor.close()
    return Response(response)

def create_database():
    mydb = MySQLdb.connect(host='localhost',user='root',passwd='',port=3306)
    cursor = mydb.cursor()
    cursor.execute("DROP DATABASE IF EXISTS earnup")
    cursor.execute("CREATE DATABASE earnup")
    cursor.close()

def create_table(cursor):
    cursor.execute("CREATE TABLE apt_info (`id` int(11) NOT NULL, `name` varchar(255) NOT NULL,`host_id` int(11) NOT NULL,`host_name` varchar(255) not NULL,`neighbourhood_group` varchar(255) NOT NULL,`neighbourhood`  varchar(255) NOT NULL,`latitude` decimal(18,5) NOT NULL, `longitude` decimal(18,5) NOT NULL, `room_type`  varchar(255) NOT NULL, `price` int(11) NOT NULL, `minimum_nights` int(11) NOT NULL,`number_of_reviews` int(11) NOT NULL,`last_review` timestamp, `reviews_per_month`  decimal(11,2) DEFAULT 0.00,`calculated_host_listings_count` int(11),`availability_365` int(11), PRIMARY KEY (`id`), FULLTEXT (`name`))")
    

def populate_table(conn,cursor):
    with open("AB_NYC_2019.csv","rb") as file:
        csv_data = csv.reader((line.replace('\000','').replace('\xef\xbc\x8c',',') for line in file), delimiter=",")
        for index,row in enumerate(csv_data):
            if index > 1:       
                if (row[13] != ''):
                    row[13] = float(row[13])
                else:
                    row[13] = 0.0
                if (row[12] != ''):
                    row[12] =  row[12]
                else:
                    row[12] = None
                row[6] = ''.join([i for i in row[6] if i.isdigit()])  
                row[2] = row[2].encode("ascii")
                cursor.execute("INSERT INTO apt_info (id,name,host_id,host_name,neighbourhood_group,neighbourhood,latitude,longitude,room_type,price,minimum_nights,number_of_reviews,last_review,reviews_per_month,calculated_host_listings_count,availability_365) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",[int(row[0]),row[1],int(row[2]),row[3],row[4],row[5],float(row[6]),float(row[7]),row[8],int(row[9]),int(row[10]),int(row[11]),row[12],row[13],int(row[14]),int(row[15])])
                conn.commit()

if __name__ == '__main__':
    from werkzeug.serving import run_simple
    create_database()
    conn = MySQLdb.connect(host='localhost',user='root',passwd='',db='earnup')
    cursor = conn.cursor()
    create_table(cursor)
    populate_table(conn,cursor)
    cursor.close()
    run_simple('localhost', 4000, application)
