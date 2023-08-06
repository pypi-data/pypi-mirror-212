import requests
from typing import List, Dict

class GenericClient:
    """
    This client class has some generic constants/methods that we inherit in the specific client classes, e.g. ApiClient or FuturesClient.
    """
    def __init__(self):
        self.API_ENDPOINT = 'http://10.20.25.249:8000/' # internal private ip
        self.CONNECT_ERROR = 'Unable to connect to the API.\nThe IP may have changed, try updating grabngro with `pip install --upgrade grabngro`'
    
    # Generic function for simple "fetch this json and return" style requests
    def simple_get_request(self, endpoint: str):
        """Generic function for simple "fetch this json and return" style requests

        Args:
            endpoint: String representing the endpoint to hit

        """
        try:
            res = requests.get(self.API_ENDPOINT + endpoint)
        except requests.exceptions.ConnectionError:
            raise Exception(self.CONNECT_ERROR)
        res.raise_for_status()
        json = res.json()
        if isinstance(json, dict) and 'error' in json.keys():
            raise Exception(json['error'])
        return json

class ApiClient(GenericClient):
    """
    `ApiClient` is a `grabngro` API client that pulls geospatial and yield model data.

    Example:

        ```python
        client = ApiClient()

        # lists available datasets
        datasets = client.get_datasets()
        print(datasets) # ex: ['ndvi_8day', 'gdi_daily', 'lst_daily']

        # query ndvi data for a district in 2019
        client.get_by_district(district_id=140360, dataset='ndvi_8day', year=2019)

        # query gdi data for Illinois in December 2017
        client.get_by_province(province_id=13064, dataset='gdi_daily', year=2017, month=12)

        # query lst data for France from January 2017 to March 2020, inclusive
        x = client.get_by_country(country_id=1070, dataset='lst_daily', year=2017, month=1, year_until=2020, month_until=3)

        # load the result into a pandas DataFrame
        df = pd.DataFrame(x).T
        ```
    """
    
    def get_datasets(self) -> List[str]:
        """Get the datasets that are available in `ApiClient`

        The format of each string returned is `dataset_frequency`,
        e.g. `ndvi_8day` or `uscornym_daily`

        Returns:
            List of strings, where each string is a dataset that is 
            available in `ApiClient`
        """
        return self.simple_get_request('datasets')
    
    def get_by_district(self, district_id, **kwargs) -> Dict[str, Dict[str, Dict]]:
        """
        Returns data for a given district, for a given year and (optionally) month

        Example:
            ```python
            client.get_by_district(130542, dataset="LST_daily", year=2022, month=3)

            {'130542': {'2022-03-01': -3.7999999523, '2022-03-02': -3.7999999523, '2022-03-03': None,
            ...
            '2022-03-28': None, '2022-03-29': None, '2022-03-30': None, '2022-03-31': -7.3000001907}}
            ```

        Args:
            district_id (int): The `region_id` for the desired district
            dataset (str): An available dataset, as returned by `get_datasets()`
            year (int): The year for which to get data
            month (int): (Optional) the month for which to get data
            year_until (int): (Optional) the end of the year range to query. If not provided, query only data in `year`
            month_until (int): (Optional) the end of the month range to query. If not provided, query only data in `month`

        Returns:
            A dictionary where the key is the requested district and the value is a dictionary
            mapping dates to float values
        """
        return self.query('&district=%s' % district_id, **kwargs)

    def get_by_province(self, province_id, **kwargs) -> Dict[str, Dict[str, Dict]]:
        """Returns district-level data for a given province, for a given year and (optionally) month

        Example:
            ```python
            client.get_by_province(13066, dataset="NDVI_8day", year=2022)

            {'137545': {'2022-01-03': None, '2022-01-08': None, '2022-01-16': 0.2579999864,
             ...
             '137643': {'2022-01-03': 0.3849999905, '2022-01-08': 0.2389999926, 
             ...
            }}

            ```

        Args:
            district_id (int): The `region_id` for the desired province
            dataset (str): An available dataset, as returned by `get_datasets()`
            year (int): The year for which to get data
            month (int): (Optional) the month for which to get data
            year_until (int): (Optional) the end of the year range to query. If not provided, query only data in `year`
            month_until (int): (Optional) the end of the month range to query. If not provided, query only data in `month`

        Returns:
            A dictionary where the keys are the districts in the requested province and 
            the values are dictionaries mapping dates to float values
        """

        return self.query('&province=%s' % province_id, **kwargs)

    def get_by_country(self, country_id, **kwargs) -> Dict[str, Dict[str, Dict]]:
        """Returns district-level data for a given country, for a given year and (optionally) month

        Example:
            ```python
            client.get_by_country(1215, dataset="USCornYM_daily", year=2022, month=6)

            {'137351': {'2022-06-01': 179.1000061035, '2022-06-02': 180.3999938965,
             ...
             '139869': {'2022-06-01': 140.3999938965, '2022-06-02': 147.8000030518,
             ...
            }}

            ```

        Args:
            district_id (int): The `region_id` for the desired country
            dataset (str): An available dataset, as returned by `get_datasets()`
            year (int): The year for which to get data
            month (int): (Optional) the month for which to get data
            year_until (int): (Optional) the end of the year range to query. If not provided, query only data in `year`
            month_until (int): (Optional) the end of the month range to query. If not provided, query only data in `month`

        Returns:
            A dictionary where the keys are the districts in the requested country and 
            the values are dictionaries mapping dates to float values
        """


        return self.query('&country=%s' % country_id, **kwargs)

    def query(self, area_selector, dataset, year, month=None, year_until=None, month_until=None) -> Dict[str, Dict[str, Dict]]:
        """An internal method, not for direct use

        Args:
            area_selector (str): A querystring describing a filter, e.g. `&country=1215`
            dataset (str): A dataset, as returned by `get_datasets()
            year (int): A year for which to query data
            month (int): (Optional) A month for which to query data
            year_until (int): (Optional) The end of the year range to query
            month_until (int): (Optional) The end of the month range to query

        Returns:
            A dictionary where the keys are the districts in the requested area and 
            the values are dictionaries mapping dates to float values
           
        """
        year = int(year)
        end_mo = 12
        start_mo = int(month or 1)
        end_yr = int(year_until or year)
        querystring = '?file=%s%s' % (dataset, area_selector)
        for yr in range(year, end_yr + 1):
            if yr == end_yr:
                end_mo = int(month_until or month or 12)
            for mo in range(start_mo, end_mo + 1):
                if start_mo == 1 and end_mo == 12:
                    querystring += '&months=%s' % yr
                    break
                querystring += '&months=%s-%s' % (yr, mo)
            start_mo = 1
        return self.simple_get_request(querystring) 



class FuturesClient(GenericClient):
    """
    `FuturesClient` is a `grabngro` API client that lets you pull futures data.

    Example:

        ```python
        futures_client = FuturesClient()

        # lists available datasets
        datasets = futures_client.get_datasets()
        print(datasets) # ex: ['cme_daily']

        # lists month codes
        month_codes = futures_client.get_month_codes()
        
        # returns available contract codes and codes
        product_codes = futures_client.get_product_codes()
            
        # query futures data for corn/december 2022, using industry codes
        x = futures_client.get_by_code('CZ22')
        futures_client.get_by_code('CZ2022')
        futures_client.get_by_code('CZ2')

        # query futures data for corn/december 2022, using Gro IDs
        futures_client.get_by_ids(file='cme_daily', region_id=1215, item_id=274, start_date='2022-12-01')

        # load the result into a pandas DataFrame
        df = pd.DataFrame(x).T
        ```
    """

    def get_datasets(self) -> List[str]:
        """Get the datasets available in `FuturesClient`

        Returns:
            A list of strings identifying datasets currently available in `FuturesClient`, e.g. `['cme_daily', 'gro_derived']`
        """
        return self.simple_get_request('futures_datasets')
    
    def get_month_codes(self) -> Dict[str, int]:
        """Get the futures month codes used in `grabngro`

        Returns:
            ```python
            {'F': 1, 'G': 2, 'H': 3, 'J': 4, 'K': 5, 'M': 6, 'N': 7, 'Q': 8, 'U': 9, 'V': 10, 'X': 11, 'Z': 12}
            ```
        """
        return self.simple_get_request('futures_month_codes')
    
    def get_product_codes(self) -> Dict[str, Dict]:
        """Returns a dictionary describing the products for which `FuturesClient` has data

        Example:
        
            ```python
            {'CB': {'product_code': 'CB', 'file': 'CME_daily', 'item_id': 1008, 'item_name': 'Butter', 'region_id': 1215, 'region_name': 'United States'},
            ...
            'FC': {'product_code': 'FC', 'file': 'CME_daily', 'item_id': 3681, 'item_name': 'Cattle, on feed', 'region_id': 1215, 'region_name': 'United States'}}
            ```

        Returns:
            A dictionary where the keys are futures product codes and the values are dictionaries with details describing each available product
        """
        return self.simple_get_request('futures_product_codes')

    def search_products(self, query: str, num_results: int = 3) -> Dict[str, Dict]:
        """
        Search available futures products with a text query

        Example:
            ```python
            search_products("corn", 2)
            {'C': {'product_code': 'C', 'file': 'CME_daily', 'item_id': 274, 'item_name': 'Corn', 'region_id': 1215, 'region_name': 'United States'}, 'BCF': {'product_code': 'BCF', 'file': 'CME_daily', 'item_id': 274, 'item_name': 'Corn', 'region_id': 100000196, 'region_name': 'Black Sea'}}
            ```

        Args:
            query (str): The search query  
            num_results (int): The number of results to return

        Returns:
            A dictionary where the keys are futures product codes and the values are dictionaries with details for each product
        """
        querystring: str = f"?query={query}"
        results = self.simple_get_request('futures_product_search/'+querystring)
        # Return first N key/value pairs in a dictionary
        return {k: results[k] for k in list(results.keys())[:num_results]}

    # Get futures data for a specific contract, specified with Gro IDs
    def get_by_ids(self, file: str, region_id: int, item_id: int, start_date: str) -> Dict[str, Dict]:
        """Get futures data for a specific contract, specified with Gro IDs
        
        Args:
            file (str): The file to query, e.g. `CME_daily`
            region_id (int): The Gro `region_id` to query
            item_id (int): The Gro `item_id` to query
            start_date (str): The contract `start_date` to query

        Example:

            ```python
            futures_client.get_by_ids("CME_daily", 1215, 274, '2022-12-01')
            {'2018-12-14': {'unit_id': 978, 'start_date': '2022-12-01', 'value': 419.0, 'region_id': 1215, 'item_id': 274},
            ...
            '2022-12-14': {'unit_id': 978, 'start_date': '2022-12-01', 'value': 639.0, 'region_id': 1215, 'item_id': 274}}
            ```
        Returns:
            A dictionary where the keys are dates and the values are entities/prices for each day
        """
        querystring: str = f"?file={file}&region_id={region_id}&item_id={item_id}&start_date={start_date}"
        return self.simple_get_request('futures/'+querystring)

    # Get futures data using a specific contract code
    def get_by_code(self, code: str) -> Dict[str, Dict]:
        """Get futures data using a standard contract code

        Example:

            ```python
            futures_client.get_by_code("CZ22")
            {'2018-12-14': {'unit_id': 978, 'start_date': '2022-12-01', 'value': 419.0, 'region_id': 1215, 'item_id': 274},
            ...
            '2022-12-14': {'unit_id': 978, 'start_date': '2022-12-01', 'value': 639.0, 'region_id': 1215, 'item_id': 274}}
            ```
        Args:
            code: A futures contract code, e.g. `CZ24`, `CZ2024`, `CZ4`

        Returns:
            A dictionary where the keys are dates and the values are entities/prices for each day
        """
        querystring: str = f"?code={code}"
        return self.simple_get_request('futures_by_code/'+querystring)

    # Get information about a product, without returning the data
    def describe_product_data(self, product_code: str) -> Dict[str, str]:
        """Get the minimum and maximum reporting dates for a product, without returning data

        Args:
            product_code: A product code, e.g. `C` or `DCEC`

        Returns:
            A dictionary with a minimum and maximum reporting date for the given product
        """
        querystring: str = f"?product_code={product_code}"
        return self.simple_get_request('futures_describe_product_data/'+querystring)

    # Get all futures contracts for a specific month for a given product
    # For example, if product_code="C" and month_code="Z", return all data for December
    # contracts for CME corn.
    def get_all_contracts_by_month(self, product_code: str, month_code: str) -> Dict[str, List]:
        """
        Get all futures contracts for a specific month for a given product

        Args:
            product_code: A product code from `get_product_codes`, e.g. `C` or `DCEC`
            month_code: A month code from `get_month_codes`, e.g. `Z`

        Returns:
            A dictionary in Pandas `values` format that casts to a dataframe with columns
            `start_date`, `reporting_date`, `value`, and `unit`
        """
        querystring: str = f"?product_code={product_code}&month_code={month_code}"
        # Here we're returning the "values" format, so include a column parameters
        # so the output can easily cast into pandas with ** operator
        return {'data': self.simple_get_request('futures_by_month/'+querystring), 'columns': ['start_date', 'reporting_date', 'value', 'unit_id']}

    # Get futures curve for specific product/date
    def get_curve(self, product_code: str, reporting_date: str) -> Dict[str, Dict]:
        """Get the futures curve for a specific product/date

        Args:
            product_code: A product code from `get_product_codes`, e.g. `C` or `LC`
            reporting_date: The reporting date for which to return the curve

        Returns:
            A dictionary where the keys are contract `start_date` and the values are dictionaries with entities/prices for each contract
        """
        querystring: str = f"?product_code={product_code}&reporting_date={reporting_date}"
        return self.simple_get_request('futures_curve/'+querystring)

    # Get futures return series for specific product
    def get_return_series(self, product_code: str) -> Dict[str, float]:
        """
        Get a daily return series for a product's entire history

        Args:
            product_code: A product code from `get_product_codes`, e.g. `C` or `LC`

        Returns:
            A dictionary where the keys are dates and the values are floats representing the daily return for someone who continuously holds the front month contract
        """
        querystring: str = f"?product_code={product_code}"
        return self.simple_get_request('futures_return_series/'+querystring)

    # Get rolling front month futures contract for specific product
    def get_rolling_front_month(self, product_code: str, roll_method: str = 'open_interest') -> Dict[str, float]:
        """
        Get a daily front month rolling futures contract for a product's entire history

        Args:
            product_code: A product code from `get_product_codes`, e.g. `C` or `LC`

            roll_method: A method to determine when to roll contracts, defaults to 'open_interest', but should be one of 'open_interest', 'expiry', 'contract_month_start', 'one_month_prior_to_contract_month', or 'gsci'
        Returns:
            A dictionary where the keys are dates and the values are floats representing the daily front month contract price for the given product
        """
        querystring: str = f"?product_code={product_code}&roll_method={roll_method}"
        return self.simple_get_request('futures_rolling_front_month/'+querystring)
