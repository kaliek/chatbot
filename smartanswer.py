import requests
import wikipedia
from questionparser import QuestionParser
from constant import *


class SmartAnswer(QuestionParser):
    def __init__(self, question):
        super().__init__(question)
        super().preprocess()
        self.loc_answer = None
        self.hum_answer = ""
        self.wiki_answer = []

    # Check if it's a LOC question and has 'LOC' entity
    # if yes: get locaion coordinantes
    def is_loc_answer(self):
        if self.get_type() == 'LOC':
            if self.get_has('loc'):
                self.loc_answer = self.get_lat_lng(" ".join(self.get_loc_entity()))
        return self.loc_answer

    # Get location coordinates for loc entity
    def get_lat_lng(self, loc):
        api = ""
        try:
            with open('googlemap_api.txt', 'r') as f:
                api = f.readline().strip()
        except IOError:
            print("No API file. Please create a token.txt with your token in the first line.")
            sys.exit()
        response = requests.get("https://maps.googleapis.com/maps/api/geocode/json?address={}&key={}".format(loc, api))
        location = response.json()["results"][0]["geometry"]["location"]
        return [location['lat'], location['lng']]
    
    # Check if it's a 'HUM' question, and has 'PER' entity or noun subject
    # If yes, return one-sentence wiki result
    def is_hum_answer(self):
        if self.get_type() == 'HUM':
            print("for hum question: ")
            if self.get_has('per'):
                print("has per entity:")
                self.hum_answer = self.get_wiki_one_sentence(" ".join(self.get_per_entity()))
            elif self.get_nsubj():
                print("has nsubj: ")
                self.hum_answer = self.get_wiki_one_sentence(" ".join(self.get_nsubj()))
        return self.hum_answer

    # Get one-sentence wili result if obj exists
    def get_wiki_one_sentence(self, obj):
        print(obj)
        try:
            raw = wikipedia.page(obj)
        except:
            raw = None
        if raw: 
            summ = wikipedia.summary(obj, sentences=1)
            result = summ + "\n" + raw.url
        return result
    
    # Check if it has any noun
    # if yes, get wiki summary for all the nous
    def is_wiki_answer(self):
        if self.get_nsubj(): 
            print("wiki nsubj")
            self.wiki_answer.append(self.get_wiki_summary(self.get_nsubj()))
        else:
            print("wiki other nouns")
            obj_list = self.get_entity()
            possible_noun = self.get_noun_chunk()
            possible_noun.extend(self.get_noun_phrase())
            for n in possible_noun:
                if n not in obj_list: obj_list.append(n)
            for obj in obj_list:
                self.wiki_answer.append(self.get_wiki_summary(obj))
        return self.wiki_answer

    # Get wiki summary if obj exists
    def get_wiki_summary(self, obj):
        print(obj)
        try:
            raw = wikipedia.page(obj)
        except:
            raw = None
        if raw: 
            summ = wikipedia.summary(obj)
            result = summ + "\n" + raw.url
        return result