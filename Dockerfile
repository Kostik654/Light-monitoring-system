FROM python:3.9

USER 0

ARG pname="monitor"

ENV TZ=Europe/Moscow

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN mkdir $pname

WORKDIR $pname

COPY ./backend_engine/* ./

EXPOSE 65400

RUN apt-get update

RUN apt-get install -y iputils-ping net-tools

RUN pip install --no-cache-dir --upgrade pip -r requirements.txt

CMD [ "python","-u","main.py" ]
