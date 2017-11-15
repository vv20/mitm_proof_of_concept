java -jar mmt.jar --file mitm_server.msl &
inst/gap-master/bin/gap.sh gap_server.g &
python3.5 singular_server.py &
sleep 5
python3.5 ControllingClient.py
jupyter notebook --no-browser --ip=0.0.0.0
