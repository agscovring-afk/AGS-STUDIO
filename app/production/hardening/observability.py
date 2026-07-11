import logging

logging.basicConfig(
filename="logs/production.log",
level=logging.INFO
)

def log(message):
    logging.info(message)
