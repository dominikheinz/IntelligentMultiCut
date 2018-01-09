from src.classes.models.Config import Config
class Base():

    # initiate the config object
    config = Config("config.json")

    def get_config(self):
        return self.config

