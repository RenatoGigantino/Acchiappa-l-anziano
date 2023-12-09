from flask import Flask,request,render_template,redirect,url_for, make_response, jsonify
import json
from google.cloud import firestore
from flask_login import LoginManager, current_user, login_user, logout_user, login_required, UserMixin
from secret import secret_key
from flask_cors import CORS
import smtplib # modulo per inviare email
from email.mime.text import MIMEText
import ssl
from datetime import datetime


class User(UserMixin):
    def __init__(self, username):
        super().__init__()
        self.id = username
        self.username = username
        self.par = {}

app = Flask(__name__)
app.config['SECRET_KEY'] = secret_key
local = True
CORS(app)
login = LoginManager(app)
login.login_view = '/static/login.html'


@login.user_loader
def load_user(username):
    db = firestore.Client.from_service_account_json('credentials.json') if local else firestore.Client()
    user = db.collection('utenti').document(username).get()
    if user.exists:
        return User(username)
    return None

@app.route('/',methods=['GET','POST'])
@app.route('/main',methods=['GET','POST'])
@app.route('/sensors',methods=['GET'])
def main():
    # db = firestore.Client.from_service_account_json('credentials.json') if local else firestore.Client()
    # s = []
    # for doc in db.collection('acceleration').stream():
    #     s.append(doc.id)
    # return json.dumps(s), 200
    return redirect('/static/login.html')

@app.route('/getcurrent', methods=['GET'])
def get_current_user():
    # response = Flask.make_response(('Hello world!\n'), {'X-My-Header': 'foo'})
    # return response
    return jsonify(current_user.username)   

@app.route('/sendemail',methods=['GET'])
def send_email ():
    print("mando la mail a => ", current_user.username)

    # variabile di prova andra' sostituita con current_user.username
    email = current_user.username

    # credenziali per la email mittente
    sender = "avviso.caduta@gmail.com"
    sender_psw = "xywi yzzw hati kkii"

    # contenuto della email
    message = MIMEText("e' caduto!!!!!!!\n\n")
    message['Subject'] = "Acchiappa l'anziano"
    message['From'] = sender
    message['To'] = email

    # dobbiamo specificare il server SMTP del servizio a cui vogliamo
    # connetterci e la relativa porta di servizio associata: 
    email_allarme = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    # Ora possiamo connetterci al server
    email_allarme.ehlo()

    # mandiamo l'email
    email_allarme.login(sender, sender_psw)
    email_allarme.sendmail(sender, [email], message.as_string())
    email_allarme.quit() # chiudo la connessione

    # come risposta ritorno ad accelleration... non e' soluzione definitiva
    # sarebbe meglio ritornare status 200 e bona 
    return redirect(url_for('static', filename='acceleration.html'))




@app.route('/sensors/<s>', methods=['POST'])
def add_data(s):
    print(request.values)
    data = request.get_json()
    val = data.get('val')
    
    # Add timestamp
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    data_dict = {'value': val, 'timestamp': timestamp}

    print(val, s)
    db = firestore.Client.from_service_account_json('credentials.json') if local else firestore.Client()
    doc_ref = db.collection('acceleration').document(current_user.username)
    entity = doc_ref.get()

    if entity.exists and 'values' in entity.to_dict():
        v = entity.to_dict()['values']
        v.append(data_dict)
        doc_ref.update({'values': v})
    else:
        doc_ref.set({'values': [data_dict]})

    return 'ok', 200


@app.route('/sensors/<s>',methods=['GET'])
def get_data(s):
    db = firestore.Client.from_service_account_json('credentials.json') if local else firestore.Client()
    entity = db.collection('acceleration').document(s).get()
    if entity.exists:
        return json.dumps(entity.to_dict()['values']),200
    else:
        return 'sensor not found',404

@app.route('/graph/<s>',methods=['GET'])
# @login_required
def graph_data(s):
    db = firestore.Client.from_service_account_json('credentials.json') if local else firestore.Client()
    entity = db.collection('acceleration').document(s).get()
    print(entity)
    if entity.exists:
        # d = []
        # d.append(['Number',s])
        # t = 0
        # dizionario={}
        # for x in entity.to_dict()['values']:
        #     if x['timestamp'] in dizionario:
        #        dizionario [x['timestamp']]+=1
        #     else:
        #        dizionario [x['timestamp']]=1   
        #     print(x)
        #     # d.append([t,x])
        #     # t+=1
        # print(dizionario)
        # list_of_items = list(dizionario.items())
        # list_of_items.insert(0,  ['date', 'cadute'])
        values = entity.to_dict().get('values', [])

        # Create a dictionary to store counts for each day
        day_counts = {}

        # Process each value and count occurrences for each day
        for value in values:
            timestamp_str = value.get('timestamp', '')
            if timestamp_str:
                timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S')
                day = timestamp.strftime('%Y-%m-%d')

                if day in day_counts:
                    day_counts[day] += 1
                else:
                    day_counts[day] = 1

        # Convert the dictionary to a list of items
        list_of_items = list(day_counts.items())
        list_of_items.insert(0, ['date', 'cadute'])
        # transposed_data = [['date', 'cadute']]
        # for day, count in day_counts.items():
        #     transposed_data.append([day, count])
        return render_template('graph.html',sensor=s,data=json.dumps(list_of_items))
        # return redirect(url_for('static', filename='acceleration.html'))
    else:
        return redirect(url_for('static', filename='sensor404.html'))

@app.route('/login', methods=['POST'])
def log_in():
    # if current_user.is_authenticated:
    #     return redirect(url_for('/main'))
    username = request.values['m']
    password = request.values['p']
    print(username, password)

    db = firestore.Client.from_service_account_json('credentials.json') if local else firestore.Client()
    user = db.collection('utenti').document(username).get()
    if user.exists and user.to_dict()['password']==password:
        login_user(User(username))
        # print("current_user ==== ", current_user.username)
        # next_page = request.args.get('next')
        # if not next_page:
        # next_page = 'main'
        # return redirect(url_for('/main'))
    # return redirect('/static/login.html')
        return redirect(url_for('static', filename='index.html'))
        # return 'sensor404.html'
    return 'non ok'


@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')


@app.route('/adduser', methods=['GET','POST'])
# @login_required
def adduser():
    # if current_user.username == 'marco':
    if request.method == 'GET':
        return redirect('/static/adduser.html')
    else:
        username = request.values['m']
        password = request.values['p']
        # email = request.values['m']
        db = firestore.Client.from_service_account_json('credentials.json') if local else firestore.Client()
        user = db.collection('utenti').document(username)
        user.set({'username':username,'password':password})
        return redirect('/static/login.html')
    # else:
    #     return redirect('/')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
