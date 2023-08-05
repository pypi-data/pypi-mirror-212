import requests

def chat_completions(access_token, messages):
    url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions"
    headers = {
        "Content-Type": "application/json",
    }
    params = {
        "access_token": access_token,
    }
    data = {
        "messages": messages,
    }
    response = requests.post(url, headers=headers, params=params, json=data)
    return response.json()