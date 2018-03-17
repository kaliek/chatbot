# Chatbot

## Purpose
To build a chatbot that provides informative answer to users.

## Audience
For anyone who wants a quick adaptation of Natural Language Processing (NLP) and Machine Learning (ML) Techniques in chatbot development.
 
## Feature To-do List
- [x] Question Parsing
- [x] Co-reference
- [x] Smart Answering
- [x] Preprocessing Illed Inputs
- [x] Interactivity
- [ ] Testing and Rating
- [ ] Provides Accurate One-line Factual Answer (Not my focus for now)

## Implementation Summary for Each Feature
It's written in Python 3.
* Question Parsing
    * Inspired by [adam-qas](https://github.com/5hirish/adam_qas)
    * Thoughout understanding of requests for informative reply
    * Question type: train Support Vector Machine (SVM) using a dataset that contains questions and their corresponding features such as "bi-gram", "question head words" and etc. Then uses NLP to extract the same feature for new incoming question, and predict the question type via SVM.
    * Question keywords: use NLP Part of Speech (POS) techniques to extract noun phrases.
    * Question entities: use NLP Named Entity Recognition (NER) techniques to identify entities such as "CITY", "STATE_OR_PROVINCE", "COUNTRY", "ORGANIZATION", "LOCATION", "MONEY", "NUMBER", "ORDINAL", "PERCENT","DATE", "TIME", "DURATION", "SET"……
    * This feature aims to parse questions thoughoutly for better answer extraction

* Co-reference
    * To co-refer what users have previously said (e.g. "I want to know more about A." "What's his job?", "his" refers to "A's")
    * Uses [neuralcoref](https://github.com/huggingface/neuralcoref) for now

* Smart Answering
    * Smarter answer for some question types (e.g. return Google Map for location questions)
    * Only `LOC` questions are entertained for now
    * if `question type` is `LOC` and any question entities is location-related, i.e."CITY", "STATE_OR_PROVINCE", "COUNTRY", "ORGANIZATION", "LOCATION" 
    * Return Google Map of the entities to users
    * Plan to return wikipedia summary for `DESC` questions

* Preprocessing for Illed Input
    * Typos create misunderstanding for users' needs, so I used language_check to correct the typos before parsing the input
    * Caseless input affects NER, so I use `truecase` from StanfordCoreNLP to correct the input first
    * Problems are: question head words are often "miscorrected" to personal proper nouns, causing question type to be misidentified as `HUM`
    * Self wrote rules to take into conderation of question entities before using `truecase` to correct question head words, might be susceptible to unusal questions that do not start with common question head words: "who", "what", "where", "when", "why", "how", "whose", "which", "whom"

* Interactivity
    * To interact with users via casual conversation if factual question is not asked
    * Uses [chatterbot](https://github.com/gunthercox/ChatterBot) to converse with users
    * chatterbot matches input with conversation turns to find the closest utterance and return the corresponding reply

* Testing and Rating
    * To store user's rating for improving the system over time
    * Plan to ask users to rate right/wrong for each factual question answered, and rate overall experience with the chatbot after a session

## Realisation
Current implementation is a Telegram bot: @corefbot
You can choose your own platform to build the chatbot
Nice functions of [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot):
* `send_location(latitude, longitude)`: returns Google Map for users
* Users can use `\info` command to signal the bot that you are asking for factual answers instead of just sharing your loneliness with the bot





