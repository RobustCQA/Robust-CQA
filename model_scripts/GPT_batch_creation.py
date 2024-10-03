import pandas as pd
from glob import glob
import os
import json
import base64
import PIL.Image

chart_type = "complex" # "simple" or "complex"
question_type = "complex" # "simple" or "complex"

def decode_image(base_64_string):
    image_data = base64.b64decode(base_64_string)
    image = PIL.Image.open(io.BytesIO(image_data))
    return image

def encode_image(image_path):
    with open(image_path, "rb") as image:
        return base64.b64encode(image.read()).decode("utf-8")
    
prompt = """ Task: You will be given a chart and a question. Answer the given question from the chart given to you.  
Instructions: 
0) Look carefully at the chart, think about the type of chart, before answering the question directly.
1) If a question asks about a column name, give the full and exact name for the column as it is written in the chart. 
2) If a question required multiple outputs, give it in the form: [<output1>, <output2> ..] where outputs are in sorted order. For example, if the output is 'Australia and India' give the answer as [Australia, India]. Please dont use this with column names invloving 'and' keyword. 
3) If a question requires doing arithmetic operations, calculate till the final number.
4) If a question asks for what column a certain value is in, give the full and exact name of the column and not the value.
5) If a question asks how many times a certain value appears, give the count and not the name of the columns where it appears.
6) Answer without taking account of the units or scale given in chart. For example, if the chart has values in millions, you should ignore the scale and account absolute numbers. Remove the unit from your final answer and reason based on the absolute values obtained directly from the chart. Example: If your answer is 10 million USD, you should write 10 as your answer.
7) It is known that the answer is obtainable from the chart given to you.
8) Write your intermediate steps.

The chart might not have exact values written on it, therefore you might need to find the exact value in that case with the help of the axes.
Think step by step and append the answer at the last of your response in the form: "... . The answer is: <answer>"
Question: """

def format_payload(id, prompt, question, base64_image):
    payload = {
        "custom_id" : id,
        "method" : "POST",
        "url" : "/v1/chat/completions",
        "body" : {
        "model": "gpt-4o",
        "messages": [
            {
            "role": "user",
            "content": [
                {
                "type": "text",
                "text": prompt + question
                },
                {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{base64_image}",
                }
                }
            ]
            }
        ],
        "max_tokens": 1000
        }
    }
    return payload

categories = os.listdir("../perturb_jsons/{}_{}".format(chart_type, question_type))
categories = [os.path.basename(category).split(".")[0] for category in categories]

for category in categories:
    os.makedirs(f"./GPT_batches/{chart_type}_{question_type}", exist_ok=True)
    df = pd.read_json(f"../perturb_jsons/{chart_type}_{question_type}/{category}.json")
    questions = df['query'].tolist()
    gold_labels = df['label'].tolist()
    imagenames = df['imgname'].tolist()
    perturbations = df['perturbation'].tolist()
    imagenames = [f"../final_data/{chart_type}_{question_type}/plots/{perturbation}/{imagename}" for perturbation, imagename in zip(perturbations, imagenames)]

    payloads = [format_payload(f"{chart_type}_{question_type}_{category}_{i}", prompt, questions[i], encode_image(imagenames[i])) for i in range(len(questions))]
    for i, payload in enumerate(payloads):
        with open(f"./GPT_batches/{chart_type}_{question_type}/{category}.jsonl", "a") as f:
            json.dump(payload, f)
            f.write("\n")

