import os
from dotenv import load_dotenv


if os.getenv("python_dev"):
    from dev_config import *
    load_dotenv(secret_path)
    providers_config = os.path.join(providers_path)
else:
    from .config import *
    load_dotenv("configs/secret.py")
    providers_config = os.path.join(
        os.path.abspath("."), "configs/providers.yml")

cert_handler_list= []
