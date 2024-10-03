# dependencies 
import google.generativeai as genai
import pandas as pd
from PIL import Image
from concurrent.futures import ThreadPoolExecutor
import os
from evaluation_utils import modified_relaxed_accuracy

genai.configure(api_key= '') #API key

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
# or any model
model = genai.GenerativeModel('gemini-1.5-flash-latest', safety_settings=safety_settings, generation_config=generation_config)

model.generate_content("Valid connection")

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
        print(query, e)
        return 'Error by gemini'

chart_type = "simple"
question_type = "complex"

categories = os.listdir("../perturb_jsons/{}_{}".format(chart_type, question_type))
categories = [os.path.basename(category).split(".")[0] for category in categories]

global_answers = {}
category_wise_scores = {}

    
for category in categories:
    df = pd.read_json('../perturb_jsons/{}_{}/{}.json'.format(chart_type, question_type, category))
    questions = df['query'].tolist()
    gold_labels = df['label'].tolist()
    imagenames = df['imgname'].tolist()
    perturbations = df['perturbation'].tolist()
    imagenames = [f"../final_data/{chart_type}_{question_type}/plots/{perturbation}/{imagename}" for perturbation, imagename in zip(perturbations, imagenames)]
    images = [Image.open(img) for img in imagenames]

    queries = []

    for i, question in enumerate(questions):
        text = prompt + question
        queries.append([text, images[i]]) 

    model_responses = get_results(queries, max_workers= 16)
    print("answers generated!")
    copy = model_responses.copy()
    for i, resp in enumerate(copy):
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
        model_score = modified_relaxed_accuracy(questions[i],gold_labels[i], ans)
        model_performance.append(model_score)

    print('Category:', category)
    print('Model accuracy:', sum(model_performance) / len(model_performance))
    print()

    del model_responses
    del copy
    del results
    del final_responses
    del model_performance
    del df
    del questions
    del gold_labels
    del imagenames
    del perturbations
    del images
    
    