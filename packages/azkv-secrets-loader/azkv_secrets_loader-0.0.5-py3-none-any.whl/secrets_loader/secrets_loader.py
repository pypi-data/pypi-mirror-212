import os
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from azure.core.exceptions import ResourceNotFoundError

def load_secret(secret_name):
    underscore_name = secret_name.replace("-", "_")
    ev = os.getenv(underscore_name)
    if ev:
        return ev
    
    if os.getenv("TENANT_ID"):
        credential = DefaultAzureCredential(additionally_allowed_tenants=os.getenv("TENANT_ID"))
    else:
        credential = DefaultAzureCredential()

    key_vault_uri = os.getenv("KEY_VAULT_URI")
    if not key_vault_uri:
        raise Exception("Enviromental Variable KEY_VAULT_URI missing.")
    
    client = SecretClient(vault_url=key_vault_uri, credential=credential)

    dashed_name = secret_name.replace("_", "-")
    try:
        secret_value = client.get_secret(dashed_name).value
        return secret_value
    except ResourceNotFoundError:
        raise ValueError(f"Secret '{dashed_name}' not found in Azure Key Vault.")
    except Exception as e:
        raise RuntimeError(f"Failed to retrieve secret '{dashed_name}' from Azure Key Vault: {str(e)}")
