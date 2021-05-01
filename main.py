#!/usr/local/bin/python3 -u
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
from dotenv import load_dotenv
load_dotenv()  # take environment variables from .env

from flask import Flask, abort, jsonify, request
from flask_cors import CORS, cross_origin
import gpt_2_simple as gpt2
import tensorflow as tf

# from run_generation import generate_text

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
gpt2.download_gpt2(model_name="355M")
print("GPT downloaded")
sess = gpt2.start_tf_sess()
print("session started")
gpt2.load_gpt2(sess, run_name='run1')
print("checkpoint loaded")

graph = tf.get_default_graph()


def getResponse(msg, prefixHistory):
    global graph
    app.logger.debug(f"Received request with text: {msg}")
    prefixHistory += "Person: " + msg + "\n" + "Aryeh Bookbinder:"
    with graph.as_default():
        text = gpt2.generate(sess, length=200,temperature=0.6,prefix=prefixHistory, return_as_list=True)[0]
    text = text[len(prefixHistory):]
    end = text.find("Person")

    response = text[:end-1]
    app.logger.debug(f"Responding with: {response}")
    return response, prefixHistory

@app.route("/generate", methods=['POST'])
@cross_origin()
def get_gen():
    data = request.get_json()

    if 'text' not in data or len(data['text']) == 0 or 'model' not in data:
        abort(400)
    else:
        # text = data['text']
        # model = data['model']

        # result = generate_text(
        #     model_type='gpt2',
        #     length=100,
        #     prompt=text,
        #     model_name_or_path=model
        # )
        response, _ = getResponse(data['text'], data['prefixHistory'])
        #result = response.replace("Aryeh Bookbinder", "Aryeh Bot")
        return jsonify({'result': "Aryeh Bookbinder:" + str(response)})

@app.route('/test')
def test_response():
    return 'Done', 201
