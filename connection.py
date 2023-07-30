from streamlit.connections import ExperimentalBaseConnection

# https://docs.streamlit.io/library/advanced-features/connecting-to-data#connection-building-best-practices
class london_datastore_connection(ExperimentalBaseConnection):

    def _connect(self, **kwargs) -> None:
        if 'app_key' in kwargs:
            self.app_key = kwargs["app_key"]
           
        else:
            raise Exception("Enter API key!")

        return None