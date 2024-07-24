import os
import psycopg2
from dotenv import load_dotenv
from flask import Flask, request
from flask import Flask

load_dotenv()

INSERT_DEPARTMENT = "INSERT INTO DEPARTMENT (deptName, numfaculty) VALUES (%s, %s) RETURNING id";

app = Flask(__name__)
#url = os.environ.get("DATABASE_URL")
connection = psycopg2.connect(database="deptdb",host="postgres-service.default.svc.cluster.local",port=5432,user="svcuser",
                        password="postgres")
@app.get("/health")
def health():
    return {}, 200

@app.post("/department")
def create_dept():
    data = request.get_json()
    deptName = data["deptName"]
    numfaculty = data["numFaculty"]
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(INSERT_DEPARTMENT, (deptName, numfaculty))
            deptId = cursor.fetchone()[0]
            #deptName = cursor.fetchone()[1]
            return {"id": deptId}, 201

if __name__ == "__main__":
    app.run(host='0.0.0.0')
