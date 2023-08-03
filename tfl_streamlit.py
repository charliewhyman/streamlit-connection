import streamlit as st
from connection import tfl_api_connection

def main():

    st.set_page_config(
        page_title='TfL Line Disruptions',
        page_icon='🏙️'
    )

    # Ask user for API key
    app_key = st.text_input("Enter your TfL API Key", type="password")

    # ask user to select a mode
    modes = ['tube', 'dlr', 'overground', 'tram', 'elizabeth-line']

    mode = st.selectbox('Select a mode of transport', modes)

    # Create a button to get data from the TfL API
    if st.button("Check status"):
        if not app_key or not mode:
            st.warning("Please enter Tfl API key and a mode.")
        else:
            conn = tfl_api_connection(connection_name='tfl_api_connection', app_key=app_key)

            statuses = conn.query(mode)

            if statuses == None:
                st.error("Unable to connect to TfL API")
            else:
                display_mode_statuses(statuses)

# 
def display_mode_statuses(statuses):
    for line in statuses:
        st.subheader(line['line_name'])

        st.markdown(f'**{line["statusSeverityDescription"]}**')

        # no need to display reason if Good Service on the line
        if line['reason'] != None:
            st.text(line['reason'])

if __name__ == "__main__":
    main()