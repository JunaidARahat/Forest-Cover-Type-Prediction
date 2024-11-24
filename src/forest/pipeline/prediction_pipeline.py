import sys
import numpy as np
import pandas as pd
from pandas import DataFrame
from src.forest.cloud_storage.aws_storage import SimpleStorageService
from src.forest.exception import CustomException
from src.forest.logger import logging
from src.forest.entity.config_entity import PredictionPipelineConfig
from src.forest.entity.s3_estimator import ForestEstimator


class PredictionPipeline:
    """
    This class handles the prediction process, including data retrieval, model interaction, and storing results.
    """

    def __init__(self, prediction_pipeline_config: PredictionPipelineConfig = PredictionPipelineConfig()) -> None:
        """
        Initialize the PredictionPipeline.

        :param prediction_pipeline_config: Configuration for the prediction pipeline.
        """
        try:
            self.prediction_pipeline_config = prediction_pipeline_config
            self.s3 = SimpleStorageService()
            self.model_estimator = ForestEstimator(
                bucket_name=self.prediction_pipeline_config.model_bucket_name,
                model_path=self.prediction_pipeline_config.model_file_path
            )
        except Exception as e:
            raise CustomException(f"Error initializing PredictionPipeline: {e}", sys)

    def get_data(self) -> DataFrame:
        """
        Retrieve prediction data from the S3 bucket.

        :return: DataFrame containing prediction data.
        """
        try:
            logging.info("Entered get_data method of PredictionPipeline class.")
            prediction_df = self.s3.read_csv(
                filename=self.prediction_pipeline_config.data_file_path,
                bucket_name=self.prediction_pipeline_config.data_bucket_name
            )
            logging.info("Successfully read prediction CSV file from S3 bucket.")
            logging.info("Exited the get_data method of PredictionPipeline class.")
            return prediction_df
        except Exception as e:
            raise CustomException(f"Error retrieving data from S3: {e}", sys)

    def predict(self, dataframe: DataFrame) -> np.ndarray:
        """
        Perform predictions using the model loaded via ForestEstimator.

        :param dataframe: DataFrame containing input data for predictions.
        :return: Predictions as a NumPy array.
        """
        try:
            logging.info("Entered predict method of PredictionPipeline class.")
            
            # Ensure the model is loaded
            if not self.model_estimator.is_model_present():  # Ensure no extra arguments are passed here
                raise CustomException("Model file not found in the S3 bucket.", sys)
            
            # Load the model if not already loaded
            if self.model_estimator.loaded_model is None:
                self.model_estimator.load_model()

            # Perform prediction
            predictions = self.model_estimator.predict(dataframe)
            logging.info("Predictions successfully generated.")
            logging.info("Exited the predict method of PredictionPipeline class.")
            return predictions
        except Exception as e:
            raise CustomException(f"Error during prediction: {e}", sys)

    def initiate_prediction(self) -> DataFrame:
        """
        Execute the prediction pipeline, including retrieving data, predicting, and storing results.

        :return: DataFrame containing the input data with predictions appended.
        """
        try:
            logging.info("Entered initiate_prediction method of PredictionPipeline class.")
            
            # Step 1: Get input data
            dataframe = self.get_data()
            
            # Step 2: Predict the output
            predicted_arr = self.predict(dataframe)
            
            # Step 3: Prepare the prediction results
            prediction = pd.DataFrame(predicted_arr, columns=['Cover_Type'])
            predicted_dataframe = pd.concat([dataframe, prediction], axis=1)
            logging.info("Prediction results appended to the input dataframe.")
            
            # Step 4: Upload results to S3
            self.s3.upload_df_as_csv(
                dataframe=predicted_dataframe,
                filename=self.prediction_pipeline_config.output_file_name,
                folder_name=self.prediction_pipeline_config.output_folder_name,
                bucket_name=self.prediction_pipeline_config.data_bucket_name
            )
            logging.info(f"Predicted results uploaded to S3 bucket: {self.prediction_pipeline_config.data_bucket_name}")
            logging.info("Exited initiate_prediction method of PredictionPipeline class.")
            return predicted_dataframe
        except Exception as e:
            raise CustomException(f"Error during prediction pipeline execution: {e}", sys)
