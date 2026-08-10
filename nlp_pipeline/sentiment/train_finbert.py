from transformers import Trainer, TrainingArguments
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from datasets import load_dataset

from nlp_pipeline.sentiment.gru_model import GRUSentiment
from nlp_pipeline.sentiment.gru_tokenizer import GRUTokenizer


def load_phrasebank():
    return load_dataset("financial_phrasebank", "sentences_allagree")

def train():
    model_name = "ProsusAI/finbert"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name)

    dataset = load_phrasebank()

    def tokenize(batch):
        return tokenizer(batch["sentence"], truncation=True)

    tokenized = dataset.map(tokenize, batched=True)

    args = TrainingArguments(
        output_dir="models/finbert_finetuned",
        evaluation_strategy="epoch",
        save_strategy="epoch",
        learning_rate=2e-5,
        per_device_train_batch_size=8,
        num_train_epochs=3,
    )

    trainer = Trainer(
        model=model,
        args=args,
        train_dataset=tokenized["train"],
        eval_dataset=tokenized["test"],
    )

    trainer.train()
