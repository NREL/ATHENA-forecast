import json
import os
import logging

logger = logging.getLogger(__name__)

def get_api_key():
    """ Returns the Tom Tom API key from credentials file"""

    cred_file = os.path.join( os.environ['ATHENA_CREDENTIALS_PATH'], "athena_tom_tom.json")
    # Load credentials
    try: 
        credentials = json.loads(open(cred_file).read())
        return credentials.get("api_key")
    except FileNotFoundError:
        if not cache:
            logger.error('You need the following credentials \
                        file {} to access the tom tom data'.format(cred_file))
