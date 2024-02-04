import requests


#Use Oobabooga textgen webui to generate responses
def ooba(api,text):
    

    headers = {
        "Content-Type": "application/json"
    }

    history = []

    while True:
        user_message = text
        history.append({"role": "user", "content": user_message})
        data = {
            "mode": "chat",
            "character": "Example",
            "messages": history,
           
        }

        response = requests.post(api, headers=headers, json=data, verify=False)
        assistant_message = response.json()['choices'][0]['message']['content']
        history.append({"role": "assistant", "content": assistant_message})
        #print(assistant_message)
        return assistant_message
    
if __name__ == "__main__":
    msg = ooba('Hello, How are you?')
    print(msg)