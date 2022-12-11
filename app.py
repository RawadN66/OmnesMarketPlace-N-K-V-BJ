import datetime

from flask import Flask, abort, session, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
from flask_bcrypt import Bcrypt
from flask_cors import CORS, cross_origin
from flask_marshmallow import Marshmallow
from flask import request
from flask import jsonify
from flask_session import Session
from flask_mail import Mail, Message
import os
import jwt

SECRET_KEY = "b'|\xe7\xbfU3`\xc4\xec\xa7\xa9zf:}\xb5\xc7\xb9\x139^3@Dv'"
basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
bcrypt = Bcrypt(app)
ma = Marshmallow(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'Project_DB.db')
app.secret_key = "b'|\xe7\xbfU3`\xc4\xec\xa7\xa9zf:}\xb5\xc7\xb9\x139^3@Dv'"

engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
db = SQLAlchemy(app)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'serenackhayef@gmail.com'
app.config['MAIL_PASSWORD'] = 'omnesmarketplace'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
Email = Mail(app)

from .model.item import Item, ItemSchema
from .model.user import User, UserSchema
from .model.ticket import Ticket, TicketSchema
from .model.match import Match, MatchSchema
from .model.staff import Staff, StaffSchema
from .model.order import Orders, OrdersSchema
from .model.calendar import Calendar, CalendarSchema, CalendarSchemaFan

CORS(app, supports_credentials=True, withCredentials=True)


meta = MetaData()


# userstable = Table('users', meta, Column('id', Integer, primary_key=True, autoincrement=True),
#                    Column('username', String, unique=True), Column('password', String), Column('mail', String),
#                    Column('dob', String), Column('gender', String), Column('date_joined', String))
# itemstable = Table('items', meta, Column('id', Integer, primary_key=True, autoincrement=True),
#                    Column('name', String), Column('price', String), Column('stockleft', Integer),
#                    Column('kind', String), Column('sale', db.Boolean), Column('size', String))



staffTable = Table('admins', meta, Column('id', Integer, primary_key=True, autoincrement=True),
                   Column('username', String, unique=True), Column('password', String), Column('mail', String),
                   Column('dob', String), Column('gender', String), Column('date_joined', String),
                   Column('position', String),
                   Column('phone', String))

matches_schema = MatchSchema(many=True)
user_schema = UserSchema(many=True)
staff_schema = StaffSchema(many=True)
item_schema = ItemSchema(many=True)
ticket_schema = TicketSchema(many=True)
orders_schema = OrdersSchema(many=True)
calendar_schema = CalendarSchema(many=True)
calendar_schema1 = CalendarSchemaFan(many=True)


@app.route('/')
def init():
    return render_template('Home.html')


@app.route('/Home.html')
def index():
    return render_template('Home.html')


@app.route('/About_User.html')
def about_user():
    return render_template('About_User.html')


@app.route('/About.html')
def about():
    return render_template('About.html')


@app.route('/Cart.html')
def cart():
    return render_template('Cart.html')


@app.route('/edit_item.html')
def edit_item_():
    return render_template('edit_item.html')


@app.route('/edit_staff.html')
def edit_staff():
    return render_template('edit_staff.html')


@app.route('/edit_user.html')
def edit_user_():
    return render_template('edit_user.html')


@app.route('/edit.html')
def edit():
    return render_template('edit.html')



@app.route('/Home_signed.html')
def home_signed():
    return render_template('Home_signed.html')


@app.route('/Mailing-.html')
def mailing():
    return render_template('Mailing-.html')


@app.route('/Order-History.html')
def order_history():
    return render_template('Order-History.html')


@app.route('/self_edit_user.html')
def self_edit_user():
    return render_template('self_edit_user.html')


@app.route('/Shop_unsigned.html')
def shop_unsigned():
    return render_template('Shop_unsigned.html')


@app.route('/Shop.html')
def shop():
    return render_template('Shop.html')


@app.route('/Sign-In.html')
def sign_in():
    return render_template('Sign-In.html')


@app.route('/Staff-Calendar.html')
def staff_calendar():
    return render_template('Staff-Calendar.html')


@app.route('/Ticket-Sale.html')
def ticket_sale():
    return render_template('/Ticket-Sale.html')


@app.route('/edit_ticket.html')
def edit_ticket():
    return render_template('/edit_ticket.html')


@app.route('/Calendar.html')
def view_calendar():
    return render_template('/Calendar.html')

@app.route('/Calendar_staff.html')
def view_calendar_staff():
    return render_template('/Calendar_staff.html')

@app.route('/transaction vendeur-client.html')
def transactionvc():
    return render_template('/transaction vendeur-client.html')

@app.route('/payment.html')
def panierconfirm():
    return render_template('/payment.html')

@app.route('/cardpaymentvisa.html')
def visa():
    return render_template('/cardpaymentvisa.html')

@app.route('/cardpaymentmc.html')
def mastercard():
    return render_template('/cardpaymentmc.html')

@app.route('/cardpaymentamex.html')
def amex():
    return render_template('/cardpaymentamex.html')

@app.route('/cardpaiementcartecadeau.html')
def cadeau():
    return render_template('/cardpaiementcartecadeau.html')

@app.route('/orderplaced.html')
def order():
    return render_template('/orderplaced.html')

@app.route('/meilleureoffre.html')
def meilleureoffre():
    return render_template('/meilleureoffre.html')


# api to add item to db
# expects json file with price, stockleft, kind, sale, size
@app.route('/add_item', methods=['POST'])
@cross_origin(supports_credentials=True)
def add_item():
    nom = request.json['name']
    pri = request.json['price']
    stock = request.json['stockleft']
    kind = request.json['kind']
    sale = ''
    if request.json['sale'] == "True" or request.json['sale'] == "true":
        sale = True
    elif request.json['sale'] == "False" or request.json['sale'] == "false":
        sale = False
    size = request.json['size']
    if not pri or not stock or not kind or not sale or not size:
        # empty fields
        abort(400)
    newitem = Item(nom, pri, stock, kind, sale, size)
    db.session.add(newitem)
    db.session.commit()
    return "Item Added"




@app.route('/get_all_items', methods=['GET'])
def get_all_items():
    items = Item.query.all()
    success = jsonify(item_schema.dump(items))
    return success




@app.route('/edit_orders.html')
def view_edit_orders():
    return render_template('edit_orders.html')



# api to add user to db
# expects json file with username , password , mail , dob and gender fields create time is automatic
@app.route('/add_user', methods=['POST'])
@cross_origin(supports_credentials=True)
def add_user():
    name = request.json['username']
    pwd = request.json['password']
    mail = request.json['mail']
    dob = request.json['dob']
    gender = request.json['gender']
    if not name or not pwd or not dob or not mail:
        # name is empty or pwd is empty
        abort(400)
    # check for unique name
    not_unique = User.query.filter_by(username=name).first()
    # similar username exists
    if not_unique:
        abort(403)
    else:
        newuser = User(name, pwd, mail, dob, gender)
        db.session.add(newuser)
        db.session.commit()
        sender = 'serenackhayef@gmail.com'
        recipients = [mail]
        subject = "Bienvenue chez Omnes MarketPlace"
        msg = Message(subject, sender=sender, recipients=recipients)
        msg.body = "Merci d'avoir rejoins Omnes MarketPlace, " + name + " \n On espere que vous allez apprécier notre site. \n N'oubliez pas de visiter nos articles. \n  Omnes MarketPlace Team. "
        #Email.send(msg)

        return "success"


@app.route('/view_info', methods=['POST'])
@cross_origin(supports_credentials=True)
def view_info():
    if request.json["token"] is None:
        abort(403)
    my_id = decode_token(request.json["token"])
    user = User.query.filter_by(id=my_id).first()
    x = {
        "username": user.username,
        "mail": user.mail,
        "dob": user.dob,
        "id": user.id,
        "date_joined": user.date_joined,
        "gender": user.gender
    }

    return jsonify(x)


# api to authenticate user on log in
# expects username and password
# returns token
@app.route('/authentication', methods=['POST'])
def authenticate():
    usname = request.json['username']
    pwd = request.json['password']
    if not id or not pwd:
        abort(400)
    user_db = User.query.filter_by(username=usname).first()
    # no username exists
    if user_db is None:
        abort(403)
    # password don't match
    if not bcrypt.check_password_hash(user_db.password, pwd):
        abort(403)
    # create token
    token = create_token(user_db.id)
    return jsonify({"token": token})


@app.route('/authentication_staff', methods=['POST'])
@cross_origin(supports_credentials=True)
def authenticate_staff():
    staff_username = request.json['username']
    pwd = request.json['password']
    if not id or not pwd:
        abort(400)
    staff_db = Staff.query.filter_by(username=staff_username).first()
    # no username exists
    if staff_db is None:
        abort(403)
    # password don't match
    if not bcrypt.check_password_hash(staff_db.password, pwd):
        abort(403)
    # create token
    token = create_token(staff_db.id)
    return jsonify({"token": token})


@app.route('/check_staff', methods=['POST'])
@cross_origin(supports_credentials=True)
def check_staff():
    if request.json["token"] is None:
        abort(403)
    signed_in_ID = decode_token(request.json["token"])

    staff = Staff.query.filter_by(id=signed_in_ID).first()
    user = User.query.filter_by(id=signed_in_ID).first()

    return jsonify({'staffCheck': staff is not None})


@app.route('/view_info_staff', methods=['POST'])
@cross_origin(supports_credentials=True)
def view_info_admin():
    if request.json["token"] is None:
        abort(403)
    my_id = decode_token(request.json["token"])
    admin = Staff.query.filter_by(id=my_id).first()
    x = {
        "username": admin.username,
        "mail": admin.mail,
        "dob": admin.dob,
        "id": admin.id,
        "date_joined": admin.date_joined,
        "gender": admin.gender,
        "position": admin.position,
        "phone": admin.phone
    }

    return jsonify(x)


@app.route('/check_admin', methods=['POST'])
@cross_origin(supports_credentials=True)
def check_admin():
    if request.json["token"] is None:
        abort(403)
    signed_in_ID = decode_token(request.json["token"])
    admin = Staff.query.filter_by(id=signed_in_ID, position='Admin').first()

    return jsonify({'adminCheck': admin is not None})


@app.route('/logout', methods=['POST'])
@cross_origin(supports_credentials=True)
def logout():
    return "DECONNEXION REUSSIE"


def extract_auth_token(authenticated_request):
    auth_header = authenticated_request.headers.get('Authorization')
    if auth_header:
        return auth_header.split(" ")[1]
    else:
        return None



def decode_token(token):
    payload = jwt.decode(token, SECRET_KEY, 'HS256')
    return payload['sub']



def create_token(user_id):
    payload = {
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=4),
        'iat': datetime.datetime.utcnow(),
        'sub': user_id
    }
    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm='HS256'
    )


@app.route('/email', methods=['POST'])
def send_email():
    sender = 'serenackhayef@gmail.com'
    recipients = request.json["recipients"]
    subject = request.json["subject"]
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = request.json["body"]
    Email.send(msg)
    return "Message envoyé!"


@app.route('/delete_user', methods=['POST'])
def delete_account():
    username = request.json["username"]
    user_delete = User.query.filter_by(username=username).first()
    db.session.delete(user_delete)
    db.session.commit()
    x = {
        "success": "Success"
    }
    return jsonify(x)


@app.route('/all_user', methods=['GET'])
@cross_origin(supports_credentials=True)
def all_user():
    users = User.query.all()
    success = jsonify(user_schema.dump(users))
    return success


@app.route('/all_item', methods=['GET'])
@cross_origin(supports_credentials=True)
def all_item():
    items = Item.query.all()
    success = jsonify(item_schema.dump(items))
    return success



@app.route('/edit_user', methods=['POST'])
@cross_origin(supports_credentials=True)
def edit_user():
    username = request.json['username']
    field = request.json['field']
    value = request.json['value']
    field = str(field)
    # if request.json["token"] is None:
    #    abort(403)
    user = User.query.filter_by(username=username).first()
    setattr(user, field, value)
    db.session.add(user)
    db.session.commit()
    x = {
        "username": user.username,
        "field": getattr(user, field)
    }
    return jsonify(x)


@app.route('/delete_staff', methods=['POST'])
def delete_staff():
    username = request.json["username"]
    staff_delete = Staff.query.filter_by(username=username).first()
    db.session.delete(staff_delete)
    db.session.commit()
    x = {
        "succes": "Succes"
    }
    return jsonify(x)


@app.route('/delete_item', methods=['POST'])
def delete_item():
    name = request.json["name"]
    item_delete = Item.query.filter_by(name=name).first()
    db.session.delete(item_delete)
    db.session.commit()
    x = {
        "succes": "Succes"
    }
    return jsonify(x)




@app.route('/all_staff', methods=['GET'])
@cross_origin(supports_credentials=True)
def all_admin():
    admins = Staff.query.all()
    success = jsonify(staff_schema.dump(admins))
    return success


@app.route('/edit_staff', methods=['POST'])
@cross_origin(supports_credentials=True)
def edit_admin():
    username = request.json['username']
    field = request.json['field']
    value = request.json['value']
    field = str(field)
    # if request.json["token"] is None:
    #    abort(403)
    admin = Staff.query.filter_by(username=username).first()
    setattr(admin, field, value)
    db.session.add(admin)
    db.session.commit()
    x = {
        "username": admin.username,
        "field": getattr(admin, field)
    }
    return jsonify(x)


@app.route('/edit_item', methods=['POST'])
@cross_origin(supports_credentials=True)
def edit_item():
    name = request.json['name']
    field = request.json['field']
    value = request.json['value']
    field = str(field)
    # if request.json["token"] is None:
    #    abort(403)
    item = Item.query.filter_by(name=name).first()
    setattr(item, field, value)
    db.session.add(item)
    db.session.commit()
    x = {
        "name": item.name,
        "field": getattr(item, field)
    }
    return jsonify(x)


@app.route('/add_order', methods=['POST'])
def add_order():
    token = extract_auth_token(request)
    if not token or token == None:
        abort(403)
    else:

        id = decode_token(token)
        for itemid in request.json:
            order = Orders(id, itemid, request.json[itemid])
            db.session.add(order)
            item = Item.query.filter_by(id=itemid).first()
            item.stockleft -= request.json[itemid]
            db.session.commit()
        sender = 'serenackhayef@gmail.com'

        subject = "Reçu"
        user = User.query.filter_by(id=id).first()
        recipients = [user.mail]
        msg = Message(subject, sender=sender, recipients=recipients)
        name = User
        body = ""
        body += "Merci pour votre achat" + user.username + ", \n\n" + "Vous avez commander: \n"
        summary = ''
        grand_total = 0
        for itemid in request.json:
            item = Item.query.filter_by(id=itemid).first()
            order = "    -" + str(request.json[itemid]) + " " + item.name + " à " + str(
                item.price) + "$ chaqun" + " pour un total de " + str(int(request.json[itemid]) * int(item.price)) + "$ \n"
            grand_total += int(request.json[itemid]) * int(item.price)
            summary += order
        body += summary + "Total: " + str(grand_total) + "$ \n\n"
        body += "On espere que vous etes satisfaits \n" + "Omnes MarketPlace Team."
        msg.body = body
        Email.send(msg)

        return "Succes!"


@app.route('/add_staff', methods=['POST'])
@cross_origin(supports_credentials=True)
def add_staff():
    name = request.json['username']
    pwd = request.json['password']
    mail = request.json['mail']
    dob = request.json['dob']
    gender = request.json['gender']
    phone = request.json['phone']
    position = request.json['position']
    if not name or not pwd or not dob or not mail or not phone or not position:
        # name is empty or pwd is empty
        abort(400)
    else:
        newstaff = Staff(name, pwd, mail, dob, gender, phone, position)
        db.session.add(newstaff)
        db.session.commit()
        sender = 'serenackhayef@gmail.com'
        recipients = [mail]
        subject = "Bienvenue chez Omnes MarketPlace"
        msg = Message(subject, sender=sender, recipients=recipients)
        msg.body = "Merci d'avoir rejoins Omnes MarketPlace, " + name + " \nOn espere que vous allez apprécier notre site. \n N'oubliez pas de visiter nos articles. \n  Omnes MarketPlace Team. "
        Email.send(msg)
        return "success"


@app.route('/get_order_history', methods=['GET'])
def get_order_history():
    token = extract_auth_token(request)
    if not token or token == None:
        abort(403)
    else:

        id = decode_token(token)
        # get all orders
        orders = Orders.query.filter_by(user_id=id).all()
        # need to now get info about each item ordered
        ods = {}
        for order in orders:
            item = Item.query.filter_by(id=order.item_id).first()
            od = {}
            od["name"] = item.name
            od["kind"] = item.kind
            od["size"] = item.size
            od["price"] = item.price
            od["amount"] = order.amount
            od["date"] = order.order_date
            ods[order.order_id] = od
        return jsonify(ods)
        # we now have item descritption for each order


@app.route('/add_event', methods=['POST'])
@cross_origin(supports_credentials=True)
def add_event():
    if request.json["token"] is None:
        abort(403)
    my_id = decode_token(request.json["token"])
    admin = Staff.query.filter_by(id=my_id).first()
    title = request.json['title']
    event_type = request.json['event_type']
    description = request.json['description']
    time_begin = request.json['time_begin']
    time_end = request.json['time_end']
    privacy = ''
    if request.json["privacy"] == "True":
        privacy = True
    elif request.json["privacy"] == "False":
        privacy = False
    else:
        abort(400)
    last_modify = str(admin.username)
    if not title or not event_type or not time_end or not last_modify or not time_begin:
        # name is empty or pwd is empty
        abort(400)
    else:
        event = Calendar(title, event_type, description, time_begin, time_end, last_modify, privacy)
        db.session.add(event)
        db.session.commit()
        return "success"


@app.route('/edit_event', methods=['POST'])
@cross_origin(supports_credentials=True)
def edit_event():
    if request.json["token"] is None:
        abort(403)
    my_id = decode_token(request.json["token"])
    admin = Staff.query.filter_by(id=my_id).first()
    title = request.json['title']
    field = request.json['field']
    value = request.json['value']
    field = str(field)
    # if request.json["token"] is None:
    #    abort(403)
    event = Calendar.query.filter_by(title=title).first()
    setattr(event, field, value)
    event.last_modify_by = "2022-04-29"
    db.session.add(event)
    db.session.commit()
    x = {
        "title": event.title,
        "field": getattr(event, field),
        "last_modify_by": event.last_modify_by
    }
    return jsonify(x)


@app.route('/all_events_staff', methods=['GET'])
@cross_origin(supports_credentials=True)
def all_events_staff():
    events = Calendar.query.all()
    success = jsonify(calendar_schema.dump(events))
    return success


@app.route('/all_events', methods=['GET'])
@cross_origin(supports_credentials=True)
def all_events():
    events = Calendar.query.with_entities(Calendar.id, Calendar.title, Calendar.event_type, Calendar.description,
                                          Calendar.time_begin, Calendar.time_end).filter_by(privacy=0)
    success = jsonify(calendar_schema1.dump(events))
    return success

@app.route('/all_order', methods=['GET'])
def all_orders():
    od = Orders.query.all()
    return jsonify(orders_schema.dump(od))
  
  
@app.route('/edit_order',methods=['POST'])
def edit_order():
    order_id = request.json['order_id']
    field=request.json['field']
    value =request.json['value']
    order= Orders.query.filter_by(order_id=order_id).first()
    setattr(order,field,value)
    db.session.add(order)
    db.session.commit()
    return 'Success'


@app.route('/delete_order',methods=['POST'])
def delete_order():
    order = Orders.query.filter_by(order_id=request.json['order_id']).first()
    db.session.delete(order)
    db.session.commit()
    return "Success"

  
@app.route('/admin_add_order',methods=['POST'])
def admin_add_order():
    user_id=request.json['user_id']
    item_id=request.json['item_id']
    amount = request.json['amount']
    order=Orders(user_id,item_id,amount)
    db.session.add(order)
    db.session.commit()
    return "success"
 
