# Kayak project readme

* The specs of the project are here : https://app.jedha.co/course/project-plan-your-trip-with-kayak-ft/plan-your-trip-with-kayak-ft

## Read the .pptx first
* Everything is in the title... We can't do it for you
* The content of the slides is mainly a cut-and-paste of what's available in the project notebook(s) and other files
* The idea is that the slides should help you understand the project and its results, guiding you step by step

## Files of the project 
```
tree /f
./
│   01_kayak_project.pptx
│   02_kayak_part1.ipynb
│   03_kayak_part2.ipynb
│   include_kayak.py
│   my_api_id.py
│   readme.md
│   scraper8_attributes.py
│   scraper9_hotels_per_city.py
│   
├───assets
│   │   cities.csv
│   │   hotels_attributes.json
│   │   hotels_list.json
│   │   scrapy.log
│   │   sqlite.png
│   │   travel_data.csv
│   │   travel_data.sql
│   │   travel_data.sqlitevv
│   │
│   └───heap
│          Old stuff... 
└───__pycache__
        ...
```

``assets`` : This directory include some screen captures, backup, preliminary testing... If needed this is where the notebook read the dataset, store the log files, save some ``.json`` or ``.csv`` files...

``__pycache__`` : A directory where Python stores compiled bytecode files to speed up script execution. It helps reduce loading times by avoiding recompilation of the source code on subsequent runs. It is NOT pushed on Github but will be created locally when needed

* The file ``my_api_id.py`` will be missing on Github. Indeed this file contains my keys to access S3 and various API. It is not pushed on github.
* ``include_kayak.py`` is just a set of constant definitions shared among the files of the project.

## How to use the project ?
1. Open and run ``kayak_part1.ipynb``
    * It generates one file `.\Project_Kayak\assets\cities.csv`
    * It also display the ranked cities on a map 
    * Most of the <span style="color:orange"><b>Comments </b></span> cells are NOT about the code but about the results, the data and ideas we want to share etc.

1. Open and run ``kayak_part2.ipynb``
    * Based on the content of `\assets\cities.csv` it generate diffrents intermediates files
    * All the intermediates and log files are stored in ``./assets`` directory
    * In addition to cities.csv you should find 
        * ``hotels_attributes.json`` : list of attributes (comment, lon, lat...) for each hotel of the current town
        * ``hotels_list.json`` : list of hotels for the current town
        * ``scrapy.log`` : the log of the last scraping session
        * ``travel_data.csv`` : the file with all the collected data. It is a copy of the csv file available on S3 
        * ``travel_data.sql`` : sql schema of travel_date.csv
        * ``travel_data.sqlite`` : sqlite version of the travel_date.csv 
        * Few .png files
    * Most of the <span style="color:orange"><b>Comments </b></span> cells are NOT about the code but about the results, the data and ideas we want to share etc.
1. One could run ``scraper9_hotels_per_city.py`` or ``scraper8_attributes.py`` from the terminal without parameters. It is the best method for debug.


## Side note
* If you know nothing about Scrapy 
* In VSCODE
* Open a terminal
* Type `scrapy shell "https://quotes.toscrape.com/page/1/"`
* Read https://docs.scrapy.org/en/latest/intro/tutorial.html
* Type ``exit`` to quit

