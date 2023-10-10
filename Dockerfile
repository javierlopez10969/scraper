FROM python:3.9
COPY ./requirements.txt /code/requirements.txt
RUN python3 -m venv /opt/venv
RUN /opt/venv/bin/pip install --no-cache-dir --upgrade pip
RUN /opt/venv/bin/pip install --no-cache-dir --upgrade -r /code/requirements.txt

RUN apt update
RUN apt-get install ffmpeg -y
RUN ffmpeg -version

# Copy app into container
COPY . .
COPY ./app /code/app

WORKDIR /code

RUN mkdir pw-browsers

#RUN PLAYWRIGHT_BROWSERS_PATH=pw-browsers /opt/venv/bin/playwright install --with-deps firefox
RUN PLAYWRIGHT_BROWSERS_PATH=pw-browsers /opt/venv/bin/playwright install --with-deps webkit

COPY . .

CMD ["/opt/venv/bin/python", "-m", "awslambdaric", "app.main.handler"]