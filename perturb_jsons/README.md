# **JSON files relating to the Question-Answer pairs and Metadata**

## **Below mentioned is the file structure for Question-Answering pairs for RobustCQA**

```
└── perturb_jsons
    ├───complex_complex 
    |   ├───JSON files for QA
    ├───complex_simple    
    |   ├───JSON files for QA
    ├───simple_complex
    |   ├───JSON files for QA
    └───simple_simple
        ├───JSON files for QA
```

### **General Information about the files:**

1. The naming scheme for each folder is as follows: `<chart_type>_<question_type>` where chart_type represents the complexity of the chart and question type represents the complexity of the question in the question-answer pairs. For example, `complex_simple` contains the question-answer pairs where the charts are complex and the questions are simple.

2. Each folder contains the JSON files for the respective type of question-answer pairs. For example, the `complex_complex` folder contains the JSON files for the question pairs with complex charts and complex questions.

3. Within each folder, the JSON files are named as follows: `<type_of_perturbation>.json` where type_of_perturbation represents the type of perturbation applied to the original chart. For example, `log_scale.json` contains the question-answer pairs for the log scale perturbation applied to the original chart.

4. The structure of each QA JSON pair is as follows:
    ```
    {
        "imgname": <Name of the image used>,
        "query": <Question>,
        "label": <Answer>,
        "q_set": <'Human' or 'Augmented', splits are defined in the paper>,
        "perturbation": <ID of the perturbation type>,
        "perturbation_description": <A small description of the perturbation type>
    }
    ```