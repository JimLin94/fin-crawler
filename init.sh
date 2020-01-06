#!/bin/bash
# if python --version

virtualenv -p python3 ./fin-crawler
source ./fin-crawler/bin/activate

# if virtualenv ; then
#     virtualenv -p python3 ./fin-crawler
# else
#     echo 'No virtualenv detected!'
# fi
