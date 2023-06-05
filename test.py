import requests

def main():
    
    response = requests.get(
        url="http://localhost:8000/get_token",
    )
    if response.status_code == 200:
        
        token = response.json()
        
        response = requests.get(
            url="http://localhost:8000/secure",
            headers={"Authorization": f"Bearer {token['access_token']}"},
        )
        if response.status_code == 200:
            print(response.json())
        else:
            print(response.text)


if __name__ == "__main__":
    main()