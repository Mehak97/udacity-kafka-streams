import logging.config
import os
logging.config.fileConfig(f"{os.path.dirname(os.path.abspath(__file__))}/logging.ini")
