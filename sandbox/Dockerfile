FROM codebox

RUN mkdir /.codebot
COPY ./handler.py /.codebot/handler.py
WORKDIR /home
ENTRYPOINT python3 /.codebot/handler.py
