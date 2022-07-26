FROM python:3.9-slim

COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r ./requirements.txt

#RUN groupadd -g 999 pizzaseol
#RUN useradd -r -u 999 -g pizzaseol pizzaseol
#
#USER pizzaseol