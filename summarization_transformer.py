# -*- coding: utf-8 -*-
"""summarization transformer.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1by2ohHPyCxZebUaacbKXmvwFmPfIduw4
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

!pip install datasets

from datasets import load_dataset

dataset = load_dataset('cnn_dailymail', '3.0.0')

type(dataset)

dataset['train']

sample = dataset["train"][1]
print(f"""
Article (excerpt of 500 characters, total length: {len(sample["article"])}):
""")
print(sample["article"][:500])
print(f'\nSummary (length: {len(sample["highlights"])}):')
print(sample["highlights"])

sample_text = dataset["train"][1]["article"][:2000]
# We'll collect the generated summaries of each model in a dictionary
summaries = {}

import nltk
from nltk.tokenize import sent_tokenize

# Download the 'punkt_tab' resource
nltk.download('punkt_tab')

string = "The U.S. are a country. The U.N. is an organization."
sent_tokenize(string)

def three_sentece_summary(text):
  return "\n".join(sent_tokenize(text)[:3])

summaries["baseline"] = three_sentece_summary(sample_text)

summaries

from transformers import pipeline, set_seed

set_seed(42)
pipe = pipeline("text-generation", model="gpt2-xl")
gpt2_query = sample_text + "\nTL;DR:\n"
pipe_out = pipe(gpt2_query, max_length=512, clean_up_tokenization_spaces=True)
summaries["gpt2"] = "\n".join(
 sent_tokenize(pipe_out[0]["generated_text"][len(gpt2_query) :]))

pipe = pipeline("summarization", model="t5-large")
pipe_out = pipe(sample_text)
summaries["t5"] = "\n".join(sent_tokenize(pipe_out[0]["summary_text"]))

pipe = pipeline("summarization", model="facebook/bart-large-cnn")
pipe_out = pipe(sample_text)
summaries["bart"] = "\n".join(sent_tokenize(pipe_out[0]["summary_text"]))

pipe = pipeline("summarization", model="google/pegasus-cnn_dailymail")
pipe_out = pipe(sample_text)
summaries["pegasus"] = pipe_out[0]["summary_text"].replace(" .<n>", ".\n")

print("GROUND TRUTH")
print(dataset["train"][1]["highlights"])
print("")
for model_name in summaries:
 print(model_name.upper())
 print(summaries[model_name])
 print("")

!pip install evaluate && pip install sacrebleu

from evaluate import load

bleu_metric = load("sacrebleu")

predictions = ["the the the the the the"]  # Wrap prediction in a list
references = ["the cat is on the mat"]  # Wrap reference in a list
results = bleu_metric.compute(predictions=predictions, references=references)

print("BLEU score:", results["score"])

results["precisions"] = [np.round(p, 2) for p in results["precisions"]]
pd.DataFrame.from_dict(results, orient="index", columns=["Value"])

!pip install rouge_score

rouge_metric = load("rouge")

reference = dataset["train"][1]["highlights"]
records = []
rouge_names = ["rouge1", "rouge2", "rougeL", "rougeLsum"]
for model_name in summaries:
    rouge_metric.add(prediction=summaries[model_name], reference=reference)
    score = rouge_metric.compute()
    rouge_dict = dict((rn, score[rn]) for rn in rouge_names)
    records.append(rouge_dict)
pd.DataFrame.from_records(records, index=summaries.keys())

def evaluate_summaries_baseline(dataset, metric,
  column_text="article",
  column_summary="highlights"):
  summaries = [three_sentece_summary(text) for text in dataset[column_text]]
  metric.add_batch(predictions=summaries,
  references=dataset[column_summary])
  score = metric.compute()
  return score

test_sampled = dataset["test"].shuffle(seed=42).select(range(1000))
score = evaluate_summaries_baseline(test_sampled, rouge_metric)
rouge_dict = dict((rn, score[rn]) for rn in rouge_names)
pd.DataFrame.from_dict(rouge_dict, orient="index", columns=["baseline"]).T

from tqdm import tqdm
import torch

device = "cuda" if torch.cuda.is_available() else "cpu"

def chunks(list_of_elements, batch_size):
  """Yield successive batch-sized chunks from list_of_elements."""
  for i in range(0, len(list_of_elements), batch_size):
    yield list_of_elements[i : i + batch_size]

def evaluate_summaries_pegasus(dataset, metric, model, tokenizer,
  batch_size=16, device=device,
  column_text="article",
  column_summary="highlights"):

  article_batches = list(chunks(dataset[column_text], batch_size))
  target_batches = list(chunks(dataset[column_summary], batch_size))

  for article_batch, target_batch in tqdm(
    zip(article_batches, target_batches), total=len(article_batches)):
    inputs = tokenizer(article_batch, max_length=1024, truncation=True,
    padding="max_length", return_tensors="pt")
    summaries = model.generate(input_ids=inputs["input_ids"].to(device),
    attention_mask=inputs["attention_mask"].to(device),
    length_penalty=0.8, num_beams=8, max_length=128)
    decoded_summaries = [tokenizer.decode(s, skip_special_tokens=True,
    clean_up_tokenization_spaces=True)
    for s in summaries]
    decoded_summaries = [d.replace("<n>", " ") for d in decoded_summaries]
    metric.add_batch(predictions=decoded_summaries, references=target_batch)

  score = metric.compute()
  return score

from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
model_ckpt = "google/pegasus-cnn_dailymail"
tokenizer = AutoTokenizer.from_pretrained(model_ckpt)
model = AutoModelForSeq2SeqLM.from_pretrained(model_ckpt).to(device)
score = evaluate_summaries_pegasus(test_sampled, rouge_metric,
 model, tokenizer, batch_size=8)
rouge_dict = dict((rn, score[rn].mid.fmeasure) for rn in rouge_names)
pd.DataFrame(rouge_dict, index=["pegasus"])

dataset_samsung = load_dataset("samsum")
split_lengths = [len(dataset_samsum[split])for split in dataset_samsum]

print(f"Split lengths: {split_lengths}")
print(f"Features: {dataset_samsum['train'].column_names}")
print("\nDialogue:")
print(dataset_samsum["test"][0]["dialogue"])
print("\nSummary:")
print(dataset_samsum["test"][0]["summary"])

pipe_out = pipe(dataset_samsum["test"][0]["dialogue"])
print("Summary:")
print(pipe_out[0]["summary_text"].replace(" .<n>", ".\n"))

score = evaluate_summaries_pegasus(dataset_samsum["test"], rouge_metric, model,
 tokenizer, column_text="dialogue",
 column_summary="summary", batch_size=8)
rouge_dict = dict((rn, score[rn].mid.fmeasure) for rn in rouge_names)
pd.DataFrame(rouge_dict, index=["pegasus"])

d_len = [len(tokenizer.encode(s)) for s in dataset_samsum["train"]["dialogue"]]
s_len = [len(tokenizer.encode(s)) for s in dataset_samsum["train"]["summary"]]
fig, axes = plt.subplots(1, 2, figsize=(10, 3.5), sharey=True)
axes[0].hist(d_len, bins=20, color="C0", edgecolor="C0")
axes[0].set_title("Dialogue Token Length")
axes[0].set_xlabel("Length")
axes[0].set_ylabel("Count")
axes[1].hist(s_len, bins=20, color="C0", edgecolor="C0")
axes[1].set_title("Summary Token Length")
axes[1].set_xlabel("Length")
plt.tight_layout()
plt.show()

def convert_examples_to_features(example_batch):
  input_encodings = tokenizer(example_batch["dialogue"], max_length=1024,
  truncation=True)
  with tokenizer.as_target_tokenizer():
  target_encodings = tokenizer(example_batch["summary"], max_length=128,
  truncation=True)
  return {"input_ids": input_encodings["input_ids"],
  "attention_mask": input_encodings["attention_mask"],
  "labels": target_encodings["input_ids"]}

dataset_samsum_pt = dataset_samsum.map(convert_examples_to_features,
 batched=True)
columns = ["input_ids", "labels", "attention_mask"]
dataset_samsum_pt.set_format(type="torch", columns=columns)

