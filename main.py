import requests


def shorten_link(token: str, long_url: str) -> str:

    url = "https://api.vk.com/method/utils.getShortLink"
    params = {
        "access_token": token,
        "url": long_url,
        "v": "5.131"
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        if "response" in data:
            return data["response"]["short_url"]
        else:
            error_msg = data.get("error", {}).get("error_msg", "Неизвестная ошибка API")
            return f"Ошибка: {error_msg}"

    except requests.exceptions.RequestException as e:
        return f"Ошибка соединения: {e}"


def main():

    TOKEN = "7db8c8fe7db8c8fe7db8c8fe1f7e979cf177db87db8c8fe1a45ffa0e0a7530175d2a5d5"
    TEST_URL = "https://api.vk.com/method/utils.getShortLink"


    short_url = shorten_link(TOKEN, TEST_URL)
    print("Сокращенная ссылка:", short_url)


if __name__ == "__main__":
    main()




