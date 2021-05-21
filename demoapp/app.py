from flask import Flask
from flask import render_template
from flask import request
from twilio.rest import Client
from colorama import Fore, Back, Style
import requests_cache
import requests
account_sid = "AC43a5dd5d9b5418da70de48b91247452d"
auth_token = "8da1496139462eede8c95ebd614b279d"
client = Client(account_sid, auth_token)
app = Flask(__name__ , template_folder='templates')
@app.route("/")
def home():
    return render_template('index.html')
@app.route('/status_page', methods=['POST','GET'])
def login_reg_details():
    first_name = request.form['fname']
    last_name = request.form['lname']
    email_id = request.form['email']
    source_st = request.form['statePresent']
    source_dt = request.form['districtPresent']
    dest_st = request.form['visitState']
    dest_dt = request.form['visitDistrict']
    pno = request.form['phone']
    #id_proof = request.form['id-proof']
    date = request.form['bdate']
    date1 = request.form['ddate']
    full_name = first_name+" "+last_name
    r = requests.get('https://api.covid19india.org/v4/min/data.min.json')
    json_data = r.json()
    cnt = json_data[dest_st]['districts'][dest_dt]['total']['confirmed']
    #cnt = 3655115
    pop = json_data[dest_st]['districts'][dest_dt]['meta']['population']
    travel_pass = ((cnt/pop)*100)
    if(travel_pass< 30) and request.method == 'POST':
        status = 'CONFIRMED'
        final_status=Back.GREEN + status
        client.messages.create(to="whatsapp:+919441168409",
                               from_="whatsapp:+14155238886",
                               body="Hello "+full_name+" "+"Your Travel From "+" "+source_dt+" To "+dest_dt+" is "+ status+" "+" "+"Please Note this Ticket is Valid from"+" "+date+" "+" to "+" "+date1)
        return render_template('status.html',fname=first_name,lname=last_name,address=email_id,phone=pno,state=source_st,city=source_dt,vstate=dest_st,vcity=dest_dt,sdate=date,edate=date1,result=status) #var2=id_proof,
    else:
        status="Not Confirmed"
        client.messages.create(to="whatsapp:+919441168409",
                               from_="whatsapp:+14155238886",
                               body="Hello " + full_name + " " + "Your")
        return render_template('status.html',fname=first_name,lname=last_name,address=email_id,phone=pno,state=source_st,city=source_dt,vstate=dest_st,vcity=dest_dt,sdate=date,edate=date1,result="DECLINED") #var2=id_proof,
if(__name__=="__main__"):
    app.run("127.0.0.1",port=3011,debug=True)