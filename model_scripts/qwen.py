# dependencies 
import torch 
import pandas as pd
import os
import json
from modelscope import snapshot_download
from transformers import AutoModelForCausalLM, AutoTokenizer
from evaluation_utils import modified_relaxed_accuracy

model_dir = snapshot_download('qwen/Qwen-VL')

tokenizer = AutoTokenizer.from_pretrained(model_dir, trust_remote_code=True)

model = AutoModelForCausalLM.from_pretrained(
    model_dir,
    device_map="cuda:0",
    trust_remote_code=True
).eval()

tokenizer.pad_token = '<|endoftext|>'
tokenizer.padding_side = 'left'

chart_type = "complex"
question_type = "complex"

os.makedirs(f"../Results/Qwen-VL/{chart_type}_{question_type}/", exist_ok=True)

categories = os.listdir("../perturb_jsons/{}_{}".format(chart_type, question_type))
categories = [os.path.basename(category).split(".")[0] for category in categories]
categories = sorted(categories)

global_answers = {}
category_wise_scores = {}

for category in categories:
    print("running for category:", category)
    print()
    df = pd.read_json('../perturb_jsons/{}_{}/{}.json'.format(chart_type, question_type, category))
    questions = df['query'].tolist()
    gold_labels = df['label'].tolist()
    imagenames = df['imgname'].tolist()
    perturbations = df['perturbation'].tolist()
    imagenames = [f'../final_data/{chart_type}_{question_type}/plots/{pert}/{img}.png' for img, pert in zip(imagenames, perturbations)]
    
    queries = []
    for i, question in enumerate(questions):
        text = question + ' Answer:'
        queries.append(tokenizer.from_list_format([
                {'image': imagenames[i]},
                {'text': text},
        ]))  

    batch_size = 8
    batches = [queries[i:i+batch_size] for i in range(0, len(queries), batch_size)] 
       
    model_responses = []
    for batch in batches:
        inputs = tokenizer(batch, return_tensors='pt', padding=True, truncation=True)
        inputs.to(model.device)
        with torch.no_grad():
            try:
                outputs = model.generate(**inputs)
            except:
                print("bad output")
        generated = tokenizer.batch_decode(outputs, skip_special_tokens=True)
        model_responses.extend(generated)
        print("." * batch_size, end='')
    print()
        
    global_answers[category] = model_responses
    print("answers generated!")

    results = list(zip(questions, model_responses))
    final_responses = []
    for result in results:
        question, response = result
        new_response = response.split('Answer:')[-1].strip()
        new_response = new_response.split('%')[0].strip()
        final_responses.append(new_response)
        
    final_responses = [response.split('=')[-1] for response in final_responses]
    final_responses = [response.split('%')[0] for response in final_responses]

    model_performance = []
    results = list(zip(questions, model_responses))
    for i, ans in enumerate(final_responses):
        model_score = modified_relaxed_accuracy(questions[i],gold_labels[i], ans)
        model_performance.append(model_score)

    category_wise_scores[category] = sum(model_performance)
    print('Model accuracy:', sum(model_performance) / len(model_performance))
    print()
    
    # store resutls after each category
    with open(f"../Results/Qwen-VL/{chart_type}_{question_type}/results.json", "w") as f:
        json.dump(category_wise_scores, f)
    # store answers after each category
    with open(f"../Results/Qwen-VL/{chart_type}_{question_type}/answers.json", "w") as f:
        json.dump(global_answers, f)