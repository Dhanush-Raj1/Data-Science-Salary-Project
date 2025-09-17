import os
import sys
from src.logger import logging 
from src.exception_handling import Custom_Exception

import mlflow
from mlflow.models import infer_signature
import mlflow.sklearn, mlflow.xgboost, mlflow.catboost


class MLFlowLogger:
    
    def __init__(self):
        """
        Initializes MLflow server and sets the experiment name.
        """
        mlflow.set_tracking_uri("http://localhost:8000")
        self.experiment_name = "Data-Science-Salary-Prediction"
        mlflow.set_experiment(self.experiment_name)
        logging.info(f"Initializing MLflow with experiment name: {self.experiment_name}")

    def log_model(self, model_name, params, metrics, model, X_train):
        """
        Logs trained models and their reports to MLflow.
        Parmas: 
        model_name(str): Name of the model,
        params(dict): hyperparameters,
        metrics(dict): performance metrics,
        model: model object,
        x_train: training data for inference signature
        """
        logging.info(f"Starting MLflow run for model: {model_name}")
        with mlflow.start_run(run_name=model_name):
            # log params
            logging.info(f"Logging parameters for {model_name}: {params} in MLflow.")
            mlflow.log_params(params)

            # log metrics
            logging.info(f"Logging metrics for {model_name} in MLflow.")
            for metric_name, value in metrics.items():
                logging.info(f"  - {metric_name}: {value}")
                mlflow.log_metric(metric_name, value)

            # infer signature 
            logging.info(f"Inferring model signature using input data shape: {X_train.shape}")
            signature = infer_signature(X_train, model.predict(X_train))

            try:
                if model_name in ["Xgboost regressor"]:
                    logging.info(f"Logging {model_name} with XGB flavor to MLflow")
                    mlflow.xgboost.log_model(
                        model,
                        artifact_path=model_name,
                        signature=signature,
                        input_example=X_train[:5]
                    )

                elif model_name in ["Catboost regressor"]:
                    logging.info(f"Logging {model_name} with CatBoost flavor to MLflow")
                    mlflow.catboost.log_model(
                        model,
                        artifact_path=model_name,
                        signature=signature,
                        input_example=X_train[:5]
                    )
                else:
                    logging.info(f"Logging {model_name} with sklearn flavor to MLFlow")
                    mlflow.sklearn.log_model(
                        model,
                        artifact_path=model_name,
                        signature=signature,
                        input_example=X_train[:5]
                    )

                logging.info(f"Successfully logged {model_name} to MLflow.")
            except Exception as e:
                logging.info(f"Error logging model {model_name}: {str(e)}")
                raise Custom_Exception(e, sys)
        
        logging.info(f"✅ MLflow logging for all models has been completed.")
            

    def register_best_model(self, metrics, models, X_train):
        """
        Registers the best model based on R2 score.
        Params:
        metrics(dict): performance metrics of all models,
        models(dict): dict of model objects with model names as keys,
        X_train: Training data for inference signature
        """
        logging.info(f"➡️ Starting best model registration process in MLflow.")
        logging.info(f"Finding best model based on R2 score")
        best_model = None 
        best_model_name = None
        best_r2_score = -float('inf')    # intialize to very small value, negative infinity 
        
        for model_name, metric_dict in metrics.items():
            #r2_score = metric_dict.get("r2_score", -float('inf'))
            r2_score = metric_dict['r2_score']
            logging.info(f"Model: {model_name}, R2 Score: {r2_score}")
            if r2_score > best_r2_score:
                best_model_name = model_name
                best_r2_score = r2_score

        if best_model_name:
            best_model = models[best_model_name]
            logging.info(f"Best model identified: {best_model_name} with R2 Score: {best_r2_score}")

            with mlflow.start_run(run_name="Best Model Registry"):
                logging.info(f"Starting MLFlow run for best model registry")
                mlflow.log_param("Best Model", best_model_name)
                mlflow.log_metric("Best Model R2 Score", best_r2_score)
                signature = infer_signature(X_train, best_model.predict(X_train))
                registered_model_name = f"DSS-Prediction-best-model-{best_model_name}"
                logging.info(f"Registering best model as {registered_model_name})")

                try:
                    if best_model_name == "Xgboost regressor":
                        mlflow.xgboost.log_model(
                            best_model,
                            artifact_path="best_model",
                            signature=signature,
                            input_example=X_train[:5],
                            registered_model_name=f"DS-Salary-Prediction-{best_model_name}-model"
                        )
                    elif best_model_name in ["Catboost regressor"]:
                        mlflow.catboost.log_model(
                            best_model,
                            artifact_path="best_model",
                            signature=signature,
                            input_example=X_train[:5],
                            registered_model_name=f"DS-Salary-Prediction-{best_model_name}-model"
                        )
                    else:
                        mlflow.sklearn.log_model(
                            best_model,
                            artifact_path="best_model",
                            signature=signature,
                            input_example=X_train[:5],
                            registered_model_name=f"DS-Salary-Prediction-{best_model_name}-model"
                        )
                    logging.info(f"✅ Successfully registered best model: {registered_model_name} ")

                except Exception as e:
                    logging.info(f"Error registering best model {best_model_name}: {str(e)}")
                    raise Custom_Exception(e, sys)
                
        else:
            logging.info("No best model found or invalid r2 scores.")
                






