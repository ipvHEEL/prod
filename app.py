from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from sqlalchemy.exc import SQLAlchemyError
import logging

logging.basicConfig(
    level=logging.DEBUG, 
    format='%(asctime)s - %(levelname)s - %(message)s', 
    handlers=[
        logging.FileHandler('app.log'),  
        logging.StreamHandler() 
    ]
)
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/alp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'key'
db = SQLAlchemy(app)
class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    FIO = db.Column(db.String(200), nullable=False)
    Number = db.Column(db.String(15), nullable=False)

    def __repr__(self):
        return f'<Application {self.FIO} - {self.Number}>'

#              Инициализация админки/////
admin = Admin(app, name='Админ панель', template_mode='bootstrap3')
admin.add_view(ModelView(Application, db.session))

@app.route('/', methods=['GET', 'POST'])
def index():
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
            return render_template('index.html', error="Произошла ошибка. Попробуйте снова.")

    return render_template('index.html')
if __name__ == "__main__":
    app.run(debug=True)
