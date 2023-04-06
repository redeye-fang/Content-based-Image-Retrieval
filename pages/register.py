import streamlit as st
import google.auth
from google.oauth2 import id_token
from google.auth.transport import requests
import uuid

CLIENT_ID = 'your-client-id-here'


def register():
    st.subheader('Register')
    email = st.text_input('Email')
    password = st.text_input('Password', type='password')
    confirm_password = st.text_input('Confirm Password', type='password')
    # if st.button('Register'):
    #     # validate user input
    #     # add user to database
    #     # redirect to home page on success

def authenticate_google_user(token):
    try:
        id_info = id_token.verify_oauth2_token(token, requests.Request(), CLIENT_ID)
        if id_info['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise ValueError('Wrong issuer.')
        # use id_info['sub'] to identify the user in your system
        # redirect to home page on success
    except ValueError:
        # Invalid token
        pass

def google_login():
    state = str(uuid.uuid4())
    # url, _ = google.auth.default(scopes=['openid', 'email'], state=state)
    st.write(f'Click [here]("www.google.com") to log in with Google')
    # if st.session_state.get('state') == state:
        # authenticate_google_user(st.session_state.get('token'))

if __name__ == '__main__':

    st.session_state.state = ''
    st.session_state.token = ''
    if 'token' in st.experimental_get_query_params():
        st.session_state.state = st.experimental_get_query_params()['state'][0]
        st.session_state.token = st.experimental_get_query_params()['token'][0]
    
    register()
    google_login()