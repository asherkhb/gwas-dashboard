# docker build --rm -t plotlydash:3 .
# docker run --rm -it -v "$PWD":/usr/src/app -p 8050:8050 plotlydash:3 <optional script-name.py>
# Make sure app is set to run on host 0.0.0.0 (app.run_server(debug=True, host='0.0.0.0'))

# Initialize Container
FROM python:3
WORKDIR /usr/src/app
COPY requirements.txt .

# Install DASH
RUN pip install \
    dash==0.18.3 \
    dash-renderer==0.11.0 \
    dash-html-components==0.8.0 \
    dash-core-components==0.12.7 \
    plotly --upgrade

# Install Common Python Libraries

# Install User Requirements
RUN pip install --no-cache-dir -r requirements.txt

# Set Entrypoint & Default App
ENTRYPOINT ["python"]
CMD ["app.py"]
