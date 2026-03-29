from src.TextInsightMlopsPipeline.config.configuration import ConfigurationManager
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch


class PredictionPipeline:
    def __init__(self):
        self.config = ConfigurationManager().get_model_evaluation_config()
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.tokenizer = AutoTokenizer.from_pretrained(self.config.tokenizer_path)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(
            self.config.model_path
        ).to(self.device)

    def predict(self, text):
        inputs = self.tokenizer(
            text,
            max_length=1024,
            truncation=True,
            return_tensors="pt"
        ).to(self.device)

        with torch.no_grad():
            summary_ids = self.model.generate(
                inputs["input_ids"],
                attention_mask=inputs["attention_mask"],
                length_penalty=0.8,
                num_beams=2,
                max_length=128
            )

        summary = self.tokenizer.decode(summary_ids[0], skip_special_tokens=True)

        print("Dialogue:")
        print(text)
        print("\nModel Summary:")
        print(summary)

        return summary