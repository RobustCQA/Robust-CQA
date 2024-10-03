from openai import OpenAI
from glob import glob 
import os
import json

client = OpenAI(api_key = "Enter API Key Here")

batch_ids = {}

chart_types = ["complex", "simple"]
ques_types = ["complex", "simple"]

for chart_type in chart_types:
    for ques_type in ques_types: 
        categories = os.listdir("../perturb_jsons/{}_{}".format(chart_type, ques_type))
        categories = [os.path.basename(category).split(".")[0] for category in categories]
        for i, category in enumerate(categories):
          filename = category + ".jsonl"
          batch_input_file = client.files.create(
            file=open(f"./GPT_batches/{chart_type}_{ques_type}_{filename}", "rb"),
            purpose="batch"
          )
          batch = client.batches.create(
            input_file_id = batch_input_file.id,
            endpoint="/v1/chat/completions",
            completion_window="24h",
            metadata={
              "description": f"{chart_type}_{ques_type}_{category}"
            }
          )
          batch_ids[f"{chart_type}_{ques_type}_{category}"] = batch.id
          print(f"Batch {i} created with id: {batch.id}")

json.dump(batch_ids, open("batch_ids.json", "w"))