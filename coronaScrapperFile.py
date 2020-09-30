import requests
import json
import speech_recognition as sr
import re
import subprocess
import threading



API_KEY = ""
PROJECT_TOKEN = ""
RUN_TOKEN = ""


class Data:
    def __init__(self, api_key, project_token):
        self.api_key = api_key
        self.project_token = project_token
        self.params = {"api_key": self.api_key}             #autentication
        self.data = self.get_data()

#will call the request and set data atribute for this object. i do it here so i can call the method whenever i want to and updated it
    def get_data(self):
        # call a get request
        response = requests.get(f'https://www.parsehub.com/api/v2/projects/{PROJECT_TOKEN}/last_ready_run/data',
                                params={"api_key": API_KEY})
        data = json.loads(response.text)
        # print(self.data)  # will print list like: {'total': [{'name': 'Coronavirus Cases:', 'value': '33,540,029'}, {'name': 'Deaths:', 'value': '1,006,057'}, {...
        return data

# print(data['total']) #print info related to total
# #set up class that let me parse the data

    def get_total_cases(self):
        data = self.data['total']

        for content in data:
            if content['name'] == "Coronavirus Cases:":
                # print(content['value'])
                return content['value']

    def get_total_deaths(self):
        data = self.data['total']

        for content in data:
            if content['name'] == "Deaths:":
                return content['value']
        return "0"

    def get_country_info(self, country):
        data = self.data["country"]

        for content in data:
            if content['name'].lower() == country.lower():
                return content

        return "0"


# data = Data(API_KEY, PROJECT_TOKEN)

# print(data.data)
# print("Total deaths: " + data.get_total_deaths())
# print(data.get_country_info("usa"))
# print(data.get_country_info("poland")['total_cases'])

def get_list_of_countries(self):
    countries = []
    for country in self.data['country']:
        countries.append(country['name'].lower())

    return countries


def say(text):
    subprocess.call(['say', text])


def get_audio():
    r = sr.Recognizer()             #set up recognizer
    mic = sr.Microphone()           #set up microphone
    with mic as source:
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)     #listen and record
        transcript = ""

        try:
            transcript = r.recognize_google(audio)  #pass it here and translate to a text
            return transcript.lower()
        except Exception as e:
            print("Exception: ", str(e))

        return transcript.lower()



# say(get_audio())
# say(get_audio())
def main():
    print("Program started.")
    data = Data(API_KEY, PROJECT_TOKEN)
    end_phrase = "STOP"

    TOTAL_PATTERNS = {
                    re.compile("[\w\s]+ total [\w\s]+ cases"): data.get_total_cases,
                    re.compile("[\w\s]+ total cases"): data.get_total_cases,
                    re.compile("[\w\s]+ total [\w\s]+ deaths"): data.get_total_deaths,
                    re.compile("[\w\s]+ total cases"): data.get_total_deaths
                    # re.compile("total cases"): data.get_total_cases
                    }

    while True:
        print("Listening...")
        text = get_audio()
        print(text)
        result = None

        for pattern, func in TOTAL_PATTERNS.items():
            if pattern.match(text):
                result = func()
                break

        if result:
            say(result)

        if text.find(end_phrase):
            break


main()