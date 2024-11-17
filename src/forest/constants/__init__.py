
import os
from from_root import from_root

# common file name
TARGET_COLUMN = "Cover_Type"
FILE_NAME: str = "covtype.csv"
TRAIN_FILE_NAME: str = "train.csv"
TEST_FILE_NAME: str = "test.csv"
PREPROCSSING_OBJECT_FILE_NAME = "preprocessing.pkl"
SCHEMA_FILE_PATH = os.path.join("config", "schema.yaml")
DATABASE_NAME = "forest_db"
COLLECTION_NAME = "forest_col"


# Data Ingestion related constants

ARTIFACTS_DIR = os.path.join(from_root(), "artifacts")
DATA_INGESTION_ARTIFACTS_DIR = "DataIngestion"
DATA_INGESTION_FEATURE_STORE_DIR: str = "feature_store"
DATA_INGESTION_INGESTED_DIR: str = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO: float = 0.2