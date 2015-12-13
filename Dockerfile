FROM eliostvs/tomate

ENV PROJECT /code/

COPY ./ $PROJECT

RUN apt-get update -qq && apt-get -yqq install gir1.2-notify-0.7 gir1.2-gtk-3.0 notify-osd

WORKDIR $PROJECT

ENTRYPOINT ["make"]

CMD ["test"]