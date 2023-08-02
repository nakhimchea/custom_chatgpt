# CX ChatGPT
This is the custom package to run ChatGPT as endpoints with transfer learning techniques. 
* Train own organization data to match business needs and feed it to knowledge base in the form of GPTSimpleVectorIndex.
* Retrieve data from one's organizations' data combined with ChatGPT-3.5-turbo and response back to user queries.

# Installation
This project is using Python version 3.11.4 with PIP requirements as in "requirements.txt" file.
* Check current working directory command:
  - pwd
* Check python version command: 
  - python --version
* Get virtual environment command: 
  - python -m venv .cx
* Activate environment command: 
  - source .cx/bin/activate
* Recheck python version and libraries command: 
  - python --version && pip freeze
* Install requirements command:
  - python -m pip install -r requirements.txt

Now we need to create a knowledge base for the transferred learning. This Python main script is to read Excel file and 
write to firestore. Then, a knowledge base created under a folder name "storage" to contain all store files.
* command: python main.py

After created a knowledge base, we can run the script to listen for request from the user with uvicorn library.
* command: uvicorn main:app

# Docker Setup
