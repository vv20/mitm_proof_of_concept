from scscp import SCSCPCLI as cli

client = cli("localhost")
print(client.heads)
print(client.heads.scscp_transient_1.addition([2,2]))
client.quit()

