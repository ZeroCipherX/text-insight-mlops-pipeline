from src.TextInsightMlopsPipeline.config.configuration import ConfigurationManager
from src.TextInsightMlopsPipeline.logging import logger
from src.TextInsightMlopsPipeline.components.model_trainer import ModelTrainer


class ModelTrainerTrainingPipeline:
    def __init__(self):
        pass
    
    def initiate_model_trainer(self):
        config = ConfigurationManager()
        model_trainer_config = config.get_model_trainer_config()
        model_trainer = ModelTrainer(config=model_trainer_config)
        model_trainer.train()