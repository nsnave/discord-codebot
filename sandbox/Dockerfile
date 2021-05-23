FROM codebox

RUN mkdir /.codebot
COPY ./handler.py /.codebot/handler.py
WORKDIR /home
# ENTRYPOINT ["/handler"]
ENTRYPOINT python3 /.codebot/handler.py
