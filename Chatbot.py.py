import numpy as np
import nltk
import string
import random
nltk.download('punkt_tab')
f = open('/content/data.txt','r',errors = 'ignore')
raw_doc = f.read()

raw_doc = raw_doc.lower()
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')


sentence_tokens = nltk.sent_tokenize(raw_doc)
word_tokens = nltk.word_tokenize(raw_doc)

sentence_tokens[2]
word_tokens[2]

lemmer = nltk.stem.WordNetLemmatizer()
def LemTokens(tokens):
  return [lemmer.lemmatize(token) for token in tokens]
remove_punc_dict = dict ((ord(punct), None) for punct in string.punctuation)
def LemNormalize(text):
  return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punc_dict)))

greet_inputs = ("hello", "hi", "greetings", "sup", "what's up","hey",)
greet_responses = ("hi", "hey", "*nods*", "hi there", "hello", "I am glad! You are talking to me")
def greet(sentence):
  for word in sentence.split():
    if word.lower() in greet_inputs:
      return random.choice(greet_responses)

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def response(user_response):
  robo1_response = ''
  TfidfVec = TfidfVectorizer (tokenizer = LemNormalize, stop_words = 'english')
  tfidf = TfidfVec.fit_transform(sentence_tokens)
  vals = cosine_similarity(tfidf[-1], tfidf)
  idx = vals.argsort()[0][-2]
  flat = vals.flatten()
  flat.sort()
  req_tfidf = flat[-2]
  if (req_tfidf == 0):
    robo1_response = robo1_response + "I am sorry. Unable to understand you!"
    return robo1_response
  else:
    robo1_response = robo1_response+ sentence_tokens[idx]
    return robo1_response

flag = True
print('Hello! I am the Learning Bot. Start typing your text after greeting to talk to me. For ending convo type byel')
while(flag == True):
  user_response = input()
  user_response = user_response.lower()
  if(user_response != 'bye'):
    if(user_response == 'thank you' or user_response == 'thanks'):
      flag = False
      print('Bot: You are Welcome..')
    else:
      if(greet(user_response) != None):
        print('Bot '+ greet(user_response))
      else:
        sentence_tokens.append(user_response)
        word_tokens = word_tokens + nltk.word_tokenize(user_response)
        final_words = list(set (word_tokens))
        print('Bot: ', end = '')
        print(response(user_response))
        sentence_tokens.remove(user_response)
  else:
    flag = False
    print('Bot: Goodbye! Take Care <3')