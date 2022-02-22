# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.8-slim-buster

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1
EXPOSE 8501

# Install pip requirements
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

COPY . /app
# ADD . /app

RUN useradd appuser && chown -R appuser /app
RUN mkdir /home/appuser && chown -R appuser:appuser /home/appuser
RUN chown -R appuser:appuser /app
USER appuser

###########START NEW IMAGE : DEBUGGER ###################
# FROM base as debug
RUN pip install ptvsd
EXPOSE 5678

###########START NEW IMAGE : JUPYTER ###################
RUN pip install notebook jupyterlab
EXPOSE 8888

WORKDIR /app


# CMD python -m ptvsd --host 0.0.0.0 --port 5678 --wait --multiprocess -m run src/dash/app.py
# CMD python src/dash/app.py
# CMD /bin/bash
# CMD jupyter notebook --port=8888 --no-browser --ip=0.0.0.0 --allow-root


###########START NEW IMAGE: PRODUCTION ###################
# FROM base as prod

# WORKDIR /app

# CMD ["streamlit", "run", "app.py"]

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
# CMD ["streamlit", "hello"]
# ENTRYPOINT [ "python -m http.server 8501"]
# CMD ["streamlit", "run", "app.py", '--server.port=8501', '--server.enableCORS=false']