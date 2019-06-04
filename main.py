from flask import Flask, request
from waitress import serve
from src.planet import Planet

from flask import Flask

app = Flask(__name__)

@app.route("/planets/<string:action>", methods=['GET'])
def planets_get(action):
    """Handles the access via GET Methods.

    Returns
    ------
    Response
        JSON Response of the planets found. Or a message if couldn't find any.
    """

    actions = ['view', 'list']

    if (action in actions):
        if (action == 'list'):
            return planet_list()
        elif (action == 'view'):
            data = request.args

            return planet_view(data)


    return "Action {} not allowed".format(action), 405


@app.route("/planets/<string:action>", methods=['POST'])
def planets_post(action):
    """Handles the access via POST Methods.

    Returns
    ------
    Response, None
        JSON Response of the planets found. Or a message if couldn't find any.
    """

    actions = ['create', 'update', 'delete']

    if (action in actions):
        data = request.form

        if (action == 'create'):
            return planet_create(data)
        elif (action == 'update'):
            return planet_update(data)
        elif (action == 'delete'):
            return planet_delete(data)

    return "Action {} not allowed".format(action), 405


def planet_list():
    """Lists all Planets stored in the collection.

    Returns
    ------
    Response
        JSON Response of the planets. Or A message in case there is any.
    """

    model = Planet()
    result = model.list()

    if (result is not None):
        return result, 200

    return "No Planets Stored", 200


def planet_view(data):
    """Lists all Planets stored in the collection.

    Returns
    ------
    Response
        JSON Response of the planet. Or a message if not found.
    """

    model = Planet()
    result = model.view(data)

    if (result is not None):
        return result, 200

    return "Planet not found", 404


def planet_create(data):
    """Lists all Planets stored in the collection.

    Returns
    ------
    Response
        JSON Response of the planet created. Or a message in case of error.
    """

    model = Planet()
    result = model.create(data)

    if (isinstance(result,str)):
        return result, 400

    return result, 200


def planet_update(data):
    """Lists all Planets stored in the collection.

    Returns
    ------
    Response
        JSON Response of the planet updated. Or a message in case of error.
    """

    model = Planet()
    result = model.update(data)

    if (result is not None):
        return result, 200

    return "Planet {} not found".format(data.get("nome")), 404


def planet_delete(data):
    """Lists all Planets stored in the collection.

    Returns
    ------
    Response
        A message if the deletion succeeds.
    """

    model = Planet()
    result = model.delete(data)

    if (result is not None):
        return result, 200

    return "Planet {} not found".format(data.get("nome")), 404


serve(app, listen='0.0.0.0:5000')