from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from datasets import load_from_disk
import torch
import pandas as pd
from tqdm import tqdm
import evaluate

from src.TextInsightMlopsPipeline.entity import ModelEvaluationConfig


class ModelEvaluation:
    def __init__(self, config: ModelEvaluationConfig):
        self.config = config

    def evaluate(self):
        device = "cuda" if torch.cuda.is_available() else "cpu"
        tokenizer = AutoTokenizer.from_pretrained(self.config.tokenizer_path)
        model_pegasus = AutoModelForSeq2SeqLM.from_pretrained(
            self.config.model_path
        ).to(device)

        dataset_samsum_pt = load_from_disk(self.config.data_path)

        rouge_metric = evaluate.load("rouge")
        rouge_names = ["rouge1", "rouge2", "rougeL", "rougeLsum"]

        for dialogue, summary in tqdm(
            zip(
                dataset_samsum_pt["test"][0:10]["dialogue"],
                dataset_samsum_pt["test"][0:10]["summary"]
            ),
            total=10
        ):
            inputs = tokenizer(
                dialogue,
                max_length=1024,
                truncation=True,
                return_tensors="pt"
            ).to(device)

            with torch.no_grad():
                summary_ids = model_pegasus.generate(
                    inputs["input_ids"],
                    attention_mask=inputs["attention_mask"],
                    length_penalty=0.8,
                    num_beams=2,
                    max_length=128
                )

            decoded = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
            rouge_metric.add_batch(predictions=[decoded], references=[summary])

        score = rouge_metric.compute()
        rouge_dict = {rn: score[rn] for rn in rouge_names}

        df = pd.DataFrame(rouge_dict, index=["pegasus"])
        df.to_csv(self.config.metric_file_name, index=False)