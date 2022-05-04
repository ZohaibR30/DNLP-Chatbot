#Building a Chatbot with DNLP

import numpy as np
import tensorflow as tf
import re
import time


##########    DATA PREPROCESSING    ##########

#Read data from files
lines = open('movie_lines.txt', encoding = 'utf-8', errors = 'ignore').read().split('\n')
conversations = open('movie_conversations.txt', encoding = 'utf-8', errors = 'ignore').read().split('\n')

#Create dictionary to map lines with ids
id_to_line = {}
for line in lines:
    _line = line.split(' +++$+++ ')
    if len(_line) == 5:
        id_to_line[_line[0]] = _line[4]
        
#Create list of conversations
conversations_ids = []
for conversation in conversations[:-1]:
    _conversation = conversation.split(' +++$+++ ')[-1][1:-1].replace("'", "").replace(" ", "")
    conversations_ids.append(_conversation.split(','))
    
#Getting question and answers
questions = []
answers = []

for conversation in conversations_ids:
    for i in range(len(conversation) - 1):
        questions.append(id_to_line[conversation[i]])
        answers.append(id_to_line[conversation[i+1]])
        
#Clean up of texts
def clean_text(text):
    text = text.lower()
    text = re.sub(r"i'm", "i am", text)
    text = re.sub(r"he's", "he is", text)
    text = re.sub(r"she's", "she is", text)
    text = re.sub(r"that's", "that is", text)
    text = re.sub(r"what's", "what is", text)
    text = re.sub(r"where's", "where is", text)
    text = re.sub(r"\'ll", "will", text)
    text = re.sub(r"\'ve", "have", text)
    text = re.sub(r"\'re", "are", text)
    text = re.sub(r"\'d", "would", text)
    text = re.sub(r"won't", "will not", text)
    text = re.sub(r"can't", "cannot", text)
    text = re.sub(r"[-()\"#/@;:<>{}+=~|.?,]", "", text)
    return text

#Clean questions
clean_questions = []
for question in questions:
    clean_questions.append(clean_text(question))

#Clean answers
clean_answers = []
for answer in answers:
    clean_answers.append(clean_text(answer))

#Dictionary that maps words to its occurences
word_to_count = {}
for question in clean_questions:
    for word in question.split():
        if word not in word_to_count:
            word_to_count[word] = 1
        else:
            word_to_count[word] += 1
            
for answer in clean_answers:
    for word in answer.split():
        if word not in word_to_count:
            word_to_count[word] = 1
        else:
            word_to_count[word] += 1
   
#Creating two dictionaries that maps words to unique integers
#THIS METHOD WILL INCLUDE 95% MOST FREQUENT WORDS
threshold = 10
questions_words_to_int = {}
word_number = 0

for word, count in word_to_count.items():
    if count >= threshold:
        questions_words_to_int[word] = word_number
        word_number += 1

answers_words_to_int = {}
word_number = 0

for word, count in word_to_count.items():
    if count >= threshold:
        answers_words_to_int[word] = word_number
        word_number += 1

#Adding the lst tokens to these two dictionaries
tokens = ['<PAD>', '<EOS>', '<OUT>', '<SOS>']

for token in tokens:
    questions_words_to_int[token] = len(questions_words_to_int) + 1

for token in tokens:
    answers_words_to_int[token] = len(answers_words_to_int) + 1
    
#Creating inverse of answers_words_to_int
answers_int_to_word = {w_i: w for w, w_i in answers_words_to_int.items()} 

#Adding EOS to the end of every answer
for i in range(len(clean_answers)):
    clean_answers[i] += ' <EOS>' 

