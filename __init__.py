import requests 

api_url_link = "https://ai-assistant-chatbot-xnhx.onrender.com/generate"

api_url = requests.post(api_url_link, json={"query": "Which room is good for single person?"})

if api_url.status_code == 200:
    print(api_url.json())
    
# Output --> If you're looking for a room as a single person, you've got two decent options: room 106 for $80 or room 104 for $90, both of which are Standard rooms that can fit one guest. Room 106 seems like the better deal, saving you $10 compared to room 104.