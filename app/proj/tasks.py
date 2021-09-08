from .celery import app
import mlflow.pytorch
from transformers import AutoTokenizer

model = mlflow.pytorch.load_model("/build/app/model")
tokenizer = AutoTokenizer.from_pretrained("/build/app/model/data", use_fast=True)

@app.task
def generator(input):
    input_ids = tokenizer.encode("<|question|> " + input, return_tensors="pt")
    outputs = model.generate(
        input_ids,
        do_sample=True,
        max_length=100,
        top_k=50,
        top_p=0.95,
        num_return_sequences=1
    )
    output = tokenizer.decode(outputs[0], skip_special_tokens=True)

    return output.replace("<|question|>", "Question:").replace("<|answer|>", "Answer:")
