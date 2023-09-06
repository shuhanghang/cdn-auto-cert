from loguru import logger


# import coloredlogs
# import logging


# def create_log():
#     logger = logging.getLogger(__name__)
#     coloredlogs.DEFAULT_FIELD_STYLES = {'asctime': {'color': 'green'}, 'funcName': {
#         'bold': True, 'color': 'magenta'}, 'levelname': {'bold': True, 'color': 'black'},
# 		'message': {'bold': True}
# 		}
#     fmt = '%(asctime)s |%(levelname)s	| %(funcName)s - %(message)s'
#     coloredlogs.install(level='INFO', logger=logger, fmt=fmt)
#     return logger


# logger = create_log()

__all__ = ['logger']