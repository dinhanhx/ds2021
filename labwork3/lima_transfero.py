# (^._.^)ﾉ Author: Vu Dinh Anh
# lima transfero = file transfer

import mpi4py.MPI as MPI

if __name__ == '__main__':
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()

    if rank == 0:
        filepath = 'init/secured_document.txt'
        with open(filepath, 'rb') as file:
            data = file.read()
            comm.send(data, dest=1, tag=42)
    elif rank == 1:
        data = comm.recv(source=0, tag=42)
        filepath = 'dest/secured_document.txt'
        with open(filepath, 'wb') as file:
            file.write(data)