import requests
import urllib.parse
from flask import jsonify
from bson import ObjectId
from src.client import Client

class Planet():
    def __init__(self):
        self.client = Client()
        self.collection = self.client.db["planets"]


    def list(self):
        planets = []

        for planet in self.collection.aggregate([
            {"$project": {"_id": {"$toString": "$_id"}, "nome": "$nome", "clima": "$clima", "terreno": "$terreno"}}
        ]):
            planets.append(planet)

        if (planets):
            return jsonify(planets)

        return None


    def view(self, args):
        planet = self.check_planet_by_name(args.get("nome"))

        if (planet is None):
            planet = self.check_planet_by_id(args.get("id"))

        return planet


    def create(self, args):
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
        planet = self.check_planet_by_name(args.get("nome"))

        if (planet is not None):
            self.collection.delete_one({"nome": args.get("nome")})

            return "{} is deleted.".format(args.get("nome"))

        return None


    def check_planet_by_name(self, nome):
        if (bool(nome and nome.strip() and nome is not None)):
            return self.check_planet_by_match({"nome": nome})

        return None


    def check_planet_by_id(self, id):
        if (bool(ObjectId.is_valid(id) and id is not None)):
            return self.check_planet_by_match({"_id": ObjectId(id)})

        return None


    def check_planet_by_match(self, match):
        for planet in self.collection.aggregate([
            {"$match": match},
            {"$project": {"_id": {"$toString": "$_id"}, "nome": "$nome", "clima": "$clima", "terreno": "$terreno"}}
        ]):
            if (planet is not None):
                planet["filmes"] = self.get_film(planet["nome"])

                return jsonify(planet)

        return None


    def get_film(self, nome):
        nome = urllib.parse.quote(str(nome), safe='')
        url = "https://swapi.co/api/planets/?search=" + nome
        myResponse = requests.get(url)

        if (myResponse.ok):
            planets = myResponse.json()

            if (planets["count"] > 0):
                for planet in planets["results"]:
                    if (planet["name"] == nome):
                        return planet["films"]

            return []

        else:
            myResponse.raise_for_status()
