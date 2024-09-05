from flask import Flask, request, jsonify
from flask_cors import CORS


app = Flask(__name__)
CORS(app) 

def convert_request_data(data):
    responses = []
    for item in data:
        response = [item['value'], item['personality']]
        responses.append(response)
    return responses


def evaluate_mbti(responses):
    scores = {"E": 0, "I": 0, "S": 0, "N": 0, "T": 0, "F": 0, "J": 0, "P": 0}
    for response, dimension in responses:
        if response == 1:  # Strongly Agree
            scores[dimension] += 2
        elif response == 2:  # Agree
            scores[dimension] += 1
        elif response == 4:  # Disagree
            scores[dimension] -= 1
        elif response == 5:  # Strongly Disagree
            scores[dimension] -= 2
    # Determine MBTI type
    mbti_type = ""
    mbti_type += "E" if scores["E"] >= scores["I"] else "I"
    mbti_type += "S" if scores["S"] >= scores["N"] else "N"
    mbti_type += "T" if scores["T"] >= scores["F"] else "F"
    mbti_type += "J" if scores["J"] >= scores["P"] else "P"
    return mbti_type

@app.route('/')
def hello_world():
    return 'Hello World'

@app.route('/api/data', methods=['POST'])
def receive_data():
    data = request.get_json()  # Get the JSON data sent in the POST request
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    #Get the data array from request JSON
    data_array = data['data']

    responses = convert_request_data(data_array)
    mbti_type = evaluate_mbti(responses)
    print(mbti_type)
    return jsonify({"mbti": mbti_type})

if __name__ == '__main__':
    app.run(debug=True)