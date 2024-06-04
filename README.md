# Creating in Virtual Environment:
![image](https://github.com/kishorreyansh/IMDB-NEO4J-AURA-DB-PROGRAMMING/assets/140970519/2e453691-43c3-495e-9458-65222c28ac94)

![image](https://github.com/kishorreyansh/IMDB-NEO4J-AURA-DB-PROGRAMMING/assets/140970519/a59704a4-226c-4c86-a37f-d2a84c45e811)

![image](https://github.com/kishorreyansh/IMDB-NEO4J-AURA-DB-PROGRAMMING/assets/140970519/cf3cb584-cb16-4ab9-84eb-46632cf8b080)


# POSTMAN API:

# GET API : http://127.0.0.1:5000/imdb
![image](https://github.com/kishorreyansh/IMDB-NEO4J-AURA-DB-PROGRAMMING/assets/140970519/cd5e9bf4-f93b-4c42-bbf8-dc50c828a95f)

# POST API : http://127.0.0.1:5000/imdb

{
        "description": "A KALKI is based on Mahabharat.",
        "ids": "1001",
        "rating": "9.1",
        "revenue": "933.13",
        "runtime": "174",
        "title": "KALKI",
        "votes": "85085089",
        "year": "2024"
    }
    
![image](https://github.com/kishorreyansh/IMDB-NEO4J-AURA-DB-PROGRAMMING/assets/140970519/3d70241d-6c2a-4180-a731-37982b0c3c49)

# DELETE API : http://127.0.0.1:5000/imdb/KALKI
![image](https://github.com/kishorreyansh/IMDB-NEO4J-AURA-DB-PROGRAMMING/assets/140970519/43be81dc-10a6-4436-af8b-5c523a4b7c21)

# PATCH API : http://127.0.0.1:5000/imdb/KALKI

{
        "description": "A KALKI is based on Mahabharat. Prabhas and Deepika acted in it",
        "rating": "9.5",
        "title": "KALKI"
    }
    
![image](https://github.com/kishorreyansh/IMDB-NEO4J-AURA-DB-PROGRAMMING/assets/140970519/fc35639e-9e0f-4d45-85b3-66f79e7893f5)

# GET API USING TITLE : http://127.0.0.1:5000/imdb/KALKI
![image](https://github.com/kishorreyansh/IMDB-NEO4J-AURA-DB-PROGRAMMING/assets/140970519/060030c3-0387-4ae5-b2fa-a5ec9e128c31)

# NEO4J STEPS:

LOAD CSV WITH HEADERS FROM "https://raw.githubusercontent.com/khomsun2013/ADB/main/IMDB-Movie-Data.csv" AS row
WITH row.Ids AS i, row.Title AS t, row.Description AS d, row.Year AS y, row.Runtime AS r, row.Rating AS rt, row.Votes AS v, row.Revenue AS rv
WHERE rv IS NOT NULL
MERGE (:Movie{ids:i, title:t, description:d, year:y, runtime:r, rating:rt, votes: v, revenue:rv})
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
LOAD CSV WITH HEADERS FROM "https://raw.githubusercontent.com/khomsun2013/ADB/main/IMDB-Movie-Data.csv" AS row
WITH row.Ids AS i, row.Title AS t, row.Description AS d, row.Year AS y, row.Runtime AS r, row.Rating AS rt, row.Votes AS v, row.Revenue AS rv
WHERE rv IS NULL
MERGE (m:Movie{ids:i, title:t, description:d, year:y, runtime:r, rating:rt, votes: v})
ON CREATE SET m.revenue = NULL 
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
LOAD CSV WITH HEADERS FROM "https://raw.githubusercontent.com/khomsun2013/ADB/main/IMDB-Movie-Data.csv" AS row
WITH row.Ids AS t, SPLIT(row.Actors,',') AS a
UNWIND t AS t1
UNWIND a AS a1
WITH *, trim(a1) AS a2
MERGE (:Person{name:a2})
WITH *
MATCH(mo:Movie{ids:t1}),(ac:Person{name:a2})
MERGE (ac)-[:ACTED_IN]->(mo)
RETURN ac, mo


![image](https://github.com/kishorreyansh/IMDB-NEO4J-AURA-DB-PROGRAMMING/assets/140970519/fc2f7628-4d7e-4478-a8c3-8ce24a72a78a)

![image](https://github.com/kishorreyansh/IMDB-NEO4J-AURA-DB-PROGRAMMING/assets/140970519/444007bb-100e-4157-a859-fbc64a127c6b)





