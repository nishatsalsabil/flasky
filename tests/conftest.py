import pytest
from app import create_app
from app import db
from flask.signals import request_finished
from app.models.cars import Car


@pytest.fixture
def app():
    app = create_app({"TESTING": True})

    @request_finished.connect_via(app)
    def expire_session(sender, response, **extra):
        db.session.remove()

    with app.app_context():
        db.create_all()
        yield app

    with app.app_context():
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def two_saved_cars(app):
    # Arrange
    aniq_car = Car(driver="Aniq", team="BMW", mass_kg=654)
    fatima_car = Car(driver="Fatima", team="Toyota", mass_kg=498)

    db.session.add_all([aniq_car, fatima_car])
    # Alternatively, we could do
    # db.session.add(aniq_car)
    # db.session.add(fatima_car)
    db.session.commit()


@pytest.fixture
def seven_cars(app):
    car1 = Car(id=1, driver='Danny Ric', team='McLaren', mass_kg=800)
    car2 = Car(id=2, driver='Carlos', team='Ferrari', mass_kg=750)
    car3 = Car(id=3, driver='driver name 3', team='McLaren', mass_kg=700)
    car4 = Car(id=4, driver='driver name 4', team='Mercedes', mass_kg=750)
    car5 = Car(id=5, driver='driver name 5', team='Mercedes', mass_kg=800)
    car6 = Car(id=6, driver='driver name 6', team='Ferrari', mass_kg=750)
    car7 = Car(id=7, driver='driver name 7', team='McLaren', mass_kg=800)

    db.session.add(car1)
    db.session.add(car2)
    db.session.add(car3)
    db.session.add(car4)
    db.session.add(car5)
    db.session.add(car6)
    db.session.add(car7)

    db.session.commit()