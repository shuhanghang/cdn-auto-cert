import os

if os.getenv("cdn_auto_cert_env","prod") == "dev":
    from .dev_config import *
    providers_config = os.path.join(os.path.abspath("."), "config/dev-providers.yml")
else:
    from .config import *
    providers_config = os.path.join(os.path.abspath("."), "config/providers.yml")