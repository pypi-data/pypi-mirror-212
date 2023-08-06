# Binance API Python Wrapper

This is a Python wrapper for the Binance API, providing convenient methods to interact with various endpoints of the Binance API.

## Installation

To use this wrapper, you'll need Python 3.6 or above. Clone the repository and install the required dependencies using pip:

```shell
git clone https://github.com/your-username/binance-api-python-wrapper.git
cd binance-api-python-wrapper
pip install -r requirements.txt
```

## Usage

1. Import the `BinanceAPI` class:

```python
from binance_api import BinanceAPI
```

2. Create an instance of the BinanceAPI class by providing your Binance API key and secret:

```python
api_key = 'YOUR_API_KEY'
api_secret = 'YOUR_API_SECRET'

bn = BinanceAPI(api_key, api_secret)
```

3. Use the available methods to interact with the Binance API. For example, to search for advertisements:

```python
ads = bn.search_ads("BTC", "GBP", "BUY")
print(ads)
```

4. Refer to the docstrings in the code for detailed information about each method, including arguments and return values.

## Disclaimer
This project is provided as-is and is not affiliated with or endorsed by Binance. Use it at your own risk.
