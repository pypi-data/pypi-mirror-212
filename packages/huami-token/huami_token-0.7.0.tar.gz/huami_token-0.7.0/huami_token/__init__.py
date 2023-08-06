"""
The huami_token module provides functionalities to retrieve the Bluetooth 
access token for the watch or band from Huami servers and also to download the 
AGPS data packs, cep_alm_pak.zip and cep_7days.zip.

This module consists of the following main components:
- HuamiAmazfit: A class that encapsulates all the operations related to 
  token retrieval and AGPS data downloading.
- ERRORS: A dictionary mapping error codes to their descriptions.
- URLS, PAYLOADS: Constants used for making requests to Huami servers.
"""

from .huami_token import HuamiAmazfit
from .errors import ERRORS
from .urls import URLS, PAYLOADS

__all__ = ["HuamiAmazfit", "ERRORS", "URLS", "PAYLOADS"]
