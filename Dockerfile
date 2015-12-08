FROM eliostvs/tomate-gtk

COPY ./ /code/

RUN apt-get update -qq && \
    gir1.2-notify-0.7 \
    notify-osd

RUN apt-get clean

WORKDIR /code/

ENTRYPOINT ["make"]

CMD ["test"]