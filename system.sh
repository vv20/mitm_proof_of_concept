shopt -s expand_aliases
source ~/.bash_aliases

echo "starting the gap server..."
gap gap_server.g > gap.log &
echo "starting the singular server..."
python3 singular_server.py > singular.log &
echo "waiting for the server to initialise..."
sleep 5
echo "running the control client..."
python3 ControllingClient.py > control_script.log
echo "done"
