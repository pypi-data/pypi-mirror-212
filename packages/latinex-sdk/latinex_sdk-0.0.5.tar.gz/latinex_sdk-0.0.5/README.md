# latinex_sdk
Python SDK for basic interactions with the Latinex API

# Developed by Rodolfo Blasser 
https://www.linkedin.com/in/rodblasser/

## Usage
This is a prototype SDK and it's not being currently maintained.

## Example
```python
from latinex_sdk.generic_utils import Utilities as utils

# Test Connectivity
test = utils.whois()
print(test)

# Welcome
greetings = utils.welcome()
print(greetings)

# Register (get an API Key)
email = "example1@mail.com"
get_key = utils.register(email)
print(get_key)

# Params
fecha_inicio = "2023-05-28"
fecha_fin = "2023-06-28"
tipo_emision = "BONOS"
key = get_key[1]

# Query
data = utils.get_historic(key, fecha_inicio, fecha_fin, tipo_emision)
```
