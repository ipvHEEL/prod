from app import app, db, Service  # Импортируем приложение и нужные элементы

# Открываем контекст приложения
with app.app_context():
    # Создание всех таблиц в базе данных
    db.create_all()

    # Добавление нового объекта в базу данных
    new_service = Service(name='Ремонт фасадов', description='Ремонт фасадов зданий.')
    db.session.add(new_service)
    db.session.commit()

    print("Данные успешно добавлены в базу данных!")
