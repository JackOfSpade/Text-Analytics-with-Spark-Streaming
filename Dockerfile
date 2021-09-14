FROM eecsyorku/eecs4415

# Output to terminal in real-time
ENV PYTHONUNBUFFERED 1

# Enable path conversion from Windows-style to Unix-style in volume definitions
ENV COMPOSE_CONVERT_WINDOWS_PATHS=1

RUN mkdir /my_project

WORKDIR /my_project

COPY . /my_project

RUN apt-get -qq update && apt-get -qq install gcc && apt-get -qq install python-dev python3-dev && pip install -r requirements.txt

