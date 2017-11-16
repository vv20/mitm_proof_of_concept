shopt -s expand_aliases
source ~/.bash_aliases

echo "starting the MMT server..."
mmt --file mitm_server.msl &
echo "starting the gap server..."
gap gap_server.g &
echo "starting the singular server..."
python3 singular_server.py &
echo "waiting for the server to initialise..."
sleep 5
echo "running the control client..."
python3 ControllingClient.py 
echo "done"
