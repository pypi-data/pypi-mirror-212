import requests

def generateJoke():
    url = "https://v2.jokeapi.dev/joke/Any"
    response = requests.get(url)
    
    if response.status_code == 200:
        joke = response.json()
        
        if joke["type"] == "single":
            return joke["joke"]
        elif joke["type"] == "twopart":
            return f"{joke['setup']}\n{joke['delivery']}"
    else:
        return "Failed to fetch joke"


if __name__ == '__main__':
    joke = generateJoke()
    print(joke)
