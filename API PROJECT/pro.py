from flask import Flask,request,jsonify
from flask_mysqldb import MySQL
from datetime import datetime,timedelta
from flask_bcrypt import Bcrypt
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
    pname=data['pname']
    ppemail=data['ppemail']
    ppassw=data['ppassw']
    pphn=data['pphn']
    pplace=data['pplace']
    if not pname or not ppemail or not ppassw:
        return jsonify({"Error":"Missing credentials"})
    cur=mysql.connection.cursor()
    cur.execute("select * from patient where ppemail=%s",(ppemail,))
    if cur.fetchone():
        return jsonify({"message":"patient already exist"})
    hashed_password=bcrypt.generate_password_hash(ppassw).decode('utf-8')
    cur.execute("insert into patient (pname,ppemail,ppassw,pphn,pplace) values (%s,%s,%s,%s,%s)",(pname,ppemail,hashed_password,pphn,pplace))
    mysql.connection.commit()
    return jsonify({"Message":"patient register success"})
    
   

@app.route("/viewalltodo",methods=["GET"])
def viewalltodo():
    cur=mysql.connection.cursor()
    cur.execute("select pname,pplace from patient")
    rows=cur.fetchall()
    col_name=[desc[0] for desc in cur.description]
    results=[dict(zip(col_name,row)) for row in rows]
    return jsonify(results)

@app.route("/userlogin",methods=["POST"])
def userlogin():
    data=request.json
    email=data['ppemail']
    userp_=data['ppassw']
    if not email or not userp_:
        return jsonify({"Error":"missing credentials"})
    cur=mysql.connection.cursor()
    cur.execute("select pid,pname,ppemail,ppassw from patient where ppemail=%s",(email,))
    user=cur.fetchone()
    if not user:
        return jsonify({"Message":"patient not found"})
    pid,pname,ppemail,ppassw=user
    if bcrypt.check_password_hash(ppassw,userp_):
        access_token=create_access_token(identity=str(pid),expires_delta=timedelta(hours=1))
        return jsonify({"message":"Login success","access_token":access_token})
    else:
        return jsonify({"message":"Login failed"})
 
@app.route("/profile1",methods=['get'])
@jwt_required()
def profile1():
    jwt_data=get_jwt()
    current_user=get_jwt_identity()
    cur=mysql.connection.cursor()
    cur.execute("select * from patient where pid=%s",(current_user,))
    row=cur.fetchone()
    return jsonify(
        {"patientid":current_user,"JWT":jwt_data,"patientname":row[1],"patientemail":row[2],"patientplace":row[5],"patientphn":row[4]}
    )

@app.route("/userhistory",methods=['GET'])
@jwt_required()
def userhistory():
    current_user=get_jwt_identity()
    cur=mysql.connection.cursor()
    cur.execute("select p.pname,q.kw,d.dname from patient p join query q on q.pemail=p.ppemail join doctor d on d.dkw=q.kw where pid=%s",(current_user,))
    #joining tables to get information 
    rows=cur.fetchall()
    col_name=[desc[0] for desc in cur.description]
    results=[dict(zip(col_name,row)) for row in rows]
    return jsonify(results)


@app.route("/tellproblem",methods=['post','get'])
@jwt_required()
def tellproblem():
    data = request.get_json()
    problem = data.get("problem")
    current_user=get_jwt_identity()
    cur=mysql.connection.cursor()
    cur.execute("select ppemail from patient where pid = %s", (current_user,))
    result = cur.fetchone()
    if not result:
        return jsonify({"message": "User not found"}), 404
    email = result[0]
    cur.execute("select did,dname from doctor where dkw=%s",(problem,))
    row=cur.fetchone()
    if row:  # If a matching doctor is found
        did, dname = row
        # You can store did and dname in the 'answer' column (e.g., concatenated as a string)
        answer = f"Doctor ID: {did}, Name: {dname}"
    cur.execute("insert into query (pemail,kw,answer) values(%s,%s,%s)",(email,problem,answer))
    mysql.connection.commit()
    if cur.rowcount>0:
        return jsonify({"message":"Go to View history button"})
    return jsonify({"message":"something went wrong"})

if __name__=="__main__":
   app.run(debug=True)
