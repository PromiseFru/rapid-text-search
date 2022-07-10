from os import truncate
import torch
from transformers import T5Tokenizer, T5ForConditionalGeneration

class T5:
    def __init__(self) -> None:
        self.model_name = "t5-small"
        self.tokenizer = T5Tokenizer.from_pretrained(self.model_name)
        self.model = T5ForConditionalGeneration.from_pretrained(self.model_name)
        self.device = torch.device('cpu')


    def summarize(self, text: str) -> str:
        """
        """
        preprocess_text = text.strip().replace("\n","")
        t5_prepared_Text = "summarize: "+preprocess_text

        tokenized_text = self.tokenizer.encode(t5_prepared_Text, return_tensors="pt").to(self.device)

        # summmarize 
        summary_ids = self.model.generate(tokenized_text,
                                            num_beams=5,
                                            no_repeat_ngram_size=5,
                                            min_length=80,
                                            max_length=160,
                                            early_stopping=True)

        output = self.tokenizer.decode(summary_ids[0], skip_special_tokens=True)

        return output