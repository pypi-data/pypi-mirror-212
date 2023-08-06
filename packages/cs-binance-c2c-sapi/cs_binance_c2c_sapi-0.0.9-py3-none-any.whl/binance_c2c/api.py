import requests
import hashlib
import hmac
import json


class BinanceAPI:
    BASE_URL = 'https://api.binance.com'

    def __init__(self, api_key, api_secret):
        """
        Initialize the BinanceAPI instance.

        Args:
            api_key (str): Binance API key.
            api_secret (str): Binance API secret.
        """
        self.api_key = api_key
        self.api_secret = api_secret

    def get_server_time(self):
        """
        Get the server time from the Binance API.

        Returns:
            int: Server time in milliseconds.
        """
        url = f'{self.BASE_URL}/api/v3/time'
        response = requests.get(url)
        response.raise_for_status()  # Check for successful request
        return response.json()['serverTime']

    def create_signature(self, params):
        """
        Create a signature for API authentication.

        Args:
            params (dict): Request parameters.

        Returns:
            str: Signature string.
        """
        query_string = '&'.join([f'{k}={v}' for k, v in params.items()])
        signature = hmac.new(
            self.api_secret.encode('utf-8'),
            query_string.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        return signature

    def make_request(self, method, endpoint, params={}, body_params=None):
        """
        Make a request to the Binance API.

        Args:
            method (str): HTTP method ('GET' or 'POST').
            endpoint (str): API endpoint.
            params (dict, optional): Request parameters. Defaults to {}.
            body_params (dict, optional): Request body parameters. Defaults to None.

        Returns:
            dict: Response data in JSON format.
        """
        url = f'{self.BASE_URL}{endpoint}'
        server_time = self.get_server_time()

        params = { **params, 
            'timestamp': server_time
        }

        signature = self.create_signature(params)
        params['signature'] = signature

        headers = {
            'X-MBX-APIKEY': self.api_key,
            'Content-Type': 'application/json'
        }
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, params=params)
            elif method == 'POST':
                response = requests.post(
                    url, headers=headers, params=params, data=json.dumps(body_params))
            response.raise_for_status()  # Check for successful request
        except requests.exceptions.Timeout:
            # Handle timeouts
            print("The request timed out")
        except requests.exceptions.TooManyRedirects:
            # Handle TooManyRedirects
            print("Too many redirects")
        except requests.exceptions.RequestException as e:
            # If an error occurred during the request, print out some debug information
            print("Status Code: ", response.status_code)
            print("Response Text: ", response.text)
            print("An error occurred: ", e)
            raise SystemExit(e)

        try:
            data = response.json()
        except ValueError:
            print("Error: Unable to parse JSON response")
            data = {}

        return data

    def get_ad_details(self, ad_num):
        """
        Get details of a specific advertisement.

        Args:
            ad_num (str): Advertisement number.

        Returns:
            dict: Advertisement details.
        """
        return self.make_request('POST', '/sapi/v1/c2c/ads/getDetailByNo', params={'adsNo': ad_num})['data']

    def get_messages(self, order_number, page=1, rows=10):
        """
        Get chat messages related to a specific order.

        Args:
            order_number (str): Order number.
            page (int, optional): Page number. Defaults to 1.
            rows (int, optional): Number of rows per page. Defaults to 10.

        Returns:
            dict: Chat messages.
        """
        return self.make_request('GET', '/sapi/v1/c2c/chat/retrieveChatMessagesWithPagination',
                                 params={'page': page, 'rows': rows, 'orderNo': order_number})['data']

    def retrieve_chat_credentials(self, client_type='web'):
        """
        Retrieve chat credentials for connecting to the chat WebSocket.

        Args:
            client_type (str, optional): Client type. Defaults to 'web'.

        Returns:
            dict: Chat credentials.
        """
        return self.make_request('GET', '/sapi/v1/c2c/chat/retrieveChatCredential',
                                 params={'clientType': client_type}).get('data')

    def get_order_list(self, request_body):
        """
        Get a list of orders.

        Args:
            request_body (dict): Request body parameters.

        Returns:
            dict: List of orders.
        """
        return self.make_request('POST', '/sapi/v1/c2c/orderMatch/listOrders', body_params=request_body)['data']

    def get_ads_list(self, page=1, rows=100):
        """
        Get a list of advertisements.

        Args:
            page (int, optional): Page number. Defaults to 1.
            rows (int, optional): Number of rows per page. Defaults to 100.

        Returns:
            dict: List of advertisements.
        """
        return self.make_request('POST', '/sapi/v1/c2c/ads/listWithPagination',
                                 body_params={'page': page, 'rows': rows})['data']

    def update_ad(self, adv_no, price):
        """
        Update the price of an advertisement.

        Args:
            adv_no (str): Advertisement number.
            price (str): New price.

        Returns:
            dict: Updated advertisement details.
        """
        return self.make_request('POST', '/sapi/v1/c2c/ads/update', body_params={'advNo': adv_no, 'price': price})['data']

    def search_ads(self, asset, fiat, trade_type, page=1, rows=20, filter_type='all'):
        """
        Search advertisements based on search criteria.

        Args:
            asset (str): Asset.
            fiat (str): Fiat currency.
            trade_type (str): Trade type ('BUY' or 'SELL').
            page (int, optional): Page number. Defaults to 1.
            rows (int, optional): Number of rows per page. Defaults to 20.
            filter_type (str, optional): Filter type. Defaults to 'all'.

        Returns:
            dict: List of matching advertisements.
        """

        return self.make_request('POST', '/sapi/v1/c2c/ads/search',
                                 body_params={'page': page, 'rows': rows, 'asset': asset, 'fiat': fiat,
                                              'tradeType': trade_type, 'filterType': filter_type})['data']
    
    def get_ads(self, asset, fiat, trade_type):
        """
        Get the first 2 pages of adverts in p2p market.

        Args:
            asset (str): Asset.
            fiat (str): Fiat currency.
            trade_type (str): Trade type ('BUY' or 'SELL').

        Returns:
            dict: List of matching advertisements.
        """
        ads = []
        for i in range(1, 3):
            ads += self.search_ads(asset, fiat, trade_type, i, 20, 'all')
        return ads        

    def get_order_details(self, order_number):
        """
        Get details of a specific order.

        Args:
            order_number (str): Order number.

        Returns:
            dict: Order details.
        """
        return self.make_request('POST', '/sapi/v1/c2c/orderMatch/getUserOrderDetail',
                                 body_params={'adOrderNo': order_number})['data']

    def save_to_json(self, file_name, data):
        """
        Save data to a JSON file.

        Args:
            file_name (str): File name.
            data (dict): Data to be saved.
        """
        with open(f'./json/{file_name}.json', 'w') as f:
            json.dump(data, f, indent=4)


if __name__ == "__main__":
    import os
    from dotenv import load_dotenv
    load_dotenv()
    bn = BinanceAPI(os.getenv("BINANCE_API_KEY"), os.getenv("BINANCE_API_SECRET"))
    print(bn.get_order_details("20495432379774300160"))
    print(bn.get_order_details("20495432379774300160"))
    print(bn.get_order_details("20495432379774300160"))
    print(bn.get_order_details("20495432379774300160"))