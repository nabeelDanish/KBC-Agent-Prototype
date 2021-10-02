from flask import Flask
from flask_cors import CORS
from flask import request
from flask import jsonify
from ...models.ukbm.ukbm import ukbm

app = Flask(__name__)
CORS(app)


knowledge_source = "The Black Death is thought to have originated in the arid plains of Central Asia, where it then " \
                   "travelled along the Silk Road, reaching Crimea by 1343. From there, it was most likely carried by " \
                   "Oriental rat fleas living on the black rats that were regular passengers on merchant ships. " \
                   "Spreading throughout the Mediterranean and Europe, the Black Death is estimated to have killed " \
                   "30–60% of Europe's total population. In total, the plague reduced the world population from an " \
                   "estimated 450 million down to 350–375 million in the 14th century. The world population as a " \
                   "whole did not recover to pre-plague levels until the 17th century. The plague recurred " \
                   "occasionally in Europe until the 19th century. "

model = ukbm(knowledge_source)


@app.route('/reply', methods=['POST'])
def add_rider():
    _json = request.json
    _message = _json['message']
    response = {"response": model.getResponse(_message)}
    return jsonify(response), 200
