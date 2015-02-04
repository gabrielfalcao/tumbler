FROM debian:stable
MAINTAINER <Gabriel Falcão gabriel@nacaolivre.org>

RUN apt-get update
RUN apt-get install -y python-setuptools openssh-client git
RUN easy_install pip
RUN pip install -U tumbler
RUN git clone https://github.com/gabrielfalcao/tumbler.git /tumbler
WORKDIR /tumbler

# Expose
EXPOSE  5000

# Run
CMD ["tumbler", "run", "--port", "5000", "example/routes.py"]
