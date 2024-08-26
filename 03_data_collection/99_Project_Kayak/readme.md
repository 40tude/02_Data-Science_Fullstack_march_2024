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
│   │   travel_data.sqlite
│   │
│   └───heap
│          Old stuff... 
└───__pycache__
        ...
```
* the file ``my_api_id.py`` will be missing. Indeed this file contains my keys to access S3 and various API. It is not pushed on github.
* include_kayak.py is just a set of constant definitions shared among the files of the project.

## How to use the project ?
1. Open and run ``kayak_part1.ipynb``
    * It generates one file `.\Project_Kayak\assets\cities.csv`
    * It also display the ranked cities on a map 
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
1. One could run ``scraper9_hotels_per_city.py`` or ``scraper8_attributes.py`` from the terminal without paramaters. It is the best method for debug


## Side note
* If you know nothing about Scrapy 
* In VSCODE
* Open a terminal
* Type `scrapy shell "https://quotes.toscrape.com/page/1/"`
* Read https://docs.scrapy.org/en/latest/intro/tutorial.html
* Type ``exit`` to quit

