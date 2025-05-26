from flask import Flask,request,jsonify
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
from datetime import datetime,timedelta
from flask_jwt_extended import JWTManager,create_access_token,jwt_required,get_jwt,get_jwt_identity
from flask_cors import CORS


app=Flask(__name__)
bcrypt=Bcrypt(app)
CORS(app)
app.config['JWT_SECRET_KEY']="myapp123"
jwt=JWTManager(app)


app.config['MYSQL_USER']="root"
app.config['MYSQL_PASSWORD']="satvika"
app.config['MYSQL_DB']="health"
app.config['MYSQL_HOST']="localhost"

mysql=MySQL(app)

@app.route("/addtodo",methods=["POST"])
def addtodo():
    data=request.json

    pemail=data['pemail']
    kw=data['kw']
    
    if not pemail or not kw:
        return jsonify({"Error":"Missing credentials"})
    cur=mysql.connection.cursor()
    cur.execute("insert into query(pemail,kw)values(%s,%s)",(pemail,kw))
    cur.execute("select did,dname from doctor where dkw=%s",(kw,))
    row=cur.fetchone()
    if row:  # If a matching doctor is found
        did, dname = row
        # You can store did and dname in the 'answer' column (e.g., concatenated as a string)
        answer = f"Doctor ID: {did}, Name: {dname}"
        
        # Step 3: Insert the 'answer' back into the 'query' table
        cur.execute("UPDATE query SET answer = %s WHERE pemail = %s AND kw = %s", (answer, pemail, kw))
        mysql.connection.commit()
        return answer
    else:
        return jsonify({"Error": "No doctor found for the given keyword"})
    




if __name__=="__main__":
   app.run(debug=True)
