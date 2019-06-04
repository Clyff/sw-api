# SW-API
My Star Wars based API


## Requisites

You need this softwares and modules instaled in your machine to run this application:

- [Git](https://git-scm.com/download)
- [Python >= 3.5.2](https://www.python.org/downloads/)
- [Virtualenv >= 16.6.0](https://virtualenv.pypa.io/en/latest/installation/)
- [MongoDB >= V4.0.10](https://docs.mongodb.com/manual/installation/)

## Instalation

1. Download the repository:
```sh
$ git clone git@github.com:Clyff/sw-api.git
$ cd sw-api
```

2. Create a virtual enviroment and activactivate it:
```sh
$ virtualenv env
$ source env/bin/activate
```

3. Within the enviroment, install the packages:
```sh
$ pip install -r requirements.txt
```

4. Start mongodb (if not already started at boo) and run the application:
```sh
$ sudo service mongod start
$ python main.py
```

## Usage

The following routes ar avaliable (all under the port 5000):

- **/planets/list**: Returns a list of all Planets stored in the collection.
- **/planets/view**: Returns a specific Planet based on url parameters. Avaliable GET parameters: `nome` and `id`.
- **/planets/create**: Creates a Planet, if the name is avaliable, and return it. Avaliable POST parameters: `nome` (obrigatory), `clima` and `terreno`.
- **/planets/update**: Updates a existing Planet and return it. Avaliable POST parameters: `nome` (obrigatory), `clima` and `terreno`.
- **/planets/delete**: Deletes a specific Planet based on POST parameters. Avaliable POST parameters: `nome` (obrigatory).


## Docs

List of documentations used to create this application:

- [Flask](http://flask.pocoo.org/)
- [MongoDB](https://docs.mongodb.com/manual/)
- [PyMongo](https://api.mongodb.com/python/current/tutorial.html)
- [Documenting Python Code](https://realpython.com/documenting-python-code/)
