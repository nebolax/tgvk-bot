FROM python

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY environment_setup.sh .

RUN bash environment_setup.sh

COPY . .


CMD ["python3", "main.py"]