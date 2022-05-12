from app import db
from app.models.cars import Car
from flask import Blueprint, jsonify, make_response, request, abort 

cars_bp = Blueprint("cars", __name__, url_prefix="/cars")

@cars_bp.route("", methods=["POST"])
def create_car():
    request_body = request.get_json()

    new_car = Car(
        driver_id=request_body["driver_id"]
        )

    db.session.add(new_car)
    db.session.commit()

    return {
        "id": new_car.id
    }, 201
    

@cars_bp.route("", methods=["GET"])
def get_all_cars():
    # params = request.args
    # if "driver" in params and "team" in params:
    #     driver_name = params["driver"]
    #     team_name = params["team"]
    #     cars = Car.query.filter_by(driver=driver_name, team=team_name)
    # elif "driver" in params:
    #     driver_name = params["driver"]
    #     cars = Car.query.filter_by(driver=driver_name)
    # elif "team" in params:
    #     team_name = params["team"]
    #     cars = Car.query.filter_by(team=team_name)
    # else:
    #     cars = Car.query.all()

    response = []
    cars = Car.query.all()
    for car in cars:
        response.append(car.to_dict())

    return jsonify(response)


# ######## helper function ########
# def validate_car(car_id):
#     try:
#         car_id = int(car_id)

#     except ValueError:
#         abort(make_response(jsonify({'msg': f"Car {car_id} is invalid"}), 400))
#         #return abort({'msg': f"Invalid car ID: '{car_id}'. ID must be an integer"}), 400

#     car = Car.query.get(car_id)

#     if car is None: 
#         abort(make_response({'msg': f"Car {car_id} not found"}, 404))

#     return car 
# ######## helper function ########


# @cars_bp.route("/<car_id>", methods=["GET"])
# def get_one_car(car_id):
#     car = validate_car(car_id)

#     return {
#             "id": car.id,
#             "driver": car.driver,
#             "team": car.team,
#             "mass_kg": car.mass_kg
#         }


# @cars_bp.route("/<car_id>", methods=["PUT"])
# def update_car(car_id):
#     car = validate_car(car_id)

#     request_body = request.get_json()

#     if "driver" not in request_body or \
#         "team" not in request_body or \
#         "mass_kg" not in request_body:
#         return jsonify({'msg': f"Request must include driver, team, and mass_kg"}), 400


#     car.driver = request_body["driver"]
#     car.team = request_body["team"]
#     car.mass_kg = request_body["mass_kg"]
    
#     db.session.commit()

#     return make_response(jsonify({'msg': f"Successfully replaced car with id {car_id}"}), 200)


# @cars_bp.route("/<car_id>", methods=["DELETE"])
# def delete_car(car_id):
#     car = validate_car(car_id)

#     db.session.delete(car)
#     db.session.commit()

#     return make_response(jsonify({'msg': f"Successfully deleted car with id {car_id}"}), 200)
#     # return make_response({'msg': f"Successfully deleted car with id {car_id}"}), 200
#     # return jsonify({'msg': f" Deleted car with id {car_id}"}), 200




######### Functions without helper function #########
@cars_bp.route("/<car_id>", methods=["GET"])
def get_one_car(car_id):
    try:
        car_id = int(car_id)
    except ValueError:
        return jsonify({'msg': f"Invalid car ID: '{car_id}'. ID must be an integer"}), 400
    
    chosen_car = Car.query.get(car_id)

    if chosen_car is None: 
        return jsonify({'msg': f"Could not find car with ID '{car_id}'"}), 404
    
    return jsonify(chosen_car.to_dict())


@cars_bp.route("/<car_id>", methods=["PATCH"])
def update_one_car(car_id):
    try:
        car_id = int(car_id)
    except ValueError:
        return jsonify({'msg': f"Invalid car ID: '{car_id}'. ID must be an integer"}), 400

    request_body = request.get_json()

    if "mass_kg" not in request_body:
        return jsonify({'msg': f"Request must include mass_kg"}), 400

    chosen_car = Car.query.get(car_id)

    if chosen_car is None: 
        return jsonify({'msg': f"Could not find car with ID '{car_id}'"}), 404

    chosen_car.mass_kg = request_body["mass_kg"]
    
    db.session.commit()

    return make_response(jsonify({'msg': f"Successfully replaced car with id {car_id}"}), 200)


@cars_bp.route("/<car_id>", methods=["DELETE"])
def delete_car(car_id):
    try:
        car_id = int(car_id)
    except ValueError:
        return jsonify({'msg': f"Invalid car ID: '{car_id}'. ID must be an integer"}), 400


    chosen_car = Car.query.get(car_id)

    if chosen_car is None: 
        return jsonify({'msg': f"Could not find car with ID '{car_id}'"}), 404

    db.session.delete(chosen_car)
    db.session.commit()

    return jsonify({'msg': f" Deleted car with id {car_id}"})




# Hardcoded data:
# class Car:
#     def __init__(self, id, driver, team, mass_kg):
#         self.id = id
#         self.driver = driver
#         self.team = team
#         self.mass_kg = mass_kg 

# cars = [
#     Car(7, "Sainz", "Ferrari", 795),
#     Car(88, "Sharles", "Ferarri", 80),
#     Car(4, "Danny Ric", "McLaren", 1138)
# # ]

# cars_bp = Blueprint("cars", __name__, url_prefix="/cars")

# @cars_bp.route("", methods=["GET"])
# def get_all_cars():
#     response = []
#     for car in cars:
#         response.append(
#             {
#                 "id": car.id,
#                 "driver": car.driver,
#                 "team": car.team,
#                 "mass_kg": car.mass_kg
#             }
#         )

#     return jsonify(response)


# @cars_bp.route("/<car_id>", methods=["GET"])
# def get_one_car(car_id):
#     try:
#         car_id = int(car_id)
#     except ValueError:
#         return jsonify({'msg': f"Invalid car ID: '{car_id}'. ID must be an integer"}), 400

#     chosen_car = None
#     for car in cars:
#         if car.id == car_id:
#             chosen_car = {
#                 "id": car.id,
#                 "driver": car.driver,
#                 "team": car.team,
#                 "mass_kg": car.mass_kg
#             }
#     if chosen_car is None:
#         return jsonify({'msg': f'Could not find car with id {car_id}'}), 404

#     return jsonify(chosen_car), 200
