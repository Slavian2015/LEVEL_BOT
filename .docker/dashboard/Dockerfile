FROM python:3.8

RUN mkdir -p /usr/local/WB
RUN pip install --upgrade pip
RUN apt-get update && apt-get install -y --no-install-recommends


RUN pip install pymongo
RUN pip install python-binance
RUN pip install pandas-datareader
RUN pip install apscheduler
RUN pip install pytz
RUN pip install dateparser
RUN pip install statsmodels
RUN pip install unicorn-binance-websocket-api
RUN pip install ipywidgets
RUN wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz && \
  tar -xvzf ta-lib-0.4.0-src.tar.gz && \
  cd ta-lib/ && \
  ./configure --prefix=/usr && \
  make && \
  make install
RUN rm -R ta-lib ta-lib-0.4.0-src.tar.gz
RUN pip install TA-Lib
RUN pip install cython
RUN pip install zigzag
RUN pip install pika
RUN pip install rabbitmq-client
RUN pip install Flask

COPY docker-entrypoint.sh /usr/local/bin/
RUN ln -s /usr/local/bin/docker-entrypoint.sh /entrypoint.sh # backwards compat
RUN chmod +x /usr/local/bin/docker-entrypoint.sh
RUN pip install psycopg2
RUN pip install gunicorn
RUN pip install scipy
RUN pip install trendln
RUN pip install PeakUtils
RUN pip install dash
RUN pip install dash-bootstrap-components
RUN pip install dash-core-components
RUN pip install dash-html-components

ENTRYPOINT ["docker-entrypoint.sh"]