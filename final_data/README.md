# **Data for RobustCQA dataset**

## **Below mentioned are the files for running the Question-Answering on RobustCQA**

```
└── final_data
    │
    ├───complex_complex
    │   ├───annotations
    │   │   └───<QA_ID>.json
    │   ├───plots
    │   │   └───<Perturbation_ID>
    │   │       └───<QA_ID>.png
    │   ├───scripts
    │   │   └───<Perturbation_ID>.py
    │   └───tables
    │       └───<QA_ID>.csv
    │
    ├───complex_simple
    ├───simple_complex
    └───simple_simple
```

### **General Information about the files:**

1. The naming scheme for each folder is as follows: `<chart_type>_<question_type>` where chart_type represents the complexity of the chart and question type represents the complexity of the question in the question-answer pairs. For example, `complex_complex` contains the question-answer pairs where both the charts and the questions are complex.

2. Each folder contains four subfolders: `annotations`, `plots`, `scripts`, and `tables`. The details are mentioned below:
    - **annotations**: Contains the original metadata provided by the ChartQA dataset. Each file is named as `<QA_ID>.json` where QA_ID represents the unique identifier for the question-answer pair. The structure of the JSON file is the same as the original metadata provided by the ChartQA dataset.

    - **plots**: Contains folders named <Perturbation_ID>, where each folder contains the perturbed images generated using the Python scripts in the `scripts` folder. Each image is named as `<QA_ID>.png` where QA_ID represents the unique identifier for the question-answer pair.

    - **scripts**: Contains the Python scripts for generating the perturbed images. The scripts are named as `<Perturbation_ID>.py` where Perturbation_ID represents the unique identifier for the perturbation type.

    - **tables**: Contains the CSV files which were obtained through the processing of the metadata provided by the ChartQA dataset. Each file is named as `<QA_ID>.csv` where QA_ID represents the unique identifier for the question-answer pair. 
