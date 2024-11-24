import sys
from src.forest.cloud_storage.aws_storage import SimpleStorageService
from src.forest.exception import CustomException
from src.forest.entity.estimator import ForestModel
from pandas import DataFrame

class ForestEstimator:
    """
    This class is used to save and retrieve the sensor model in an S3 bucket and to do prediction.
    """

    def __init__(self, bucket_name, model_path):
        """
        :param bucket_name: Name of your model bucket
        :param model_path: Location of your model in the bucket
        """
        self.bucket_name = bucket_name
        self.s3 = SimpleStorageService()
        self.model_path = model_path
        self.loaded_model: ForestModel = None

    def is_model_present(self):
        """
        Checks if the model is present in the specified model_path on S3.
        No need to pass model_path, since it's already an attribute of the class.
        :return: Boolean indicating model presence.
        """
        try:
            # Using the class's model_path attribute directly
            return self.s3.s3_key_path_available(bucket_name=self.bucket_name, s3_key=self.model_path)
        except CustomException as e:
            print(e)
            return False

    def load_model(self) -> ForestModel:
        """
        Load the model from the model_path.
        :return: The loaded model.
        """
        return self.s3.load_model(self.model_path, bucket_name=self.bucket_name)

    def save_model(self, from_file, remove: bool = False) -> None:
        """
        Save the model to the model_path in the S3 bucket.
        :param from_file: Path to the local model file.
        :param remove: If True, removes the local file after uploading.
        """
        try:
            self.s3.upload_file(
                from_file,
                to_filename=self.model_path,
                bucket_name=self.bucket_name,
                remove=remove
            )
        except Exception as e:
            raise CustomException(e, sys)

    def predict(self, dataframe: DataFrame):
        """
        Perform prediction using the loaded model.
        :param dataframe: DataFrame to use for prediction.
        :return: Prediction results.
        """
        try:
            if self.loaded_model is None:
                self.loaded_model = self.load_model()
            return self.loaded_model.predict(dataframe=dataframe)
        except Exception as e:
            raise CustomException(e, sys)
