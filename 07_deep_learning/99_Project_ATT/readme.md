# AT&T project readme

* The specs of the project are here : https://app.jedha.co/course/projects-deep-learning-ft/att-spam-detector-ft


## Read the .pptx first
* Everything is in the title... We can't do it for you
* The content of the slides is mainly a cut-and-paste of what's available in the project notebook(s) and other files
* The idea is that the slides should help you understand the project and its results, guiding you step by step


## Files of the project 

```
tree /f
./
│   01_att_project.pptx
│   02_att_01.ipynb     # Baseline model
│   02_att_02.ipynb     # Baseline + SMOTE
│   02_att_03.ipynb     # Baseline + Random Under Sampler
│   03_bert01.ipynb     # TF Bert model uncased
│   03_bert02.ipynb     # TF Bert model cased
│   03_bert03.ipynb     # TF Bert For Sequence Classification model uncased
│   readme.md
│   
├───assets
│       basic_loss.png
│       best_model.h5
│       cnn_loss.png
│       lstm_loss.png
│       model_basic.png
│       requirements.txt
│       spam.csv
|       ...
│
└───logs
    ├───train
    └───validation

```

``assets`` : This directory include some screen captures, backup, preliminary testing... If needed this is where the notebook read the dataset, store the log files, save some ``.json`` or ``.csv`` files...

`logs` : the train and validation logs of the BERT model. Used by tensorboard.
1. Once the model runs
1. 0pen a terminal and type in : ``tensorboard --logdir=logs``
1. Visit the url with your browser

## Virtual env ?
* I strongly recommend to create a python virtual environment
* If you use ``conda`` follow the instructions below

### Option 1 - recommended
```
WIN + X + I                            # to open a terminal
conda deactivate                       # to come back in the base virtual environment 
conda create --name tf_cpu1 --file ./assets/requirements.txt -c conda-forge -y
conda activate tf_cpu1
code .
```

### Option 2
```
WIN + X + I                            # to open a terminal
conda deactivate                       # to come back in the base virtual environment 
conda create --name tf_cpu1 python=3.10 -y
conda activate tf_cpu1
conda install pandas numpy tensorflow wordcloud matplotlib plotly scikit-learn spacy-model-en_core_web_sm nbformat graphviz pytdot imbalanced-learn -y
code .
# VSCode will ask to install ipykernel
```





## How to use the project ?
* Read the slides

### Running the baseline model 
* Open, read and run the notebook ``02_att_01.ipynb``
    * Compared to ``02_att_01.ipynb``, ``02_att_02.ipynb`` and ``02_att_03.ipynb`` simply add over and under sampling

### Running the TF BERT model
* You want to run ``03_bert_01.ipynb`` and ``03_bert_02.ipynb`` 
    * Because of version issues between tensorflow, keras, transformers... 
    * You should create a new virtual environment (see below) 
    * open a terminal in the root directory of the project 
    ```    
        conda deactivate                   # to come back in base environment
        conda create --name tf_cpu_bert_model --file .\07_deep_learning\99_Project_ATT\assets\requirements_tf_cpu_bert_model.txt -c conda-forge -y
        conda activate tf_cpu_bert_model
        code . v
    ```    
    * read and run ``03_bert_01.ipynb`` or ``03_bert_02.ipynb`` 
    * The training can be very looooong (more than 01H00 typically)

### Running the TF Bert For Sequence Classification model
* **I'M STILL WORKING ON IT**
    * A nightmare from the version management point of view
* You want to run ``03_bert_03.ipynb``  
    * Because of version issues between tensorflow, keras, transformers... 
    * You should create a third virtual environment 
    * open a terminal in the root directory of the project 
    ```    
        conda deactivate                   # to come back in base environment
        conda create --name tf_cpu_bert_seq_model --file .\07_deep_learning\99_Project_ATT\assets\requirements_tf_cpu_bert_seq_model.txt -c conda-forge -y
        conda activate tf_cpu_bert_seq_model
        code . 
    ```    
    * Read then run ``03_bert_03.ipynb``  
 

* Most of the <span style="color:orange"><b>Comments </b></span> cells are NOT about the code but about the results, the data and ideas we want to share etc.


## About contributions
This project was developed for personal and educational purposes. Feel free to explore and use it to enhance your own learning in machine learning.

Given the nature of the project, external contributions are not actively sought or encouraged. However, constructive feedback aimed at improving the project (in terms of speed, accuracy, comprehensiveness, etc.) is welcome. Please note that this project was created as part of a certification process, and it is unlikely to be maintained after the final presentation.

