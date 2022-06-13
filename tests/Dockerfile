
FROM python:3.9
COPY /functional/requirements.txt .
RUN pip install -r requirements.txt
COPY ./functional /functional/
ENTRYPOINT sh -c "/functional/utils/entrypoint.sh && pytest /functional/src"