import streamlit as st 
import requests
import json
import re 

chat_input = st.chat_input()
inputs = {"query": chat_input}
output = requests.post("http://127.0.0.1:8000/generate", data = json.dumps(inputs))
if output.status_code == 200:
    answer = output.json()
    st.write(output.json())
    extract_image = re.search(r'https?://\S+\.jpg', answer)
    if extract_image:
        image_url = extract_image.group()
        st.image(image_url)