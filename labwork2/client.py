import xmlrpc.client
from pathlib import Path
from xmlrpc.client import Binary 

proxy = xmlrpc.client.ServerProxy("http://localhost:9000/")

with open(Path(__file__).parent/'meme.jpg','rb') as handle:
    binary_data = xmlrpc.client.Binary(handle.read())
    proxy.server_receive_file(binary_data)