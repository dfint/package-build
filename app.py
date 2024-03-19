import streamlit as st
from package_build.metadata import get_hook_metadata, get_dict_metadata


hook_metadata = get_hook_metadata()

st.write(hook_metadata)

dict_metadata = get_dict_metadata()

st.write(dict_metadata)
