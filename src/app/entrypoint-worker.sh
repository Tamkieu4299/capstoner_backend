#!/bin/bash

# cd /usr/src/app/settings
# /bin/bash merge.sh $ENVIRONMENT.py
# cd /usr/src/app
# cd /usr/src/app/spark_worker/config
# /bin/bash merge.sh $ENVIRONMENT.py
# cd /usr/src/app
# cp /usr/src/app/spark_worker/microlibs/valuation/settings/$ENVIRONMENT.py /usr/src/app/spark_worker/microlibs/valuation/settings.py
# cp /usr/src/app/spark/config/$ENVIRONMENT.py /usr/src/app/spark/config/settings.py
# cp /usr/src/app/microlibs/valuation/settings/$ENVIRONMENT.py /usr/src/app/microlibs/valuation/settings.py
# sleep 3
cd /app/spark_worker
python spark_worker.py
