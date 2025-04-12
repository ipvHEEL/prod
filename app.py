from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from sqlalchemy.exc import SQLAlchemyError
import logging

# Настройка логирования
logging.basicConfig(
    level=logging.DEBUG,  # Уровень логирования (DEBUG для подробной информации)
    format='%(asctime)s - %(levelname)s - %(message)s',  # Формат вывода
    handlers=[
        logging.FileHandler('app.log'),  # Запись в файл
        logging.StreamHandler()  # Также выводить в консоль
    ]
)
app = Flask(__name__)

# Настройка базы данных MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/alp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'key'

# Инициализация базы данных
db = SQLAlchemy(app)
class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(300), nullable=True)
    def __repr__(self):
        return f'<Service {self.name}>'

# Модель данных для заявок
class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    FIO = db.Column(db.String(200), nullable=False)
    Number = db.Column(db.String(15), nullable=False)

    def __repr__(self):
        return f'<Application {self.FIO} - {self.Number}>'

# Инициализация админки
admin = Admin(app, name='Админ панель', template_mode='bootstrap3')
admin.add_view(ModelView(Application, db.session))
admin.add_view(ModelView(Service, db.session))


# Главная страница с формой для заявки
@app.route('/', methods=['GET', 'POST'])
def index():
    services = Service.query.all()  # Получаем все услуги из БД

    if request.method == 'POST':
        try:
            fio = request.form['fio']
            number = request.form['number']
            logging.debug(f"Received form data: FIO={fio}, Number={number}")

            new_application = Application(FIO=fio, Number=number)
            db.session.add(new_application)
            db.session.commit()

            logging.info("Application successfully submitted!")
            return redirect('/')
        except Exception as e:
            logging.error(f"Error processing form submission: {e}", exc_info=True)
            return render_template('index.html', error="Произошла ошибка. Попробуйте снова.", services=services)

    return render_template('index.html', services=services)




if __name__ == "__main__":
    app.run(debug=True)
