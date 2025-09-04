import mysql.connector
from mysql.connector import Error
from datetime import datetime
from config import host, user, password, database
from datetime import datetime
import hashlib

#function to connect mysql and python
def connect():
    try:
        conn= mysql.connector.connect(
            host=host,
            user = user,
            password=password,
            database=database,
          

        )
        if conn.is_connected(): 
            print("Connection successful: \n")
            return conn

    except Error as e:
        print('Ooops somthing went wrong \n')
        return None

#to protect or encode the user password
def hash_pass(password):
    return hashlib.sha256(password.encode()).hexdigest()

#function to asign user id to new users o check if already exists
def get_create_user(name, password, mod, user_name=None):
    conn=connect()
    cursor = conn.cursor()
    name=name.strip()
    name=name.lower() #to be sure that no metters how the user type your name it will be asigned the same ID
    if user_name:
        user_name=user_name.strip().lower()
    parametro = (name,) 
    cursor.execute("SELECT Id, password, name from users WHERE User_Name = %s", parametro) 
    result= cursor.fetchone()
    passH=hash_pass(password)

    if mod=="login":
        if result:# if not user not exists or incorrect password
            user_id, pass_store, users_name = result
            if pass_store==passH:
                cursor.close()
                conn.close()
                return user_id
        cursor.close()
        conn.close()
        return None
    elif mod=="register":
        #user already exists, so it should be login
        if result:
            cursor.close()
            conn.close()
            return None
        #if not exists, insert the name and password and asign an ID
        cursor.execute("INSERT INTO users (User_Name, password, name) VALUES (%s,%s,%s)", (name,passH, user_name))
        conn.commit()
        user_id=cursor.lastrowid
        users_name=user_name
        cursor.close()
        conn.close()
        return user_id

#MYSQL function to insert all values that was filled in the activities forms function to MySQL DB
def activitiesEnter(user_id, kindEx, duration, intensity):
    conn=connect()
    cursor=conn.cursor()
    consul = "INSERT INTO activities (Id_user,Exercise,Duration_min, Intensity, Date) VALUES (%s,%s,%s,%s,%s)"
    val=(user_id, kindEx,duration, intensity, datetime.now())
    cursor.execute(consul,val)
    conn.commit()
    cursor.close()
    conn.close()

#function to return records by user_id
def historialview(user_id):
    conn=connect()
    cursor=conn.cursor()
    today=datetime.now()
    #get actual month and year 
    month = today.month
    year = today.year
    #sql query to get all the records by user_id and specific dates
    consul="SELECT Exercise, Duration_min, Intensity, Date from activities WHERE Id_user=%s AND MONTH(Date)=%s AND YEAR(DATE)=%s ORDER BY Date ASC"
    cursor.execute(consul,(user_id,month,year))
    hisotrial_activities=cursor.fetchall() #save the query result of the month and year for a specific User
    conn.close()
    cursor.close()
    return hisotrial_activities


#function to get info from exercise records 
def stats_view(user_id):
    conn=connect()
    cursor=conn.cursor()
    today=datetime.now()
    month = today.month
    year = today.year
    #sql query to get info such as total sum of duration in minutes and all the data group by intensity and excersise
    #with that information, we can cover the tips and goals for stats
    consul="SELECT Exercise, sum(Duration_min) as Total_time, Intensity from activities WHERE Id_user=%s AND MONTH(Date)=%s AND YEAR(DATE)=%s GROUP BY Exercise, Intensity"
    cursor.execute(consul,(user_id,month,year))
    stats_activities=cursor.fetchall() #save the query result of the month and year for a specific user id
    conn.close()
    cursor.close()
    return stats_activities

#function to record health data such as height, weight, imc, activity status
def profiles(user_Id,height,weight, act_status, imc, kcal):
    conn=connect()
    cursor=conn.cursor()
    consul = "INSERT INTO health (user_Id,height,weight, act_status, imc, kcal, register_date) VALUES (%s,%s,%s,%s,%s,%s,%s)"
    val=(user_Id,height,weight, act_status, imc, kcal, datetime.now())
    cursor.execute(consul,val)
    conn.commit()
    cursor.close()
    conn.close()

#function to save personal data recorded in profile window
def age_sex(user_id, age, sex,birth):
    conn=connect()
    cursor=conn.cursor()
    consul="UPDATE users SET age=%s, sex=%s, birth=%s WHERE Id=%s"
    cursor.execute(consul, (age,sex,birth, user_id))

    conn.commit()
    cursor.close()
    conn.close()

#function to save and show the personal data in profile window
def savedatap(user_id):
    conn=connect()
    cursor=conn.cursor()
    consul="select DISTINCT(h.user_Id),h.imc,h.kcal,u.sex, u.birth, h.register_date from users u left join health h ON h.user_Id=u.Id WHERE h.user_ID=%s ORDER BY register_date DESC LIMIT 1"
    param=(user_id,)
    cursor.execute(consul,param)
    user=cursor.fetchall()
    cursor.close()
    conn.close()
    return user

#function to show and graph imc and weight progress over time
def imc_weight(user_id):
    conn=connect()
    cursor=conn.cursor()
    consult="SELECT user_Id, weight, imc, register_date FROM health WHERE user_Id=%s"
    cursor.execute(consult,(user_id,))

    progresshist=cursor.fetchall() #save the query result of the month and year for a specific 
    conn.close()
    cursor.close()
    return progresshist

#function to record mental health or mood over time
def mentalmood(user_id,motiva,stress,sleep,satisfied,difficult):
    conn=connect()
    cursor=conn.cursor()
    consul = "INSERT INTO mentalmood (user_Id,motivation,stress,sleep,satisfied,difficulty, date) VALUES (%s,%s,%s,%s,%s,%s,%s)"
    val=(user_id,motiva,stress,sleep,satisfied,difficult, datetime.now())
    cursor.execute(consul,val)
    conn.commit()
    cursor.close()
    conn.close()

def graphprogress(user_id):
    conn=connect()
    cursor=conn.cursor()
    consult = "SELECT DATE(Date), SUM(Duration_min) FROM activities WHERE Id_user = %s AND MONTH(Date) = MONTH(CURDATE()) AND YEAR(Date) = YEAR(CURDATE()) GROUP BY DATE(Date) ORDER BY DATE(Date)"
    cursor.execute(consult, (user_id,))
    data = cursor.fetchall()
    conn.close()
    cursor.close()

    dates = [row[0].strftime("%d-%b") for row in data]
    minutes = [row[1] for row in data]
    return dates, minutes
