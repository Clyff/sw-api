import requests
import urllib.parse
from flask import jsonify
from bson import ObjectId
from src.client import Client

class Planet():
    """
    A class used to handle the MongoDB Collection 'planets'

    ...

    Attributes
    ----------
    client : MongoDB Client
    collection : MongoDB Collection

    Methods
    -------
    list()
        Returns all items in the collection.
    view(args)
        Returns a single item in the collection.
    create(args)
        Creates a single item in the collection.
    update(args)
        Updates a single item in the collection.
    delete(args)
        Deletes a single item in the collection.
    check_planet_by_name(nome)
        Performs a search for a item in the collection.
    check_planet_by_id(id)
        Performs a search for a item in the collection.
    check_planet_by_math(match)
        Performs a search for a item in the collection.
    get_film(nome)
        Performs a search using the swapi for how many SW films that planet appears.
    """

    def __init__(self):
        self.client = Client()
        self.collection = self.client.db["planets"]


    def list(self):
        """Returns all items in the collection.

        Returns
        ------
        Response, None
            JSON Response of the planets found. Or None if could not find any.
        """

        planets = []

        for planet in self.collection.aggregate([
            {"$project": {"_id": {"$toString": "$_id"}, "nome": "$nome", "clima": "$clima", "terreno": "$terreno"}}
        ]):
            planet["filmes"] = self.get_film(planet["nome"])
            planets.append(planet)

        if (planets):
            return jsonify(planets)

        return None


    def view(self, args):
        """Returns a single item in the collection.

        Parameters
        ----------
        args : dict
            A dictionary with the following format:
            {
                "nome": str # name of the planet (optional)
                "id": str # id of the planet (optional)
            }

        Returns
        ------
        Response, None
            JSON Response of the planet found. Or None if could not find it.
        """

        planet = self.check_planet_by_name(args.get("nome"))

        if (planet is None):
            planet = self.check_planet_by_id(args.get("id"))

        return planet


    def create(self, args):
        """Creates a single item in the collection.

        Parameters
        ----------
        args : dict
            A dictionary with the following format:
            {
                "nome": str # name of the planet (obrigatory)
                "clima": str # climate of the planet (optional)
                "terreno" str # terrain of the planet (optional)
            }

        Returns
        ------
        Response, str
            JSON Response of the planet created. Or error message.
        """

        planet = self.check_planet_by_name(args.get("nome"))

        if (planet is not None):
            return "Planet with nome {} already exists".format(args.get("nome"))

        if (args.get("nome")):
            data = {
                "nome": args.get("nome"),
                "clima": args.get("clima"),
                "terreno": args.get("terreno")
            }

            self.collection.insert_one(data)

            return self.check_planet_by_name(args.get("nome"))

        return "Missing argument: 'nome'"


    def update(self, args):
        """Updates a single item in the collection.

        Parameters
        ----------
        args : dict
            A dictionary with the following format:
            {
                "nome": str # name of the planet (obrigatory)
                "clima": str # climate of the planet (optional)
                "terreno" str # terrain of the planet (optional)
            }

        Returns
        ------
        Response, None
            JSON Response of the planet updated. Or None if could not find it.
        """

        planet = self.check_planet_by_name(args.get("nome"))

        if (planet is not None):
            data = {}

            if (args.get("clima")):
                data["clima"] = args.get("clima")
            if (args.get("terreno")):
                data["terreno"] = args.get("terreno")

            if (data):
                self.collection.update_one(
                    {"nome": args.get("nome")},
                    {"$set": data}
                )

            return self.check_planet_by_name(args.get("nome"))

        return None


    def delete(self, args):
        """Deletes a single item in the collection.

        Parameters
        ----------
        args : dict
            A dictionary with the following format:
            {
                "nome": str # name of the planet
            }

        Returns
        ------
        str, None
            A Successful message. Or None if the item doesn't exist in the collection.
        """

        planet = self.check_planet_by_name(args.get("nome"))

        if (planet is not None):
            self.collection.delete_one({"nome": args.get("nome")})

            return "{} is deleted.".format(args.get("nome"))

        return None


    def check_planet_by_name(self, nome):
        """Performs a search for a item in the collection.

        Parameters
        ----------
        nome : str
            The name of the Planet we want to search

        Returns
        ------
        Response, None
            JSON Response of the planet found. Or None if could not find any.
        """

        if (bool(nome and nome.strip() and nome is not None)):
            return self.check_planet_by_match({"nome": nome})

        return None


    def check_planet_by_id(self, id):
        """Performs a search for a item in the collection.

        Parameters
        ----------
        id : str
            The id of the Planet we want to search

        Returns
        ------
        Response, None
            JSON Response of the planet found. Or None if could not find any.
        """

        if (bool(ObjectId.is_valid(id) and id is not None)):
            return self.check_planet_by_match({"_id": ObjectId(id)})

        return None


    def check_planet_by_match(self, match):
        """Performs a search for a item in the collection.

        Parameters
        ----------
        match : dict
            Match used for search in MongoDB.

        Returns
        ------
        Response, None
            JSON Response of the planet found. Or None if could not find any.
        """

        for planet in self.collection.aggregate([
            {"$match": match},
            {"$project": {"_id": {"$toString": "$_id"}, "nome": "$nome", "clima": "$clima", "terreno": "$terreno"}}
        ]):
            if (planet is not None):
                planet["filmes"] = self.get_film(planet["nome"])

                return jsonify(planet)

        return None


    def get_film(self, nome):
        """Performs a search using the swapi for how many SW films that planet appears.

        Parameters
        ----------
        nome : str
            Name of the planet we want to search.

        Returns
        ------
        int
            Number of times this planet appears in the SW Movies.

        Raises
        ------
        HTTPError
            If the connection with swapi could not be stabilized.
        """

        nome = urllib.parse.quote(str(nome), safe='')
        url = "https://swapi.co/api/planets/?search=" + nome
        myResponse = requests.get(url)

        if (myResponse.ok):
            planets = myResponse.json()

            if (planets["count"] > 0):
                for planet in planets["results"]:
                    if (planet["name"] == nome):
                        return len(planet["films"])

            return 0

        else:
            myResponse.raise_for_status()
