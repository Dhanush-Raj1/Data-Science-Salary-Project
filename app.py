import sys 
from src.logger import logging 
from src.exception_handling import Custom_Exception
from src.pipelines.predict_pipeline import PredictData, NewData 
from flask import Flask, request, render_template, url_for 
import numpy as np



app = Flask(__name__)

# route for home page 
@app.route('/')
def home(): 
    return render_template('home_page.html')
 

# route for predict page 
@app.route('/predictdata', methods=['GET', 'POST'])
def predict_datapoint():
    if request.method == 'GET':
        return render_template('predict_page.html')
    else:
        try:
            logging.info("POST request has been made.")

            data = NewData(
                 Company_Rating = float(request.form.get("Company_Rating")),
                 Skills = request.form.get("Skills"),
                 Seniority = request.form.get('Seniority'),
                 Job_type = request.form.get('Job_type'),
                 Salary_Source = request.form.get('Salary_Source'),
                 Location = request.form.get('Location') 
            )

            df = data.get_data_as_dataframe()
            logging.info("Data has been converted into a dataframe: \n{df}")

            model = PredictData()
            result = model.predict_data(df)
            logging.info(f"Prediction Result: {result}")

            # Format the result 
            predicted_salary = round(float(result[0]))
            result_text =  "Your estimated salary is"

            return render_template('predict_page.html', result=predicted_salary, result_text=result_text)

        except Exception as e:
            raise Custom_Exception(e, sys)
        


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False, port=8000)
