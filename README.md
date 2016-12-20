# YelpExercise

A short data science exercise on the [Yelp Academic Dataset](https://www.yelp.com/dataset_challenge/dataset)
using [pandas](http://pandas.pydata.org/) and [scikit-learn](http://scikit-learn.org/).

This project consists of 2 parts:
+ ProcessTarFile.py: A script, parsing the tarred Yelp dataset, and exporting the data to 5 tabular CSV files.
+ YelpAnalysis.ipynb: A Jupyter notebook, reading the CSV files, performing some exploratory data analysis on joined tables of the input dataset (using pandas), and testing some predictive analysis (using scikit-learn).

### Usage
The Notebook code including the rendered output can be viewed directly on GitHub: [YelpAnalysis.ipynb](YelpAnalysis.ipynb)

The code can be executed in containerized form. Assuming a working [docker](https://www.docker.com/) installation, proceed as follows:
+ Clone or download a copy of this code repository.
+ Change into the project directory:
```
cd yelp-exercise
```
+ Build the docker container specified by the provided Dockerfile:
```
docker build -t mkleesiek:yelp .
```
+ Run the docker container with the following options:
You need to replace [JUPYTER_PORT] with the port number that the container's jupyter notebook server should publish to your host (8888 by default).
[YELP_DOWNLOAD_DIR] is to be replaced with the location of the Yelp dataset tar file.
```
docker run --rm -it -p [JUPYTER_PORT]:8888 -v [YELP_DOWNLOAD_DIR]/yelp_dataset_challenge_academic_dataset.tar:/yelp.tar mkleesiek:yelp
```
The above command will start the container, executing ProcessTarFile.py on the mounted dataset tar and starting the jupyter notebook subsequently.

If you prefer to perform these 2 steps manually, start the container with:
```
docker run --rm -it -p [JUPYTER_PORT]:8888 -v [YELP_DOWNLOAD_DIR]/yelp_dataset_challenge_academic_dataset.tar:/yelp.tar mkleesiek:yelp /bin/bash
```
Then execute
```
python3 ProcessTarFile.py /yelp.tar
start-notebook.sh
```
