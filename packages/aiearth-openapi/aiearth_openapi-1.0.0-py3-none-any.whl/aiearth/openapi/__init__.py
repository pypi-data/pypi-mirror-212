from alibabacloud_tea_openapi.models import Config
from alibabacloud_aiearth_engine20220609.client import Client
from aiearth.core.client.endpoints import Endpoints

__ENDPOINT__ = Endpoints.OPENAPI_ENDPOINT
__REGION_ID__ = Endpoints.OPENAPI_REGION_ID

__version__ = "1.0.0"

def build_client(access_key_id, access_key_secret, endpoint=__ENDPOINT__):
    config = Config(
        access_key_id=access_key_id,
        access_key_secret=access_key_secret,
        region_id=__REGION_ID__,
        endpoint=endpoint
    )

    return Client(config)
