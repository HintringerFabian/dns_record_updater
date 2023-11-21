FROM python:3.12-slim-bookworm
LABEL   author="HintringerFabian" \
        maintainer="HintringerFabian" \
        github_repo="https://github.com/HintringerFabian/dns_record_updater"

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt && rm -rf requirements.txt

CMD ["python", "main.py"]