from xmlrpc.server import SimpleXMLRPCServer
import os 

server = SimpleXMLRPCServer(('localhost',9000))

def server_receive_file(arg):
    with open('transfered.jpg', 'wb') as handle: 
        handle.write(arg.data)
        return True

print("Server listening at port 9000")

server.register_function(server_receive_file,'server_receive_file')
server.serve_forever()