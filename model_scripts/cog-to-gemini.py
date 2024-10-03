# dependencies 
import google.generativeai as genai
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
from glob import glob
import os
import json
from evaluation_utils import modified_relaxed_accuracy

genai.configure(api_key= '')

generation_config = {
  "temperature": 0,
  "top_p": 1,
  "top_k": 1,
  "max_output_tokens": 2048,
}
safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_NONE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_NONE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_NONE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_NONE"
  }
]
# you can choose to change model here
model = genai.GenerativeModel('gemini-1.5-flash-latest', safety_settings=safety_settings, generation_config=generation_config)

model.generate_content("Valid connection")

prompt = """You are an expert in getting the answers from a given long answer with steps. These questions were asked about a chart.
Task: Extract the final answer based on the given long sequence of reasoning with answer, given the question.
 
Instructions:
Append to your response and reasoning: 'The answer is: <final_answer>'. 

If a question asks about a column name, give the full and exact name for the column as it is written in answer. 
If a question required multiple outputs and the output contains multiple outputs as well, give it in the form: [<output1>, <output2> ..] where outputs are in sorted order. For example, if the output is 'Australia and India' give the answer as [Australia, India]. 
Ignore percentage signs.
Remove the units from the answer. For example, if the answer is '10 million', give the answer as '10'. 

A few examples:

Question: What is the value of the blue column?
Given Answer: The blue column has the name 'XXX' and the value is 10.
Your Answer: <reasoning>. The answer is: 10

Question: What is the share of people above 65+ years in the small business category?
Given Answer: To find the share of SME owners in small business over 65 years, we need to add the percentages for the '65-69 years' and '70-74 years' age groups. The calculation is as follows: 26.1% (65-69 years) + 11.8% (70-74 years) = 37.9%. So, the share of SME owners in small business over 65 years is 37.9%.
Your Answer: <reasoning>. The answer is: 37.9

Where <reasoning>. is your reasoning and your chain of thought to get to the answer.

You need to carefully look at the question and the given answer. Think step by step.

Question: {question}
Given Answer: {answer}"""

    
def get_results(queries, max_workers=10):
    with ThreadPoolExecutor() as executor:
        executor._max_workers = max_workers
        results = list(executor.map(generate_content, queries))
    return results

def generate_content(query):
    try:
        resp = model.generate_content(query)
        print(".", end="")
        return resp.text
    except Exception as e:
        print(e)
        return 'Error by gemini'
  
chart_type = "simple"
question_type = "simple"

categories = os.listdir('../Results/cog_agent/{chart_type}_{ques_type}/Initial_Run/')
categories = [c.split('.')[0] for c in categories]

for category in categories:
    df = pd.read_json('../perturb_jsons/{}_{}/{}.json'.format(chart_type, ques_type, category))
    questions = df['query'].tolist()
    gold = df['label'].tolist()
    pred = json.load(open(f'../Results/cog_agent/{chart_type}_{ques_type}/Initial_Run/{category}.json','r'))
    assert(len(pred) == len(questions))
    queries = [prompt.format(question=question, answer=answer) for question, answer in zip(questions, pred)]
    with ThreadPoolExecutor() as executor:
        executor._max_workers = 16
        model_responses = list(executor.map(generate_content, queries))
    copy = model_responses.copy()
    for i, resp in enumerate(copy):
        resp = resp.strip()
        if(resp[-1] == '.'):
            resp = resp[:-1]
        if 'The answer is: ' in resp:
            x = resp.split('The answer is: ')
            model_responses[i] = x[1]
        elif 'the answer is: ' in resp:
            x = resp.split('the answer is: ')
            model_responses[i] = x[1]
        elif 'The answer is ' in resp:
            x = resp.split('The answer is ')
            model_responses[i] = x[1]
        else:
            print(i, "error by gemini")

    results = list(zip(questions, model_responses))
    final_responses = []
    for result in results:
        question, response = result
        final_responses.append(response.strip())
        
    final_responses = [response.split('=')[-1] for response in final_responses]
    final_responses = [response.split('%')[0] for response in final_responses]

    model_performance = []
    results = list(zip(questions, model_responses))
    for i, ans in enumerate(final_responses):
        model_score = modified_relaxed_accuracy(questions[i],gold[i], ans)
        model_performance.append(model_score)
        # print(f"Question: {questions[i]}\nGold: {gold[i]}\nIntern_ans: {pred[i]}\nPredicted: {ans}\nCorrect: {model_score}\n\n")
    
    print(f"For Category: {category}")
    print("Model performance: ", sum(model_performance),"out of", len(model_performance),">>", sum(model_performance)/len(model_performance))
    print("-------------------------------------------------")

    json.dump()
