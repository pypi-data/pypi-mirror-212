from hypothesis import given

from anaml_client.models import *
from generators import CredentialsProviderConfigGen


@given(CredentialsProviderConfigGen)
def test_credentials_provider_config_round_trip(config: CredentialsProviderConfig):
    assert config == CredentialsProviderConfig.from_json(config.to_json())
