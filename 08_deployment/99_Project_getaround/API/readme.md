# Local test (WIN11)

* In in your Python environment you may have to install 
    * uvicorn
    * fastapi 

* From the ``API`` directory, open a new terminal 
* Type in : `python .\api_getaround.py`
* Use a web brwoser and open `http://localhost:8000`

<p align="center">
<img src="./assets/local_welcome.png" alt="drawing" width="800"/>
<p>

* Read the instructions and copy the string : ["Citroën","140411","100","diesel","black","convertible",true,true,false,false,true,true,true]
* Now, point your browser to `http://localhost:8000/docs`
* To make a first test use these parameters : ["Citroën","140411","100","diesel","black","convertible",true,true,false,false,true,true,true]
* The prediction should be : 114€

* Send anything and you will get an exception

<p align="center">
<img src="./assets/local_exception.png" alt="drawing" width="800"/>
<p>


* Now, open a new terminal
    * Send a request : ``curl -i -H "Content-Type: application/json" -X POST -d '{"input": [["Citroën","140411","100","diesel","black","convertible",true,true,false,false,true,true,true]]}' localhost:8000/predict``
    * Make sure to write <span style="color:green"><b>true & false</b></span> and NOT <span style="color:red"><b>True & False</b></span>

<p align="center">
<img src="./assets/local_docs.png" alt="drawing" width="800"/>
<p>




# Docker : local test (WIN11)

* Make sure Docker up and is running (I always forgot this step...)
* Open an integrated terminal in VSCode in the ``API`` directory
* Type in : `./build_api_getaround.ps1`
* At the end``api_gataround`` should be available in Docker

<p align="center">
<img src="./assets/docker_image.png" alt="drawing" width="800"/>
<p>

* Type in : ``docker run -p 8000:8000 api_getaround``
* Point your favorit web browser to : `http://localhost:8000/docs`
* You can then make the same test as before

<p align="center">
<img src="./assets/docker_local_docs.png" alt="drawing" width="800"/>
<p>


* Again you can requesr a prediction with :
    * ``curl -i -H "Content-Type: application/json" -X POST -d '{"input": [["Citroën","140411","100","diesel","black","convertible",true,true,false,false,true,true,true]]}' localhost:8000/predict``
    * ``curl -i -H "Content-Type: application/json" -X POST -d '{"input": [["Citroën","140411","100","diesel","black","convertible",true,true,false,false,true,true,true]]}' 127.0.0.1:8000/predict``
    * Check `C:\Windows\System32\drivers\etc\hosts` to understand why both url works

<p align="center">
<img src="./assets/curl_docker_local.png" alt="drawing" width="800"/>
<p>


* Stop the container
    * Open an new terminal (CTRL+SHIF+ù)
    * ``docker ps``
    * `docker stop quizzical_tu`
    * ``docker ps``


# Deployment on Heroku
* Make sure Heroku CLI is installed
    * https://devcenter.heroku.com/articles/heroku-cli
* Open an integrated terminal in VSCode in the ``API`` directory
* Check heroku : ``heroku --version``
* ``heroku login``
    * blablabla...
* ``heroku container:login``
* ``heroku create api-getaround`` Please note that here we use a “-” and NOT a “_” (the latter is not allowed by Heroku ). 
* ``heroku stack:set container -a api-getaround``
* ``heroku container:push web -a api-getaround`` (this may take a while...)
* ``heroku container:release web -a api-getaround``
* You can then test the API online
    * Point to https://api-getaround-4ece015745ea.herokuapp.com/
    * Read the doc and copy the string

<p align="center">
<img src="./assets/heroku_welcome.png" alt="drawing" width="800"/>
<p>

* Make some test using the string you just copy

<p align="center">
<img src="./assets/heroku_predict.png" alt="drawing" width="800"/>
<p>

* From a terminal, get prediction using curl

<p align="center">
<img src="./assets/heroku_curl.png" alt="drawing" width="800"/>
<p>

