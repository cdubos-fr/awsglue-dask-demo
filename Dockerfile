FROM daskdev/dask:2022.10.2-py3.10

ENV WORKDIR /srv/app

WORKDIR ${WORKDIR}

COPY workflow workflow
COPY demo-models demo-models
COPY tox.ini .

RUN pip3 install tox
RUN tox -e prodenv

ENV VIRTUAL_ENV=${WORKDIR}/.venv
ENV PATH="${VIRTUAL_ENV}/bin:${PATH}"

ENTRYPOINT [ "python", "workflow/main.py" ]
