from app import db
from app.models.drivers import Driver
from app.models.cars import Car 
from .cars import validate_car
from flask import Blueprint, jsonify, make_response, request, abort 

drivers_bp = Blueprint("drivers", __name__, url_prefix="/drivers")


@drivers_bp.route("", methods=["POST"])
def create_driver():
    request_body = request.get_json()

    new_driver = Driver(
        name=request_body["name"],
        team=request_body["team"],
        country=request_body["country"],
        handsome=request_body["handsome"]
        )

    db.session.add(new_driver)
    db.session.commit()

    return {
        "id": new_driver.id
    }, 201


@drivers_bp.route("", methods=["GET"])
def get_all_drivers():
    response = []
    drivers = Driver.query.all()

    for driver in drivers:
        response.append(
            driver.to_dict()
        )

    return jsonify(response)

# helper function:
def validate_driver(driver_id):
    try:
        driver_id = int(driver_id)
    except ValueError:
        abort(make_response({"message":f"driver {driver_id} invalid"}, 400))

    chosen_driver = Driver.query.get(driver_id)

    if chosen_driver is None:
        abort(make_response({"message":f"driver {driver_id} not found"}, 404))

    return chosen_driver


@drivers_bp.route("/<driver_id>", methods=["GET"])
def get_one_driver(driver_id):

    driver = validate_driver(driver_id)

    return jsonify(driver.to_dict()), 200


@drivers_bp.route("/<driver_id>/cars", methods=["POST"])
def add_cars_to_driver(driver_id):
    driver = validate_driver(driver_id)
    request_body = request.get_json()

    try:
        car_ids = request_body["car_ids"]
    except TypeError:
        return jsonify({'msg': f"Missing car_ids in request body"}), 400
    
    if not isinstance(car_ids, list):
        return jsonify({'msg': f"Expected list of car ids"}), 400

    cars = []
    for id in car_ids:
        cars.append(validate_car(id))

    for car in cars:
        car.driver = driver
    
    db.session.commit()

    return jsonify({'msg': f"Added cars to driver {driver_id}"}), 200


