import torch
from transformers import AutoModel, AutoTokenizer
import matplotlib.pyplot as plt
import pandas as pd
import json
torch.set_grad_enabled(False)
from intern_utils import *
import os
from glob import glob

# init model and tokenizer
model = AutoModel.from_pretrained('internlm/internlm-xcomposer2-vl-7b', trust_remote_code=True).eval()
model.half()
model.to("cuda")

tokenizer = AutoTokenizer.from_pretrained('internlm/internlm-xcomposer2-vl-7b', trust_remote_code=True)

def askInternLM(prompt, question, image_path):
    query = f'<ImageHere>{prompt} {question}'
    image = f'{image_path}'
    with torch.cuda.amp.autocast():
        response, _ = model.chat(tokenizer, query=query, image=image, history=[], do_sample=False)
    return response

chart_type = "complex"
ques_type = "complex"

os.makedirs(f"../Results/InternLM_XComposer2VL/{chart_type}_{ques_type}/Initial_run", exist_ok=True)

prompt  = """You will be given a chart and a question pertaining to it. Explain your answer, and at the last of your response, append in the form: "... . The answer is: <answer>". Let's think step by step and make sure we reach the correct output.
Question: """

categories = os.listdir("../perturb_jsons/{}_{}".format(chart_type, ques_type))
categories = [os.path.basename(category).split(".")[0] for category in categories]

global_answers = {}
category_wise_scores = {}

categories = sorted(categories)

for category in categories:
    print("running for category:", category)
    print()
    df = pd.read_json('../perturb_jsons/{}_{}/{}.json'.format(chart_type, ques_type, category))
    questions = df['query'].tolist()
    gold_labels = df['label'].tolist()
    imagenames = df['imgname'].tolist()
    perturbations = df['perturbation'].tolist()
    imagenames = [f"../final_data/{chart_type}_{ques_type}/plots/{perturbation}/{imagename}" for perturbation, imagename in zip(perturbations, imagenames)]

    model_responses = []
    for L in range(0, len(questions)):
        response = askInternLM(prompt, questions[L], imagenames[L])
        model_responses.append(response)
        print(".", end="")
    print()
    with open(f'../Results/InternLM_XComposer2VL/{chart_type}_{ques_type}/Initial_run/{category}.json', 'w') as f:
        json.dump(model_responses, f)
    print("saved the responses for category:", category)
    del model_responses
    del df
    del questions
    del gold_labels
    del imagenames
    torch.cuda.empty_cache()
            