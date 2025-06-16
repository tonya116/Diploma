import configparser
import os


class Config:
    def __init__(self):

        self.config = configparser.ConfigParser()
        self.config.read(os.getcwd() + "/python/config.ini")

    def __call__(self, key):
        return self.config['DEFAULT'].get(key)

config = Config()
