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
        data = NewData(Industry = request.form.get("Industry of the company"), 
                       Sector = request.form.get("Sector of the company"), 
                       Size = request.form.get("Size of the company"),
                       Revenue = request.form.get("Revenue of the company"),
                       Ownership = request.form.get("Ownership of the company"),
                       Rating = request.form.get("Rating of the company"),  
                       age = request.form.get("Age of the company"),
                       python = request.form.get("python"),
                       spark = request.form.get("spark"),
                       aws = request.form.get("aws"),
                       excel = request.form.get("excel"),
                       LLMs = request.form.get("LLMs"),
                       sql = request.form.get("sql"),
                       Job_simp = request.form.get("Job_simp"),
                       seniority = request.form.get("seniority") )
        
        df = data.get_data_as_dataframe()
        logging.info("Data has been converted into a dataframe.")
        logging.info(f"Dataframe: \n{df.head()}")
        print(df.head())
        
        Prediction = Predict()
        result = Prediction.predict_data(df)
        print(f"Predition result {result}")
        
        result_text =  "The salary for the given role is :"
        
        
        return render_template('predict_page.html', result = result[0], result_text = result_text)
        
        
        
if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)