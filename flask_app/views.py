from flask import request, Response
from flask_app import app, db, DB_TYPE, rabbit_channels
from transactions.Booking import get_showing_detail, get_showings, select_seats_post, tickets_put, test_post, get_bookings_from_email, delete_booking_by_id
from transactions.Offer import seats_post, halls_post, showings_post
from utils.Generators import generate_response
from utils.Response_codes import *
from DAOs.DAOFactory import DAOFactory, SQLAlchemyDAOFactory

dao_factory: DAOFactory

if DB_TYPE == 'SQLAlchemy':
    dao_factory = SQLAlchemyDAOFactory(db)
else:
    raise NotImplementedError("Can't handle database type: {}".format(DB_TYPE))


@app.route('/test', methods=['POST'])
def booking():
    if request.method == 'POST':
        return test_post(dao_factory, request, rabbit_channels.channel_publisher)
    else:
        return generate_response('HTTP method {} is not supported'.format(request.method), Status_code_not_found)


@app.route('/offer/halls', methods=['POST'])
def offer_halls():
    if request.method == 'POST':
        return halls_post(dao_factory, request)
    else:
        return generate_response('HTTP method {} is not supported'.format(request.method), Status_code_not_found)


@app.route('/offer/seats', methods=['POST'])
def offer_seats():
    if request.method == 'POST':
        return seats_post(dao_factory, request)
    else:
        return generate_response('HTTP method {} is not supported'.format(request.method), Status_code_not_found)


@app.route('/offer/showings', methods=['POST'])
def offer_showings():
    if request.method == 'POST':
        return showings_post(dao_factory, request)
    else:
        return generate_response('HTTP method {} is not supported'.format(request.method), Status_code_not_found)


@app.route('/showings/<movie_id>', methods=['GET'])
def showings(movie_id):
    if request.method == 'GET':  # here goes plenty of query parameters
        from_date = request.args.get('from_date')
        to_date = request.args.get('to_date')
        movie_language = request.args.get('movie_language')
        dubbing_language = request.args.get('dubbing_language')
        subtitles_language = request.args.get('subtitles_language')
        lector_language = request.args.get('lector_language')
        age_limit = request.args.get('age_limit')
        return get_showings(dao_factory, request, from_date, to_date, movie_id, movie_language, dubbing_language,
                            subtitles_language, lector_language, age_limit)
    else:
        return generate_response('HTTP method {} is not supported'.format(request.method), Status_code_not_found)


@app.route('/showings/detail/<showing_id>', methods=['GET'])
def showings_detail(showing_id):
    if request.method == 'GET':
        return get_showing_detail(dao_factory, request, showing_id)
    else:
        return generate_response('HTTP method {} is not supported'.format(request.method), Status_code_not_found)


@app.route('/select_seats', methods=['POST'])
def select_seats():
    if request.method == 'POST':
        return select_seats_post(dao_factory, request, rabbit_channels.channel_publisher)
    else:
        return generate_response('HTTP method {} is not supported'.format(request.method), Status_code_not_found)


@app.route('/tickets', methods=['PUT'])
def create_tickets():
    if request.method == 'PUT':
        return tickets_put(dao_factory, request)
    else:
        return generate_response('HTTP method {} is not supported'.format(request.method), Status_code_not_found)


@app.route('/bookings/<booking_id>', methods=['DELETE'])
def delete_booking(booking_id):
    if request.method == 'DELETE':
        return delete_booking_by_id(dao_factory, request, rabbit_channels.channel_publisher, booking_id)
    else:
        return generate_response('HTTP method {} is not supported'.format(request.method), Status_code_not_found)


@app.route('/bookings/<email>', methods=['GET'])
def get_bookings(email):
    if request.method == 'GET':
        return get_bookings_from_email(dao_factory, email)
    else:
        return generate_response('HTTP method {} is not supported'.format(request.method), Status_code_not_found)


@app.route('/payment_completed/<successful>', methods=['PUT'])
def payment_completed(successful):
    if request.method == 'PUT':
        return generate_response('Endpoint not yet implemented', Status_code_not_found)
    else:
        return generate_response('HTTP method {} is not supported'.format(request.method), Status_code_not_found)
