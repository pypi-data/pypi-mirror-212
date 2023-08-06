import os
import requests
import json

class TranslateAPI:
    def __init__(self):
        self.url = "https://google-translate1.p.rapidapi.com/language/translate/v2"
        self.headers = {
            "Accept-Encoding": "application/gzip",
            "X-RapidAPI-Key": os.getenv("RAPIDAPI_KEY"),
            "X-RapidAPI-Host": "google-translate1.p.rapidapi.com"
        }

    def translate(self, text, source_lang, target_lang):
        data = {
            'q': text,
            'source': source_lang,
            'target': target_lang,
            'format': 'text'
        }
        response = requests.post(self.url, headers=self.headers, data=data)
        return response.json()

    def get_languages(self):
        url = self.url + "/languages"
        response = requests.get(url, headers=self.headers)
        return response.json()
