import os
import sys
import json
import pandas as pd
from src.forest.logger import logging
from src.forest.exception import CustomException
from src.forest.entity.config_entity import *
from src.forest.entity.artifact_entity import *
from src.forest.constants import *
from src.forest.utils.main_utils import *
from evidently.report import Report
from evidently.metrics import DatasetDriftMetric


class DataValidation:
    def __init__(self, data_ingestion_artifact=DataIngestionArtifact,
                 data_validation_config=DataValidationConfig):
        self.data_ingestion_artifact = data_ingestion_artifact
        self.data_validation_config = data_validation_config
        self._schema_config = read_yaml_file(file_path=SCHEMA_FILE_PATH)

    @staticmethod
    def read_data(filepath) -> pd.DataFrame:
        try:
            return pd.read_csv(filepath)
        except Exception as e:
            raise CustomException(e, sys)

    def validate_number_of_columns(self, dataframe: pd.DataFrame) -> bool:
        """
        Validate that the dataframe has the expected number of columns.
        """
        try:
            status = len(dataframe.columns) == len(self._schema_config["columns"])
            logging.info(f"Is required column present: [{status}]")
            return status
        except Exception as e:
            raise CustomException(e, sys)

    def is_numerical_column_exist(self, dataframe: pd.DataFrame) -> bool:
        """
        Check that all required numerical columns are present in the dataframe.
        """
        try:
            dataframe_columns = dataframe.columns
            status = True
            missing_numerical_columns = []
            for column in self._schema_config["numerical_columns"]:
                if column not in dataframe_columns:
                    status = False
                    missing_numerical_columns.append(column)
            logging.info(f"Missing numerical column: {missing_numerical_columns}")
            return status
        except Exception as e:
            raise CustomException(e, sys) from e

    def detect_dataset_drift(self, reference_df: pd.DataFrame, current_df: pd.DataFrame) -> bool:
        """
        Detect data drift between reference and current datasets.
        """
        try:
            # Create a report with the Data Drift Metric
            report = Report(metrics=[DatasetDriftMetric()])
            report.run(reference_data=reference_df, current_data=current_df)

            # Save the report as JSON
            report_json = report.json()
            json_report = json.loads(report_json)

            # Write the drift report to a YAML file
            write_yaml_file(file_path=self.data_validation_config.drift_report_file_path, content=json_report)

            # Extract drift metrics
            n_features = json_report["metrics"][0]["result"]["number_of_columns"]
            n_drifted_features = json_report["metrics"][0]["result"]["number_of_drifted_columns"]

            logging.info(f"{n_drifted_features}/{n_features} features detected with drift.")

            # Determine if dataset drift is present
            drift_status = json_report["metrics"][0]["result"]["dataset_drift"]

            return drift_status

        except Exception as e:
            raise CustomException(e, sys) from e

    def initiate_data_validation(self):
        """
        Run data validation checks including column validation and data drift detection.
        """
        logging.info("Entered initiate_data_validation method of DataValidation class")
        try:
            validation_error_msg = ''
            train_df, test_df = (self.read_data(filepath=self.data_ingestion_artifact.trained_file_path),
                                 self.read_data(filepath=self.data_ingestion_artifact.test_file_path))

            # Validate number of columns
            if not self.validate_number_of_columns(dataframe=train_df):
                validation_error_msg += "Columns are missing in train dataframe. "
            if not self.validate_number_of_columns(dataframe=test_df):
                validation_error_msg += "Columns are missing in test dataframe. "

            # Check numerical columns
            if not self.is_numerical_column_exist(dataframe=train_df):
                validation_error_msg += "Numerical columns are missing in train dataframe. "
            if not self.is_numerical_column_exist(dataframe=test_df):
                validation_error_msg += "Numerical columns are missing in test dataframe. "

            validation_status = len(validation_error_msg) == 0

            # Detect dataset drift if validation passes
            if validation_status:
                drift_status = self.detect_dataset_drift(train_df, test_df)
                if drift_status:
                    logging.info("Data Drift Detected")
            else:
                logging.info(f"Validation Error: {validation_error_msg}")

            data_validation_artifact = DataValidationArtifact(
                validation_status=validation_status,
                message=validation_error_msg,
                drift_report_file_path=self.data_validation_config.drift_report_file_path
            )

            logging.info(f"Data validation artifact: {data_validation_artifact}")
            return data_validation_artifact

        except Exception as e:
            raise CustomException(e, sys)
