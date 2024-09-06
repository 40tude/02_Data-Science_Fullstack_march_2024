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
C:.
│   01_att_project.pptx
│   02_att.ipynb
│   03_bert.ipynb
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
* We recommend to create a python virtual environment
* If you use ``conda`` follow the instructions below
    * If not, you should be able to use `./assets/requirements.txt` your way

```
WIN + X + I                            # to open a terminal
conda create --name att python=3.10
conda activate att
code .

# VSCode will ask to install ipykernel

# Open a terminal in VScode, double check that att is the current environment 
# Once this is done install the following packages by hand
conda install tensorflow
conda install pydot
conda install spacy
conda install pandas
conda install wordcloud
conda install scikit-learn 
conda install plotly
conda install nbformat
conda install transformers
python -m spacy download en_core_web_sm

# or use ./assets/requirements.txt
conda install --yes --file requirements.txt

```


## How to use the project ?
* Open, read and run the notebook ``02_att.ipynb``
* If you want to try BERT model, open, read and run `03_bert.ipynb`
    * This can be very looooong (01H00 typically)
* Most of the <span style="color:orange"><b>Comments </b></span> cells are NOT about the code but about the results, the data and ideas we want to share etc.


## About contributions
This project was developed for personal and educational purposes. Feel free to explore and use it to enhance your own learning in machine learning.

Given the nature of the project, external contributions are not actively sought or encouraged. However, constructive feedback aimed at improving the project (in terms of speed, accuracy, comprehensiveness, etc.) is welcome. Please note that this project was created as part of a certification process, and it is unlikely to be maintained after the final presentation.

