FROM tensorflow/tensorflow:1.15.5-gpu

RUN apt-get update \
    && apt-get install -y python3-venv \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir /opt/chatbot

WORKDIR /opt/chatbot

# Allows us to use the CUDA JIT compiler cache, size is 2 GiB
ENV CUDA_CACHE_MAXSIZE="2147483648"
VOLUME [ "/root/.nv/ComputeCache" ]

# Equivalent to creating and sourcing a venv
ENV VIRTUAL_ENV=/opt/chatbot/.venv
RUN python3 -m venv --system-site-packages $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY ./requirements.txt /opt/chatbot

RUN pip install -r requirements.txt

# Download the initial model
RUN python -c 'import gpt_2_simple as gpt2; gpt2.download_gpt2(model_name="355M")'

COPY . /opt/chatbot

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0", "--port=80", "--no-reload"]
