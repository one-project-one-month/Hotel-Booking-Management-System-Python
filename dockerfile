FROM python:3.10

COPY ./src/api/requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

COPY ./src/api/agent_api.py ./agent_api.py
COPY . .

EXPOSE 80

CMD ["uvicorn", "agent_api:app", "--host", "0.0.0.0", "--port", "80"]
