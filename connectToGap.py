from scscp import SCSCPCLI as cli
from openmath import openmath as om

client = cli("localhost")
client.heads
print(client.heads.scscp_transient_1.Factorial([om.OMInteger(5)]))
client.quit()
