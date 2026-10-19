import configparser

config = configparser.ConfigParser()

config.read("config.ini")

nom_application = config["APPLICATION"]["nom"]

print(nom_application)