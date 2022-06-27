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
                                            num_beams=4,
                                            no_repeat_ngram_size=5,
                                            min_length=30,
                                            max_length=150,
                                            early_stopping=True)

        output = self.tokenizer.decode(summary_ids[0], skip_special_tokens=True)

        return output

t5 = T5()
text = """Appendicitis is caused by a blockage of the hollow portion of the appendix.[10] This is most commonly due to a calcified "stone" made of feces.[6] Inflamed lymphoid tissue from a viral infection, parasites, gallstone, or tumors may also cause the blockage.[6] This blockage leads to increased pressures in the appendix, decreased blood flow to the tissues of the appendix, and bacterial growth inside the appendix causing inflammation.[6][11] The combination of inflammation, reduced blood flow to the appendix and distention of the appendix causes tissue injury and tissue death.[12] If this process is left untreated, the appendix may burst, releasing bacteria into the abdominal cavity, leading to increased complications.[12][13]
The diagnosis of appendicitis is largely based on the person's signs and symptoms.[11] In cases where the diagnosis is unclear, close observation, medical imaging, and laboratory tests can be helpful.[4] The two most common imaging tests used are an ultrasound and computed tomography (CT scan).[4] CT scan has been shown to be more accurate than ultrasound in detecting acute appendicitis.[14] However, ultrasound may be preferred as the first imaging test in children and pregnant women because of the risks associated with radiation exposure from CT scans.[4]"""
print(t5.summarize(text=text))