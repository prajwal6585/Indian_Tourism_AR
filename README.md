# Indian_Tourism_AR
This project promotes Indian tourism via a virtual platform using AR and AI. Users can search tourist locations, explore them in 360° Street Views, and interact with an AI chat system for insights. Built with Google Maps API and a Flask backend, it makes cultural heritage accessible globally.



https://github.com/user-attachments/assets/df7a7ad2-24dc-4bd5-b504-70d000330f89



https://github.com/user-attachments/assets/b04d5603-1baf-44b6-90c5-252c67484458



![image](https://github.com/user-attachments/assets/da1fbcbb-63b9-4994-be37-a7528c0fbdcb)


PROJECT SETUP:
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Step1:


visit https://cloud.mongodb.com/

creat account

create cluster

save username and password

copy the connection string


install mongodb compass

Click Add new connection

Paste the copied connection string here

Save and connect 

create Database

Database name  : indian_tourism_db

Collection Name: users

--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Step2:

Download and Install Miniconda Or Ananconda

open and create conda environment

conda create -n tourisumar python=3.9

conda activate tourisumar

Install all these packages

Project Dependencies

This project requires the following dependencies. Ensure these are installed in your environment before running the application.

| **Package Name**            | **Version**          | **Build**         | **Channel**   |
|-----------------------------|----------------------|-------------------|---------------|
| annotated-types             | 0.7.0               | pypi_0            | pypi          |
| blinker                     | 1.8.2               | pypi_0            | pypi          |
| ca-certificates             | 2024.9.24           | haa95532_0        | -             |
| cachetools                  | 5.5.0               | pypi_0            | pypi          |
| certifi                     | 2024.8.30           | pypi_0            | pypi          |
| charset-normalizer          | 3.4.0               | pypi_0            | pypi          |
| click                       | 8.1.7               | pypi_0            | pypi          |
| colorama                    | 0.4.6               | pypi_0            | pypi          |
| dnspython                   | 2.7.0               | pypi_0            | pypi          |
| email-validator             | 2.2.0               | pypi_0            | pypi          |
| flask                       | 3.0.3               | pypi_0            | pypi          |
| flask-login                 | 0.6.3               | pypi_0            | pypi          |
| flask-pymongo               | 2.3.0               | pypi_0            | pypi          |
| flask-wtf                   | 1.2.2               | pypi_0            | pypi          |
| google-ai-generativelanguage| 0.6.10              | pypi_0            | pypi          |
| google-api-core             | 2.22.0              | pypi_0            | pypi          |
| google-api-python-client    | 2.149.0             | pypi_0            | pypi          |
| google-auth                 | 2.35.0              | pypi_0            | pypi          |
| google-auth-httplib2        | 0.2.0               | pypi_0            | pypi          |
| google-generativeai         | 0.8.3               | pypi_0            | pypi          |
| googleapis-common-protos    | 1.65.0              | pypi_0            | pypi          |
| grpcio                      | 1.67.1              | pypi_0            | pypi          |
| grpcio-status               | 1.67.1              | pypi_0            | pypi          |
| httplib2                    | 0.22.0              | pypi_0            | pypi          |
| idna                        | 3.10                | pypi_0            | pypi          |
| importlib-metadata          | 8.5.0               | pypi_0            | pypi          |
| itsdangerous                | 2.2.0               | pypi_0            | pypi          |
| jinja2                      | 3.1.4               | pypi_0            | pypi          |
| markupsafe                  | 3.0.2               | pypi_0            | pypi          |
| openssl                     | 3.0.15              | h827c3e9_0        | -             |
| pip                         | 24.2                | py39haa95532_0    | -             |
| proto-plus                  | 1.25.0              | pypi_0            | pypi          |
| protobuf                    | 5.28.3              | pypi_0            | pypi          |
| pyasn1                      | 0.6.1               | pypi_0            | pypi          |
| pyasn1-modules              | 0.4.1               | pypi_0            | pypi          |
| pydantic                    | 2.9.2               | pypi_0            | pypi          |
| pydantic-core               | 2.23.4              | pypi_0            | pypi          |
| pymongo                     | 4.10.1              | pypi_0            | pypi          |
| pyparsing                   | 3.2.0               | pypi_0            | pypi          |
| python                      | 3.9.20              | h8205438_1        | -             |
| requests                    | 2.32.3              | pypi_0            | pypi          |
| rsa                         | 4.9                 | pypi_0            | pypi          |
| setuptools                  | 75.1.0              | py39haa95532_0    | -             |
| sqlite                      | 3.45.3              | h2bbff1b_0        | -             |
| tqdm                        | 4.66.6              | pypi_0            | pypi          |
| typing-extensions           | 4.12.2              | pypi_0            | pypi          |
| tzdata                      | 2024b               | h04d1e81_0        | -             |
| uritemplate                 | 4.1.1               | pypi_0            | pypi          |
| urllib3                     | 2.2.3               | pypi_0            | pypi          |
| vc                          | 14.40               | h2eaa2aa_1        | -             |
| vs2015_runtime              | 14.40.33807         | h98bb1dd_1        | -             |
| werkzeug                    | 3.0.6               | pypi_0            | pypi          |
| wheel                       | 0.44.0              | py39haa95532_0    | -             |
| wtforms                    | 3.2.1               | pypi_0            | pypi          |
| zipp                        | 3.20.2              | pypi_0            | pypi          |


--------------------------------------------------------------------------------------------------------------------------------------------
Step 3:

Api Key required

visit  https://console.cloud.google.com/

creat project

Go to APIs & Services

Enable APIs and Services

search

GOOGLE_PLACES_API_KEY 

CUSTOM_SEARCH_API_KEY

SEARCH_ENGINE_ID

maps googleapis

Enable all these Api

--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Step 4:

Clone project

Open in vs code 

change the python interpreter to the above created one 

run main.py file


