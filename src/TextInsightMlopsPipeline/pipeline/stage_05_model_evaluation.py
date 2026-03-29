from src.TextInsightMlopsPipeline.config.configuration import ConfigurationManager
from src.TextInsightMlopsPipeline.logging import logger
from src.TextInsightMlopsPipeline.components.model_evaluation import ModelEvaluation

class ModelEvaluationTrainerPipeline:
    def __init__(self):
        pass

    def initiate_model_evaluation(self):
        config = ConfigurationManager()
        model_evaluation_config = config.get_model_evaluation_config()
        model_evaluation_config = ModelEvaluation(config=model_evaluation_config)
        model_evaluation_config.evaluate()