# Run the event management service responsible for sending events to the 
# backend collector.

python ../../code/backend/backend.py \
       --config ../../config/backend.conf \
       --section default \
       --verbose
