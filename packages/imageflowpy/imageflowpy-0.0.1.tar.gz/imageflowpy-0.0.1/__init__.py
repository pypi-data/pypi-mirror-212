import requests

def make_request(url):
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        image_url = data.get("url")
        return image_url
    else:
        return None

def billie_eilish():
    url = 'https://imageflow.gay/flow/billie'
    image_url = make_request(url)
    print(image_url)