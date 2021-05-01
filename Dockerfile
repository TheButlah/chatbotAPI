FROM tensorflow/tensorflow:1.15.5-gpu

RUN apt-get update \
    && apt-get install -y python3-venv \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir /opt/chatbot

WORKDIR /opt/chatbot

# Equivalent to creating and sourcing a venv
ENV VIRTUAL_ENV=/opt/chatbot/.venv
RUN python3 -m venv --system-site-packages $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY ./requirements.txt /opt/chatbot

RUN pip install -r requirements.txt

COPY . /opt/chatbot

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0"]
