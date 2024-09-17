# Getaround project readme

* The specs of the project are here : https://app.jedha.co/course/project-deployment-ft/getaround-analysis-ft


## Read the .pptx first
* Everything is in the title... We can't do it for you
* The content of the slides is mainly a cut-and-paste of what's available in the project notebook(s) and other files
* The idea is that the slides should help you understand the project and its results, guiding you step by step


## Files of the project

```
tree /f
./
│   01_getaround_project.pptx
│   02_getaround_threshold.ipynb
│   03_getaround_pricing.ipynb
│   readme.md
│   
├───API
│   │   api_getaround.py
│   │   build_api_getaround.ps1
│   │   Dockerfile
│   │   environment.yml
│   │   readme.md
│   │   requirements.txt
│   │   test_pickle.ipynb
│   │   
│   ├───assets
│   │       full_pipeline.pkl
│   │       model_xgb.pkl
│   │
│   └───__pycache__
│
├───assets
│       environment.yml
│       full_pipeline.pkl
│       get_around_delay_analysis.xlsx
│       get_around_pricing_project.csv
│       model_xgb.pkl
│       requirements.txt
│       test_pickle.ipynb
│
└───dashboard
    │   build_dashboard_getaround.ps1
    │   dashboard.py
    │   deploy_dashboard_getaround.ps1
    │   Dockerfile
    │   readme.md
    │   requirements.txt
    │
    └───assets
            get_around_delay_analysis.xlsx
```


``assets`` : This directory include some screen captures, backup, preliminary testing... If needed this is where the notebook read the dataset, store the log files, save some ``.json`` or ``.csv`` files...


## How to use the project ?
1. Once you read the slides `01_getaround_project.pptx`
1. Then you can open and run `02_getaround_treshold.ipynb`
1. Finally open and run `03_getaround_pricing.ipynb`
1. Then go to to the ``./API`` and read the ``readme.md`` to get instructions
1. Do the same thing in the `./dashboard` directory

### Note
In the Jupyter Notebook above, most of the <span style="color:orange"><b>Comments </b></span> cells of the notebooks are NOT about the code but about the results, the data and ideas we want to share etc.


## About contributions
This project was developed for personal and educational purposes. Feel free to explore and use it to enhance your own learning in machine learning.

Given the nature of the project, external contributions are not actively sought or encouraged. However, constructive feedback aimed at improving the project (in terms of speed, accuracy, comprehensiveness, etc.) is welcome. Please note that this project was created as part of a certification process, and it is unlikely to be maintained after the final presentation.

