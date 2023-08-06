FROM python:3.8-slim

COPY test/input_module/requirements.txt test/input_module/input_module.py /app/
RUN pip install -r /app/requirements.txt

# copy and install weeve_modules package
COPY src pyproject.toml README.md /app/weeve-modules-python-package/
RUN pip install /app/weeve-modules-python-package

CMD [ "python", "/app/input_module.py"]