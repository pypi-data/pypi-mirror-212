import sys
if tuple(sys.version_info[:2]) >= (3, 9):
    # Python 3.9 and above
    from typing import Annotated
else:
    # Python 3.8 and below
    from typing_extensions import Annotated

from pydantic import BaseModel,Field # pylint: disable=no-name-in-module
from typing import Optional, Dict, List, Literal, Union
from .rate_limiting import ApiLimits, RateLimitState
from .configuration import InboundSyncStreamsConfiguration, OutboundSyncStrategy, StoredConfigurationValue, StoredFieldMappings
from .omnata_plugin import PluginManifest

class OutboundApplyPayload(BaseModel):
    """
    Encapsulates the payload that is sent to the plugin when it is invoked to perform an outbound sync.
    """
    sync_id:int # only used by log handler
    sync_branch_id:Optional[int] # only used by log handler
    connection_id:int # only used by log handler
    run_id:int # used by log handler and for reporting back run status updates
    source_app_name:str # the name of the app which is invoking this plugin
    results_schema_name:str # the name of the schema where the results table resides
    results_table_name:str # used to stage results back to the engine, resides in the main Omnata app database
    logging_level:str
    connection_method:str
    connection_parameters:Dict[str,StoredConfigurationValue]
    oauth_secret_name:Optional[str]
    other_secrets_name:Optional[str]
    sync_direction:Literal["outbound"] = 'outbound'
    sync_strategy:OutboundSyncStrategy
    sync_parameters:Dict[str,StoredConfigurationValue]
    api_limit_overrides:List[ApiLimits]
    rate_limits_state:Dict[str, RateLimitState]
    field_mappings:StoredFieldMappings

class InboundApplyPayload(BaseModel):
    """
    Encapsulates the payload that is sent to the plugin when it is invoked to perform an inbound sync.
    """
    sync_id:int # only used by log handler
    sync_branch_id:Optional[int] # only used by log handler
    connection_id:int # only used by log handler
    run_id:int # used by log handler and for reporting back run status updates
    source_app_name:str # the name of the app which is invoking this plugin
    results_schema_name:str # the name of the schema where the results table resides
    results_table_name:str # used to stage results back to the engine, resides in the main Omnata app database
    logging_level:str
    connection_method:str
    connection_parameters:Dict[str,StoredConfigurationValue]
    oauth_secret_name:Optional[str]
    other_secrets_name:Optional[str]
    sync_direction:Literal["inbound"] = 'inbound'
    sync_parameters:Dict[str,StoredConfigurationValue]
    api_limit_overrides:List[ApiLimits]
    rate_limits_state:Dict[str, RateLimitState]
    streams_configuration:InboundSyncStreamsConfiguration
    latest_stream_state:Dict

ApplyPayload = Annotated[Union[OutboundApplyPayload,InboundApplyPayload],Field(discriminator='sync_direction')]

class PluginInfo(BaseModel):
    """
    Manifest plus other derived information about a plugin which is determined during upload.
    """
    manifest: PluginManifest
    anaconda_packages:List[str]
    bundled_packages:List[str]
    icon_source: Optional[str]
    plugin_class_name: str
    transformer_class_name: Optional[str]
    package_source: Literal['function','stage']
