# fuse-client

The Fuse library provides convenient access to the Fuse REST API. It is intended to be used on the server.

## Installation
```
pip3 install fuse-client
```

### Initialising the Fuse Api
```python
from fuse_client.api_client import ApiClient
from fuse_client.apis.tags.fuse_api import FuseApi
from fuse_client.configuration import Configuration

config = Configuration()
config.api_key['fuseClientId'] = 'my-fuse-client-id'
config.api_key['fuseApiKey'] = 'my-fuse-api-key'
config.host = 'fuse-base-url'

fuse_api_client = ApiClient(configuration=config)
fuse_api_instance = FuseApi(api_client=fuse_api_client)

fuse_api_client.default_headers.add("Plaid-Client-Id", 'my-plaid-client-id')
fuse_api_client.default_headers.add("Plaid-Secret", 'my-plaid-secret')
fuse_api_client.default_headers.add("Teller-Application-Id", 'my-teller-application-id')
fuse_api_client.default_headers.add("Teller-Certificate", 'my-teller-certificate')
fuse_api_client.default_headers.add("Teller-Private-Key", 'my-teller-private-key')
fuse_api_client.default_headers.add("Teller-Signing-Secret", 'my-teller-signing-secret')
fuse_api_client.default_headers.add("Mx-Api-Key", 'my-mx-api-key')
fuse_api_client.default_headers.add("Mx-Client-Id", 'my-mx-client-id')
```
<br/>

### Creating a session
```python
create_session_request = CreateSessionRequest(
	supported_financial_institution_aggregators=['plaid', 'teller', 'mx'],
	products=['account_details'],
	entity=Entity(id=str(request.user.uuid))
)

response = fuse_api_instance.create_session(body=create_session_request)

logger.info(f"{response.body.client_secret}")
```
<br/>

### Creating a link token
```python
create_link_token = CreateLinkTokenRequest(
    institution_id=institution_id,
    session_client_secret=client_secret,
    entity=entity,
    client_name="My Client Name",
)

response = fuse_api_instance.create_link_token(body=create_link_token)

logger.info(f"{response.body.link_token}")
```

<br/>

### Exchanging a public token
```python
exchange_public_token_request = ExchangeFinancialConnectionsPublicTokenRequest(public_token=public_token)

response = fuse_api_instance.exchange_financial_connections_public_token(body=exchange_public_token_request)

logger.info(f"{response.body.access_token}")
logger.info(f"{response.body.financial_connection_id}")
```
<br/>

### Getting accounts
```python
get_financial_connections_account_request = GetFinancialConnectionsAccountsRequest(access_token=access_token)

response = fuse_api_instance.get_financial_connections_accounts(body=get_financial_connections_account_request)

logger.info(f"{response.body.accounts}")
```
<br/>

### Sync financial connections data
```python
json_body = json.loads(bytes.decode(request.body))
fuse_api_instance.sync_financial_connections_data(body=json_body, header_params={
    'Fuse-Verification': request.META.get('HTTP_FUSE_VERIFICATION')
})
```
<br/>


### Building and deploying the sdk
```
python3 setup.py sdist bdist_wheel
twine upload dist/*
