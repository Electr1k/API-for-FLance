from flask import Flask, session
from flask_restful import Api, Resource, reqparse
from models import *
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config['JSON_AS_UTF-8'] = True
app.secret_key = 'YOUR_KEY'  # key for session
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///establishments.db'  # база данных: общая информация по заведениям
app.config['SQLALCHEMY_BINDS'] = {
    'establishments_full_info': 'sqlite:///establishments_full_info.db',  # база данных: Полная информация по заведениям
    'users': 'sqlite:///users.db'  # база данных: Для авторизации(юзеры)
}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
db.init_app(app)
api = Api()


# класс для получения запросов по общей информации о заведениях (только get запрос)
class RestList(Resource):
    def get(self):
        # создает JSON список с ресторанами путем обращения к бд establishments.db
        establishments = Establishments.query.all()  # все заведения из бд
        data = {"establishments": []}  # создание словоря
        for establishment in establishments:  # заполнение словаря заведенями
            data["establishments"].append({
                "id": establishment.id,
                "name": establishment.name,
                "address": establishment.address,
                "url_preview_img": establishment.url_preview_img,
                "lat_for_map": establishment.lat_for_map,
                "lng_for_map": establishment.lng_for_map
            })
        print(data["establishments"][0])
        return data
        # по запросу возвращает JSON словарь


# класс для получения запросов о получении информации о конкретном завдедении (только get запрос).
class LoadRest(Resource):
    def get(self, id):
        establishment = EstablishmentsFullInfo.query.filter_by(id=id).first()  # получение обьекта класса нужного заведения по id
        data = {  # создание словаря из данных о обьекте
            "id": establishment.id,
            "name": establishment.name,
            "address": establishment.address,
            "url_preview_img": establishment.url_preview_img,
            "url": establishment.url,
            "description": establishment.description,
            "prices": establishment.prices,
            "wifi": establishment.wifi,
            "battery": establishment.battery,
            "silence": establishment.silence,
            "cashless_payment": establishment.cashless_payment,
            "time_work": establishment.time_work,
            "booking": establishment.booking
        }
        return data
        # возвращает словарь JSON


# класс для регистрации нового пользователя (только post запрос). Обращаться по http://127.0.0.1:3000/register/
class UsersRegister(Resource):
    def post(self):
        # объявляет необходимые аргументы в теле запроса name, surname, email...
        parser = reqparse.RequestParser()
        parser.add_argument("name", type=str)
        parser.add_argument("surname", type=str)
        parser.add_argument("email", type=str)
        parser.add_argument("password", type=str)
        arg = parser.parse_args()  # собирает все тело запроса в один словарь
        # получаем аргументы из тела запроса
        name = arg["name"]
        surname = arg["surname"]
        email = arg["email"]
        password = arg["password"]
        if Users.query.filter_by(email=email).first() is None:  # если такой емаил не зарегистрирован (нет в бд)
            # создание объекта класса с параметрами из тела запроса
            user = Users(name=name, surname=surname, email=email, password=password, booking={"list": [], "count": 0})
            adds(user)
            commits()
            return {"success": True,
                    "Comment": f'Add new user. Name: {name} Surname: {surname} Email: {email} Password: {password}'
                    }  # ответ об успешном добавлении
        else:
            return {"success": False, "Error": "This email is already registered!"}  # не удача


@app.route('/login', methods=['POST'])
def login():
    # объявляет необходимые аргументы в теле запроса name, email, password
    parser = reqparse.RequestParser()
    parser.add_argument("email", type=str)
    parser.add_argument("password", type=str)
    arg = parser.parse_args()  # собирает все тело запроса в один словарь
    email = arg["email"]
    password = arg["password"]
    x = Users.query.filter_by(email=email).first()  # ищет в бд этого юзера по емаилу
    if x is not None:  # если емаил зареган
        if x.password == password:  # если верный пароль
            session["email"] = email
            return {"success": True, "userinfo": {"name": x.name, "surname": x.surname, "email": email}}
        else:  # неверный пароль
            return {"success": False, "Error": "Wrong login or password."}
    else:  # не зареган
        return {"success": False, "Error": "Wrong login or password."}


@app.route('/logout', methods=['GET'])
def logout():
    session.pop('email', None)
    return {"success": True}


@app.route("/delete_booking", methods=['POST'])
def delete_booking():
    email = session.get("email")
    parser = reqparse.RequestParser()
    parser.add_argument("id", type=int)
    parser.add_argument("data", type=str)
    parser.add_argument("time", type=int)
    parser.add_argument("index", type=int)
    arg = parser.parse_args()  # собирает все тело запроса в один словарь
    id = arg["id"]
    data = arg["data"]
    time = arg["time"]
    index = arg["index"]
    if 'email' in session:
        x = Users.query.filter_by(email=email).first().booking
        count = x["count"]
        x["list"].pop(index)
        setattr(Users.query.filter_by(email=email).first(), 'booking', {"list": x["list"], "count": count-1})
        x = EstablishmentsFullInfo.query.filter_by(id=id).first().booking
        x[data].pop(x[data].index(time))
        print(x)
        print()
        setattr(EstablishmentsFullInfo.query.filter_by(id=id).first(), 'booking', x)
        commits()
        bookingUser = Users.query.filter_by(email=email).first().booking
        return {"success": True, "booking": bookingUser}
    else:
        return {"success": False, "Error": "Oops, looks like you're not logged in."}


@app.route('/new_booking', methods=['POST'])
def new_booking():
    if 'email' in session:
        parser = reqparse.RequestParser()
        parser.add_argument("id", type=int)
        parser.add_argument("name", type=str)
        parser.add_argument("person", type=int)
        parser.add_argument("data", type=str)
        parser.add_argument("time", type=int)
        arg = parser.parse_args()
        email = session.get("email")
        id = arg["id"]
        name = arg["name"]
        person = arg["person"]
        data = arg["data"]
        times = arg["time"]
        mass_time = EstablishmentsFullInfo.query.filter_by(id=id).first().booking
        if times not in mass_time[str(data)]:  # провекра на уже бронированные
            mass_time[str(data)].append(times)
            setattr(EstablishmentsFullInfo.query.filter_by(id=id).first(), 'booking', mass_time)
            x = Users.query.filter_by(email=email).first().booking["list"]
            timeWork = EstablishmentsFullInfo.query.filter_by(id=id).first().time_work
            x.append({"id": id, "name": name, "person": person, "data": data, "time": times, "timeWork": timeWork})
            setattr(Users.query.filter_by(email=email).first(), 'booking', {"list": x, "count": len(x)})
            commits()
            bookingUser = Users.query.filter_by(email=email).first().booking
            return {"success": True, "booking": bookingUser}
        else:
            return {"success": False, "Error": 0}  # время занято
    else:
        return {"success": False, "Error": 1}  # пользователь не авторизован


@app.route('/my_booking', methods=['GET'])
def my_booking():
    email = session.get("email")
    if 'email' in session:
        x = Users.query.filter_by(email=email).first()
        return {"success": True, "booking": x.booking}
    else:
        return {"success": False, "Error": "Oops, looks like you're not logged in."}


api.add_resource(RestList, "/api/")
api.add_resource(LoadRest, "/api/<int:id>")
api.add_resource(UsersRegister, "/register")
api.init_app(app)

if __name__ == "__main__":
    app.run(debug=False, port=80, host="127.0.0.1")
