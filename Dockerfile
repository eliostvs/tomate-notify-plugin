FROM eliostvs/tomate-gtk

ENV PROJECT /code/

COPY ./ $PROJECT

RUN apt-get update -qq && apt-get -yqq install gir1.2-notify-0.7 notify-osd

WORKDIR $PROJECT

ENTRYPOINT ["make"]

CMD ["test"]