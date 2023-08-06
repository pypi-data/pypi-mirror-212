# Web3 Token implementation for python

Using this package you can verify web3 token, get signer, signed message and statement  

###  Getting it  
  
To download web3-token, either fork this github repo or simply use PyPI via pip.  
```sh
$ pip install web3-token-new
```
  
## Usage  

1 - Import  
```python
from web3_token import Web3Token
```
  
2 - Usage:  
```python
wt = Web3Token(token)

signer = wt.get_signer(validate=True)

token_data = wt.get_data()

statement = wt.statement
```
