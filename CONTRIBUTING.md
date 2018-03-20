## Setup 
py3.5+ required


* Create isolated env for local development. In project folder type
  ```sh
  $ python3 -m venv env
  ```
* Activate env
  ```sh
  $ source env/bin/activate
  ```
  
* Install dev requirements
  ```sh
  $ pip install -r requirements_dev.txt
  ```
  
* Running tests
  ```sh
  pytest --cov ./aiohttp_jwt/ --cov-report=term  tests/
  ```
 
