from app.models.cars import Car

def test_get_all_cars_with_empty_db_returns_empty_list(client):
    # Act
    response = client.get("/cars")
    response_body = response.get_json()
    # Assert
    assert response.status_code == 200
    assert response_body == []


def test_get_one_car(client, two_saved_cars):
    # Act
    response = client.get("/cars/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == {
        "id": 1,
        "driver": "Aniq",
        "team": "BMW",
        "mass_kg": 654
    }


def test_get_all_cars_with_empty_db_returns_populated_list(client, seven_cars):
    # Act
    response = client.get("/cars")
    response_body = response.get_json()
    # Assert
    assert response.status_code == 200
    assert len(response_body) == 7


def test_post_one_car_creates_car_in_db(client):
    response = client.post("/cars", json={
        "driver": "Samantha",
        "team": "Fit",
        "mass_kg": 398
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 201
    #response_body = response.get_data(as_text=True) <-- only use this if in POST/books route jsonify was not added
    assert "id" in response_body
    cars = Car.query.all()
    assert len(cars) == 1
    assert cars[0].id == 1
    assert cars[0].driver == "Samantha"
    assert cars[0].team == "Fit"
    assert cars[0].mass_kg == 398


def test_get_one_car_with_empty_db_returns_404(client):
    response = client.get("/cars/1")
    assert response.status_code == 404


def test_get_one_car_with_populated_db_returns_404(client, seven_cars):
    response = client.get("/cars/100")
    assert response.status_code == 404
