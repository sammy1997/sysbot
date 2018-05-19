from flask import Flask, jsonify
from flask import request, json
from github_functions import label_opened_issue
from stemming.porter2 import stem
from nltk.tokenize import word_tokenize

app = Flask(__name__)


@app.route('/')
def home():
    return 'Response to test hosting.'

#this function will recieve all the github events
@app.route('/web_hook', methods=['POST'])
def github_hook_receiver_function():
    if request.headers['Content-Type'] == 'application/json':
        data = request.json
        action = data.get('action', None)
        if action!=None:
            if action == 'opened':
                #If it's an issue opened event
                response = label_opened_issue(data)
            #No other events are being handeled currently
        else:
            pass
            #currently the bot isn't handeling any other cases
        return jsonify(request.json)


def get_stems(sentence):
    result = list()
    tokens = word_tokenize(sentence)
    for word in tokens:
        result.append(stem(word))
    return result

if __name__ == '__main__':
    app.run()
