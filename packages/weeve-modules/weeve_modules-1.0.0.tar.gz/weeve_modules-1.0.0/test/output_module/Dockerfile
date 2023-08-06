FROM python:3.8-slim

COPY test/output_module/output_module.py /app/

# copy and install weeve_modules package
COPY src pyproject.toml README.md /app/weeve-modules-python-package/
RUN pip install /app/weeve-modules-python-package

CMD [ "python", "/app/output_module.py"]