from src.TextInsightMlopsPipeline.config.configuration import ConfigurationManager
from src.TextInsightMlopsPipeline.logging import logger
from src.TextInsightMlopsPipeline.components.data_transformation import DataTransformation


class DataTransformationTrainingPipeline:
    def __init__(self):
        pass
    
    def initiate_data_transformation(self):
        config = ConfigurationManager()
        data_transformation_config = config.get_data_transformation_config()
        data_transformation = DataTransformation(config=data_transformation_config)
        data_transformation.convert()