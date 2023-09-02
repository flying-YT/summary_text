FROM python:3.11.5-bullseye

WORKDIR /app

COPY requirements.txt .
RUN pip install -q --upgrade pip

RUN echo "deb http://archive.debian.org/debian/ stretch main" > /etc/apt/sources.list
RUN echo "deb http://archive.debian.org/debian-security stretch/updates main" >> /etc/apt/sources.list

RUN apt-get autoclean
RUN apt-get clean all
RUN apt-get update
RUN dpkg --configure -a
RUN apt-get -f install

RUN apt-get install git

RUN git clone https://github.com/huggingface/transformers -b v4.4.2

RUN pip install --upgrade pip

RUN pip install -q transformers
RUN pip install -q fugashi[unidic-lite]
RUN pip install -q ipadic
RUN pip install -q pydantic==1.10.0a1

RUN pip install -q datasets==1.2.1
RUN pip install -q rouge_score==0.0.4
RUN pip install -q sentencepiece
RUN pip install -q dill==0.3.3

RUN pip install -q git+https://github.com/boudinfl/pke.git
RUN pip install -q nltk
RUN pip install -q -U spacy


# Update default packages
RUN apt-get update

# Get Ubuntu packages
RUN apt-get install -y \
    build-essential \
    curl

# Update new packages
RUN apt-get update

# Get Rust
RUN curl https://sh.rustup.rs -sSf | bash -s -- -y

ENV PATH="/root/.cargo/bin:${PATH}"


RUN pip install -q -U ginza ja_ginza_electra
RUN pip install -q spacy==3.4.4
RUN pip install -q protobuf==3.20.1

RUN pip install -q --no-cache-dir --upgrade -r /app/requirements.txt

RUN pip uninstall -y -q pydantic
RUN pip install -q pydantic==1.10.0a1
RUN pip uninstall -y -q thinc
RUN pip install -q thinc==8.1.12

RUN apt-get install -y iputils-ping net-tools dnsutils

COPY ./app/ .
COPY ./output/ .

#RUN python t5_base_japanese.py
#RUN python ginza-510.py

CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8080"]
