import configparser
import random
import logging

def run_ini():
    config = configparser.ConfigParser()
    config.read('bot.ini')
    return config

def gen_random_int(datastructure):
    rand_int = random.randrange(len(datastructure))
    return rand_int

def system_logs():
    log_format = "[%(asctime)s] [%(levelname)s] :: %(message)s"
    logging.basicConfig(format=log_format, level=logging.INFO)
    return logging.getLogger()