from streamlit.connections import ExperimentalBaseConnection
from streamlit import cache_data
import requests

# https://docs.streamlit.io/library/advanced-features/connecting-to-data#connection-building-best-practices
class tfl_api_connection(ExperimentalBaseConnection[requests.Session]):

    def __init__(self, connection_name: str, **kwargs) -> None:
        super().__init__(connection_name=connection_name, **kwargs)
        self._session = self._connect(**kwargs)

    # Implement _connect method, returning underlying requests.Session object. Requires app key from kwargs.
    def _connect(self, **kwargs) -> requests.Session:
        if 'app_key' in kwargs:
            self.app_key = kwargs["app_key"]
        
        else:
            raise Exception("Enter API Key")
        
        return requests.Session()
    
    # retrievers underlying connection object (requests.Session)
    def cursor(self):
        return self._session
        
    # helper query
    def query(self, mode, ttl: int = 3600):
        
        @cache_data(ttl=ttl)
        # for a given mode of transport, return a list of dictionaries containing line statuses.    
        def get_mode_status(mode):
            params = {
                "app_key": self.app_key
            }
            
            # https://api.tfl.gov.uk/swagger/ui/index.html?url=/swagger/docs/v1#!/Line/Line_StatusByMode
            endpoint = f'https://api.tfl.gov.uk/line/mode/{mode}/status'
            
            response = self._session.get(endpoint, params=params)

            if response.status_code != 200:
                raise Exception(f"Error {response.status_code} - failed to get data.")
            
            else:
                statuses = []

                statusData = response.json()

                # add every line/status combination to the list
                for line in statusData:
                    line_name = line['name']

                    line_statuses = line['lineStatuses']

                    for line_status in line_statuses:
                        statusSeverity = line_status['statusSeverity']
                        statusSeverityDescription = line_status['statusSeverityDescription']

                        # statusSeverity of 10 == 'Good Service' - no need to return a status reason
                        if line_status['statusSeverity'] != 10:
                            reason = line_status['reason']

                        else:
                            reason = None

                        status = {'line_name': line_name,
                                  'statusSeverity': statusSeverity,
                                'statusSeverityDescription': statusSeverityDescription,
                                'reason': reason
                                }
                        statuses.append(status)

            return statuses
        
        return get_mode_status(mode)