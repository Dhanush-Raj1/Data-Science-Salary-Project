from src.logger import logging 
from src.pipelines.predict_pipeline import Predict, NewData

from flask import Flask, request, render_template, url_for

app = Flask(__name__)


# route for home page
@app.route('/')
def home():
    return render_template('home_page.html')


# route for predict page
@app.route('/predictdata', methods=['GET', 'POST'])
def predict():
    if request.method == 'GET': 
        return render_template('predict_page.html')
     
    else:
        logging.info("POST request has been made.")
        data = NewData(Industry = request.form.get("Industry"), 
                       Sector = request.form.get("Sector"), 
                       Size = request.form.get("Size"),
                       Revenue = request.form.get("Revenue"),
                       Ownership = request.form.get("Ownership"),
                       Rating = int(request.form.get("Rating")),  
                       age = int(request.form.get("age")),
                       python = int(request.form.get("python")),
                       spark = int(request.form.get("spark")),
                       aws = int(request.form.get("aws")),
                       excel = int(request.form.get("excel")),
                       LLMs = int(request.form.get("LLMs")),
                       sql = int(request.form.get("sql")),
                       Job_simp = request.form.get("Job_simp"),
                       seniority = request.form.get("seniority") ) 
        
        df = data.get_data_as_dataframe()
        logging.info("Data has been converted into a dataframe.")
        logging.info(f"Dataframe: \n{df.head()}")
        print(df.head())
        
        Prediction = Predict()
        result = Prediction.predict_data(df)
        logging.info("Prediction Result: {result}")
        print(f"Predition result {result}")
        
        result_text =  "Your estimated salary is:"
        
        
        return render_template('predict_page.html', result = result[0], result_text = result_text)
        
        
        
if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)