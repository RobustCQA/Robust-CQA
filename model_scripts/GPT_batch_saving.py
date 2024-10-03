from openai import OpenAI
import json
import os

client = OpenAI(api_key = "")

batch_ids = json.load(open(f"batch_ids.json","r"))

# loop through all the batch_ids
for batch_name in batch_ids.keys():
    print(f"Processing batch_name: {batch_name}")
    batch_id = batch_ids[batch_name]
    batch = client.batches.retrieve(batch_id)
    print(f"Batch status: {batch.status}")
    if batch.status == "completed":
        print(f"Downloading batch_id: {batch_id}")
        content = client.files.content(batch.output_file_id)
        chart_type, ques_type, category = batch_name.split("_")
        os.makedirs(f"GPT_final_output/{chart_type}_{ques_type}", exist_ok=True)
        content.write_to_file(f"GPT_final_output/{chart_type}_{ques_type}/{category}.jsonl")