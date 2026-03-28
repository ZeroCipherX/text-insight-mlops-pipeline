from src.TextInsightMlopsPipeline.config.configuration import ConfigurationManager
from src.TextInsightMlopsPipeline.components.data_validation import DataValidation   
from src.TextInsightMlopsPipeline.logging import logger

class DataValidationTrainingPipeline:
    def __init__(self):
        pass
    
    def initiate_data_validation(self):
        config = ConfigurationManager()
        data_validation_config = config.get_data_validation_config()

        data_validation = DataValidation(config=data_validation_config)

        validation_status = data_validation.validate_all_files_exist()

       