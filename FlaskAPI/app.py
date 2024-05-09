from flask import Flask, jsonify, request   
import json
import pickle
import numpy as np

# load the model(ran_regressor.best_estimator_)
def load_models():
    file_name =  "models/model_file.p"
    with open(file_name, 'rb') as pickled:
        data = pickle.load(pickled)
        model = data['model']
    return model 

app = Flask(__name__)
@app.route('/predict', methods = ['GET'])

# predict from the input data
def predict():
    # input data
    
    # retrieve the json data and store it in request_json
    request_json =  request.get_json()
    
    # extract the value from 'input' and assign to x
    x = request_json['input']
    
    # convert to array and reshape it
    x_in = np.array(x).reshape(1, -1)
    
    # load model
    model = load_models()
    prediction = model.predict(x_in)[0]
    response = json.dumps({'response': prediction})
    return response, 200
    
    
if __name__ == "__main__":
    application.run(debug=True)
