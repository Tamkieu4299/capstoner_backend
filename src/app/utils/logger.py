import logging


def setup_logger(name) -> logging.Logger:
    FORMAT = "[%(name)s %(module)s:%(lineno)s]\n\t %(message)s \n"
    TIME_FORMAT = "%d.%m.%Y %I:%M:%S %p"

    logging.basicConfig(
        format=FORMAT,
        datefmt=TIME_FORMAT,
        level=logging.DEBUG,
        filename="/var/logs/debug.log",
        # This path is used for local
        # filename="./logs/debug.log",
    )

    logger = logging.getLogger(name)
    return logger
