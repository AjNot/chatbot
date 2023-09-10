from lib2to3.pgen2.token import NEWLINE
from boto import config


#data1= {
#    "song1": "Happy by Pharell Williams",
#    "song2": "Lovely day by Bill Withers"
#}
#db.child("Happy").push(data1)

#data2= {
#    "song1": "'I Know It's Over' by The Smiths",
#    "song2": "'No Distance Left to Run' by Blur"
#}
#db.child("Sad").push(data2)

#data3= {
#    "song1": "'Ruel - Dazed & Confused",
#    "song2": "'Younger Ruel"
#}
#db.child("Confused").push(data3)


import nltk
nltk.download('popular')
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import pickle
import numpy as np
from keras.models import load_model
model = load_model('model.h5')
import json
import random
intents = json.loads(open('data.json').read())
words = pickle.load(open('texts.pkl','rb'))
classes = pickle.load(open('labels.pkl','rb'))

def clean_up_sentence(sentence):
    # tokenize the pattern - split words into array
    sentence_words = nltk.word_tokenize(sentence)
    # stem each word - create short form for word
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

# return bag of words array: 0 or 1 for each word in the bag that exists in the sentence

def bow(sentence, words, show_details=True):
    # tokenize the pattern
    sentence_words = clean_up_sentence(sentence)
    # bag of words - matrix of N words, vocabulary matrix
    bag = [0]*len(words)  
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s: 
                # assign 1 if current word is in the vocabulary position
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % w)
    return(np.array(bag))

def predict_class(sentence, model):
    # filter out predictions below a threshold
    p = bow(sentence, words,show_details=False)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD]
    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list

def getResponse(ints, intents_json):
    tag = ints[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if(i['tag']== tag):
            result = random.choice(i['responses'])
            #if( tag== "happy days"):
            #    pass
            #elif(tag=="sad days"):
            #    pass
            #elif(tag=="confused days"):
            #    pass
            break
    return result

def chatbot_response(msg):
    ints = predict_class(msg, model)
    res = getResponse(ints, intents)
    return res



from flask import Flask, render_template, request
app = Flask(__name__)
app.static_folder = 'static'
app = Flask(__name__, static_url_path='/static')  
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/chat")
def chat():
    return render_template("bot.html")

@app.route("/aboutus")
def aboutus():
    return render_template("aboutus.html")

@app.route("/contact")
def contact():
    return render_template("Contact.html")

@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    return chatbot_response(userText)


if __name__ == "__main__":
    app.run()