# import requests

# AIPIPE_API_KEY = "eyJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6IjIzZjIwMDI1ODNAZHMuc3R1ZHkuaWl0bS5hYy5pbiJ9._Kh_4lFxT_g07QZbWuuuabOFVyXr0NqSa2h7pwofmHU"  # 👈 Replace this with your token

# def query_aipipe(prompt: str) -> str:
#     headers = {
#         "Authorization": f"Bearer {AIPIPE_API_KEY}",
#         "Content-Type": "application/json"
#     }

#     payload = {
#         "model": "gpt-3.5-turbo",
#         "messages": [
#             {"role": "system", "content": "You are a helpful teaching assistant for the IITM Tools in Data Science course."},
#             {"role": "user", "content": prompt}
#         ],
#         "temperature": 0.4
#     }

#     response = requests.post("https://aipipe.org/openai/chat/completions", headers=headers, json=payload)



#     if response.status_code == 200:
#         return response.json()["choices"][0]["message"]["content"]
#     else:
#         raise Exception(f"AI Pipe Error {response.status_code}: {response.text}")


import requests

AIPIPE_API_KEY = "eyJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6IjIzZjIwMDI1ODNAZHMuc3R1ZHkuaWl0bS5hYy5pbiJ9._Kh_4lFxT_g07QZbWuuuabOFVyXr0NqSa2h7pwofmHU"  # 🔐 Replace with your actual token

# def query_aipipe(prompt: str) -> str:
#     headers = {
#         "Authorization": f"Bearer {AIPIPE_API_KEY}",
#         "Content-Type": "application/json"
#     }

#     payload = {
#         "model": "openai/gpt-3.5-turbo",  # ✅ Replace with your preferred model if needed
#         "messages": [
#             {"role": "system", "content": "You are a helpful teaching assistant for the IITM Tools in Data Science course."},
#             {"role": "user", "content": prompt}
#         ],
#         "temperature": 0.3
#     }

#     response = requests.post("https://aipipe.org/openrouter/v1/chat/completions", headers=headers, json=payload)

#     if response.status_code == 200:
#         return response.json()["choices"][0]["message"]["content"]
#     else:
#         raise Exception(f"AI Pipe Error {response.status_code}: {response.text}")


# def query_aipipe(prompt, image=None):
#     headers = {
#         "Authorization": f"Bearer {AIPIPE_API_KEY}",
#         "Content-Type": "application/json"
#     }

#     # body = {
#     #     "model": "gpt-3.5-turbo",
#     #     "messages": [{"role": "user", "content": prompt}]
#     # }
#     body = {
#     "model": "gpt-3.5-turbo",
#     "messages": [
#         {"role": "system", "content": "You are a helpful teaching assistant for the Tools in Data Science (TDS) course at IITM. Answer concisely."},
#         {"role": "user", "content": prompt}
#     ]
# }



#     # Add image as tool_choice if given
#     if image:
#         body["tools"] = [{
#             "type": "image_base64",
#             "image": image
#         }]

#     response = requests.post("https://aipipe.org/openai/chat/completions", headers=headers, json=body)

#     if response.status_code == 200:
#         return response.json()["choices"][0]["message"]["content"]
#     else:
#         raise Exception(f"AI Pipe Error {response.status_code}: {response.text}")
    

def query_aipipe(prompt: str, image: str = None) -> str:
    headers = {
        "Authorization": f"Bearer {AIPIPE_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful teaching assistant for the IITM Tools in Data Science course."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.4
    }
    

    response = requests.post("https://aipipe.org/openai/v1/chat/completions", headers=headers, json=payload)

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        raise Exception(f"AI Pipe Error {response.status_code}: {response.text}")