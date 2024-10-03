import torch 
import pandas as pd
from transformers import AutoModelForCausalLM, LlamaTokenizer
from PIL import Image
import json
import os
from glob import glob

tokenizer = LlamaTokenizer.from_pretrained("lmsys/vicuna-7b-v1.5")
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
torch_type = torch.bfloat16

model = AutoModelForCausalLM.from_pretrained(
    'THUDM/cogagent-vqa-hf',
    torch_dtype=torch.bfloat16,
    low_cpu_mem_usage=True,
    trust_remote_code=True,
    ).cuda().eval()

def ask_cog_agent(image_path, query, history=[], temperature=0.9, do_sample=False):
    """
    Get the response from the cogagent based on the given image, query, and conversation history.

    Parameters:
    - image_path (str): Path to the image file.
    - query (str): The current query prompt.
    - history (list): List of tuples containing the conversation history.
    - temperature (float): Sampling temperature for response generation (default is 0.9).
    - do_sample (bool): Whether to use sampling during response generation (default is False).

    Returns:
    - str: The generated response from the cogagent.
    """
    image = Image.open(image_path).convert('RGB')

    input_by_model = model.build_conversation_input_ids(tokenizer, query=query, history=history, images=[image])
    inputs = {
        'input_ids': input_by_model['input_ids'].unsqueeze(0).to(DEVICE),
        'token_type_ids': input_by_model['token_type_ids'].unsqueeze(0).to(DEVICE),
        'attention_mask': input_by_model['attention_mask'].unsqueeze(0).to(DEVICE),
        'images': [[input_by_model['images'][0].to(DEVICE).to(torch_type)]],
    }
    if 'cross_images' in input_by_model and input_by_model['cross_images']:
        inputs['cross_images'] = [[input_by_model['cross_images'][0].to(DEVICE).to(torch_type)]]

    gen_kwargs = {"max_length": 4096, "temperature": temperature, "do_sample": do_sample}

    with torch.no_grad():
        outputs = model.generate(**inputs, **gen_kwargs)
        outputs = outputs[:, inputs['input_ids'].shape[1]:]
        response = tokenizer.decode(outputs[0])
        response = response.split("</s>")[0]
    return response

chart_type = "complex" # or "simple"
ques_type = "complex" # or "simple"

os.makedirs(f"../Results/cog_agent/{chart_type}_{ques_type}/Initial_Run", exist_ok=True)

prompt  = """You will be given a chart and a question pertaining to it. Explain your answer, and at the last of your response, append in the form: "<your reasoning steps>. The answer is: <answer>". Let's think step by step.
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
        response = ask_cog_agent(imagenames[L], prompt + questions[L])
        model_responses.append(response)
        print(".", end="")
    print()
    with open(f'../Results/cog_agent/{chart_type}_{ques_type}/Initial_Run/{category}.json', 'w') as f:
        json.dump(model_responses, f)
    print("saved the responses for category:", category)
    del model_responses
    del df
    del questions
    del gold_labels
    del imagenames
    torch.cuda.empty_cache()
            