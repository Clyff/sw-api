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
        JSON Response of the planets. Or a message.
    """

    actions = ['view', 'list']

    if (action in actions):
        model = Planet()

        # JSON Response of the planets. Or A message in case there is any.
        if (action == 'list'):
            result = model.list()

            if (result is not None):
                return result, 200

            return "No Planets Stored", 200

        # JSON Response of the planet. Or a message if not found.
        elif (action == 'view'):
            data = request.args
            result = model.view(data)

            if (result is not None):
                return result, 200

            return "Planet not found", 404

    # A message if route not allowed.
    return "Action {} not allowed".format(action), 405


@app.route("/planets/<string:action>", methods=['POST'])
def planets_post(action):
    """Handles the access via POST Methods.

    Returns
    ------
    Response, None
        JSON Response of the planets. Or a message.
    """

    actions = ['create', 'update', 'delete']

    if (action in actions):
        model = Planet()
        data = request.form

        # JSON Response of the planet created. Or a message in case of error.
        if (action == 'create'):
            result = model.create(data)

            if (isinstance(result,str)):
                return result, 400

            return result, 200

        # JSON Response of the planet updated. Or a message in case of error.
        elif (action == 'update'):
            result = model.update(data)

            if (result is not None):
                return result, 200

            return "Planet {} not found".format(data.get("nome")), 404

        # A message whether the deletion succeed or not.
        elif (action == 'delete'):
            result = model.delete(data)

            if (result is not None):
                return result, 200

            return "Planet {} not found".format(data.get("nome")), 404

    # A message if route not allowed.
    return "Action {} not allowed".format(action), 405


serve(app, listen='0.0.0.0:5000')