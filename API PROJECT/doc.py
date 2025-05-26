from flask import Flask,request,jsonify
from flask_mysqldb import MySQL #pip3 install flask-mysqldb
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
    dname=data['dname']
    demail=data['demail']
    dpassw=data['dpassw']
    dphn=data['dphn']
    dspec=data['dspec']
    dkw=data['dkw']
    
    if not dname or not demail or not dpassw:
        return jsonify({"Error":"Missing credentials"})
    cur=mysql.connection.cursor()
    cur.execute("select * from doctor where demail=%s",(demail,))
    if cur.fetchone():
        return jsonify({"message":"doctor already exist"})
    hashed_password=bcrypt.generate_password_hash(dpassw).decode('utf-8')
    cur.execute("insert into doctor (dname,demail,dpassw,dphn,dspec,dkw) values (%s,%s,%s,%s,%s,%s)",(dname,demail,hashed_password,dphn,dspec,dkw))
    mysql.connection.commit()
    return jsonify({"Message":"doctor register success"})
    

@app.route("/viewalltodo",methods=["GET"])
def viewalltodo():
    cur=mysql.connection.cursor()
    cur.execute("select dname,dspec from doctor")
    rows=cur.fetchall()
    col_name=[desc[0] for desc in cur.description]
    results=[dict(zip(col_name,row)) for row in rows]
    return jsonify(results)

@app.route("/userlogin",methods=["POST"])
def userlogin():
    data=request.json
    email=data['demail']
    userp_=data['dpassw']
    if not email or not userp_:
        return jsonify({"Error":"missing credentials"})
    cur=mysql.connection.cursor()
    cur.execute("select did,dname,demail,dpassw from doctor where demail=%s",(email,))
    user=cur.fetchone()
    if not user:
        return jsonify({"Message":"doctor not found"})
    did,dname,demail,dpassw=user
    if bcrypt.check_password_hash(dpassw,userp_):
        access_token=create_access_token(identity=str(did),expires_delta=timedelta(hours=1))
        return jsonify({"message":"Login success","access_token":access_token})
    else:
        return jsonify({"message":"Login failed"})


@app.route("/profile2",methods=['get'])
@jwt_required()
def profile1():
    jwt_data=get_jwt()
    current_user=get_jwt_identity()
    cur=mysql.connection.cursor()
    cur.execute("select * from doctor where did=%s",(current_user,))
    row=cur.fetchone()
    return jsonify(
        {"doctorid":current_user,"JWT":jwt_data,"doctorname":row[1],"doctoremail":row[2],"doctorspec":row[5],"doctorphn":row[4]}
    )
 


if __name__=="__main__":
   app.run(debug=True)
