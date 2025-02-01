from transformers import LEDTokenizer, LEDForConditionalGeneration
class Summarizer:
    model_name = "allenai/led-large-16384-arxiv"

    def __init__(self, none) -> None:
        self.tokenizer = LEDTokenizer.from_pretrained(self.model_name)
        if none == False:
            self.model = None
        self.model = LEDForConditionalGeneration.from_pretrained(self.model_name)

        # self.model = None

    def summarize_led(self, text):
        inputs = self.tokenizer(text, return_tensors="pt", max_length=4096, truncation=True)
        summary_ids = self.model.generate(inputs["input_ids"], max_length=250, min_length=200)
        return self.tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    print("hello")