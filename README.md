<center><img src="RobustCQA-10-3-2024.png" alt="RobustCQA dataset" /></center>

## **Data for the RobustCQA dataset**
#### *This repository contains the dataset and implementation details for the RobustCQA dataset, as mentioned in the paper [Unraveling the Truth: Do LLMs really Understand Charts? A Deep Dive into Consistency and Robustness](https://arxiv.org/abs/2407.11229).*

### **Overview**
The RobustCQA dataset is a collection of question-answer pairs for charts, which are designed to test the consistency and robustness of Vision language models (VLMs) in understanding charts through systematic manipulation of various chart elements while preserving the underlying data. The dataset is originally based on the ChartQA dataset and contains question-answer pairs for simple and complex charts and questions. 

### **Structure**

This directory has been broken down into three sub-directories:
```
└── RobustCQA
    ├───final_data
    │   └───README.md
    ├───model_scripts
    │   └───README.md
    ├───perturb_jsons
    │   └───README.md
    ├───Evaluation_Metric.py
    └───requirements.txt
```
***Details about each sub-directory are mentioned in the respective README files of each sub directory.***

### **Evaluation Metric**
The `Evaluation_Metric.py` file contains the improved `Relaxed Accuracy` metric, as mentioned in the paper.

### **Usage**
Clone the repository and follow the instructions in the README files of each sub-directory to use the dataset and scripts provided in this repository. 
Create a virtual environment and install the required dependencies using the following command:
```bash
pip install -r requirements.txt
```

### **Citation**

To cite our work, please use the following BibTeX entry:
```bibtex
@misc{mukhopadhyay2024unravelingtruthllmsreally,
      title={Unraveling the Truth: Do LLMs really Understand Charts? A Deep Dive into Consistency and Robustness}, 
      author={Srija Mukhopadhyay and Adnan Qidwai and Aparna Garimella and Pritika Ramu and Vivek Gupta and Dan Roth},
      year={2024},
      eprint={2407.11229},
      archivePrefix={arXiv},
      primaryClass={cs.CL},
      url={https://arxiv.org/abs/2407.11229}, 
}
```
