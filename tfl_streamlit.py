import streamlit as st
from connection import london_datastore_connection
import pandas as pd

#populate modes dropdown /Line/Meta/Modes
#user selects mode
# populate available lines using /Line/Line_GetByMode
#populate line dropdown
#user selects line
# Populate disruption card using /Line/Line_Disruption


def main():

    st.set_page_config(
        page_title='TfL Line Disruptions',
        page_icon='🏙️'
    )

    # Ask user for API key
    app_key = st.text_input("Enter your TfL API Key", type="password")

if __name__ == "__main__":
    main()