FROM ubuntu

RUN apt update && apt upgrade -y
RUN apt install python3 -y
RUN apt install python3-pip -y
RUN apt install fonts-roboto -y

WORKDIR /usr/src/ceo_pp_bot

COPY main.py /usr/src/ceo_pp_bot
COPY src/ /usr/src/ceo_pp_bot/src
COPY requirements.txt /usr/src/ceo_pp_bot
COPY config.yaml /usr/src/ceo_pp_bot
COPY README.md /usr/src/ceo_pp_bot

RUN ["pip3", "install", "-r", "requirements.txt"]

CMD ["python3", "main.py"]
