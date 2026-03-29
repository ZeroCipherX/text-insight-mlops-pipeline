from src.TextInsightMlopsPipeline.logging import logger
from src.TextInsightMlopsPipeline.pipeline.stage_01_data_ingestion import DataIngestionTrainingPipeline
from src.TextInsightMlopsPipeline.pipeline.stage_02_data_validation import DataValidationTrainingPipeline
from src.TextInsightMlopsPipeline.pipeline.stage_03_data_transformation import DataTransformationTrainingPipeline
from src.TextInsightMlopsPipeline.pipeline.stage_04_model_trainer import ModelTrainerTrainingPipeline
import os

STAGE_NAME = "Data Ingestion Stage"
try:
    logger.info(f">>>>>>> Stage {STAGE_NAME} started <<<<<<<")
    data_ingestion_pipeline = DataIngestionTrainingPipeline()
    data_ingestion_pipeline.initiate_data_ingestion()
    logger.info(f">>>>>>> Stage {STAGE_NAME} completed <<<<<<<\n\nx==========x")
except Exception as e:
    logger.exception(e)
    raise e

STAGE_NAME = "Data Validation Stage"
try:
    logger.info(f">>>>>>> Stage {STAGE_NAME} started <<<<<<<")
    data_validation_pipeline = DataValidationTrainingPipeline()
    data_validation_pipeline.initiate_data_validation()
    logger.info(f">>>>>>> Stage {STAGE_NAME} completed <<<<<<<\n\nx==========x")
except Exception as e:
    logger.exception(e)
    raise e

STAGE_NAME = "Data Transformation Stage"
try:
    logger.info(f">>>>>>> Stage {STAGE_NAME} started <<<<<<<")
    data_transformation_pipeline = DataTransformationTrainingPipeline()
    data_transformation_pipeline.initiate_data_transformation()
    logger.info(f">>>>>>> Stage {STAGE_NAME} completed <<<<<<<\n\nx==========x")
except Exception as e:
    logger.exception(e)
    raise e

STAGE_NAME = "Model Trainer Stage"
try:
    model_path = os.path.join("artifacts", "model_trainer", "pegasus-samsum-model")
    tokenizer_path = os.path.join("artifacts", "model_trainer", "tokenizer")

    if os.path.exists(model_path) and os.path.exists(tokenizer_path):
        logger.info("Fine-tuned model already exists. Skipping training.")
    else:
        logger.info(f">>>>>>> Stage {STAGE_NAME} started <<<<<<<")
        model_trainer_pipeline = ModelTrainerTrainingPipeline()
        model_trainer_pipeline.initiate_model_trainer()
        logger.info(f">>>>>>> Stage {STAGE_NAME} completed <<<<<<<\n\nx==========x")
except Exception as e:
    logger.exception(e)
    raise e