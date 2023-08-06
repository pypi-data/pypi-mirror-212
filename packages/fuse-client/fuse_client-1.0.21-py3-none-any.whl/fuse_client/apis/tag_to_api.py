import typing_extensions

from fuse_client.apis.tags import TagValues
from fuse_client.apis.tags.fuse_api import FuseApi
from fuse_client.apis.tags.spend_power_api import SpendPowerApi

TagToApi = typing_extensions.TypedDict(
    'TagToApi',
    {
        TagValues.FUSE: FuseApi,
        TagValues.SPEND_POWER: SpendPowerApi,
    }
)

tag_to_api = TagToApi(
    {
        TagValues.FUSE: FuseApi,
        TagValues.SPEND_POWER: SpendPowerApi,
    }
)
