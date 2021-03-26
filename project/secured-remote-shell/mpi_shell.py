import mpi4py.MPI as MPI
import subprocess
import json
import os

from security import import_key, encode_encrypt, decrypt_decode

def mpi_shell():
    """Setup a connection between two proccesses/two cores/two nodes/two clusters"""
    
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()

    if rank == 0:
        # client-like side

        # setup keys
        client_private_key = 'rank0/private.key.txt'
        server_public_key = 'rank1/public.key.txt'
        client_private_key, server_public_key = import_key(client_private_key, server_public_key)

        # enter client-server-like loop
        while True:
            cwd = decrypt_decode(comm.recv(source=1, tag=42), client_private_key)

            cmd = input(f'{cwd}#>')

            comm.send(encode_encrypt(cmd, server_public_key), dest=1, tag=42)

            output = decrypt_decode(comm.recv(source=1, tag=42), client_private_key)
            print(output)
        # end of client-like side
    elif rank == 1:
        # server-like side

        # setup keys
        server_private_key = 'rank1/private.key.txt'
        client_public_key = 'rank0/public.key.txt'
        server_private_key, client_public_key = import_key(server_private_key, client_public_key)
        
        # enter server-client-like loop
        while True:
            cwd = os.getcwd()
            comm.send(encode_encrypt(cwd, client_public_key), dest=0, tag=42)

            cmd = decrypt_decode(comm.recv(source=0, tag=42), server_private_key)

            output = subprocess.getoutput(cmd)
            comm.send(encode_encrypt(output, client_public_key), dest=0, tag=42)
        # end of server-like side


if __name__ == '__main__':
    mpi_shell()
    