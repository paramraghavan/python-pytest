FROM ubuntu:18.04

RUN apt-get update && \
    apt-get install -y default-jdk scala wget vim software-properties-common python3.8 python3-pip curl unzip libpq-dev build-essential libssl-dev libffi-dev python3-dev&& \
    apt-get clean

RUN wget https://archive.apache.org/dist/spark/spark-3.0.1/spark-3.0.1-bin-hadoop3.2.tgz && \
    tar xvf spark-3.0.1-bin-hadoop3.2.tgz && \
    mv spark-3.0.1-bin-hadoop3.2/ /usr/local/spark && \
    ln -s /usr/local/spark spark

WORKDIR app
RUN mkdir -p /app/src
COPY src/bigdata /app/bigdata
COPY src/unit_test_pyspark/requirements_docker.txt /app/requirements.txt
RUN mkdir -p /app/tests
COPY src/unit_test_pyspark/conftest_docker.py /app/tests/conftest.py
COPY src/unit_test_pyspark/tests/* /app/tests
# Following fixed error --> ModuleNotFoundError: No module named 'setuptools_rust'
RUN pip3 install --upgrade pip
RUN pip3 install cython==0.29.21 numpy==1.18.5 &&  pip3 install pytest pyspark pandas==1.0.5 && pip3 install -r requirements.txt
#RUN pip3 install cython==0.29.21 numpy==1.18.5 && pip3 install pytest pyspark pandas==1.0.5
ENV PYSPARK_PYTHON=python3
#ENTRYPOINT python3 -m pytest --no-header -v
#ENTRYPOINT python3 -m pytest -v

# docker build -t spark-test -f src/unit_test_pyspark/Dockerfile .
# docker run -it  spark-test --> t, the docker image tag and i, for interactive session