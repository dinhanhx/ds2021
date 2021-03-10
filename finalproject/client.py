import mpi4py.MPI as MPI
import sys

if __name__ == '__main__':
    portname = sys.argv[1]
    print(portname)

    server = MPI.COMM_WORLD.Connect(portname, MPI.INFO_NULL, 0)
    MPI.COMM_WORLD.Send("Hello from the client", server, 2)
    bundle = MPI.COMM_WORLD.Recv(2048, MPI.ANY_SOURCE, 3)

    if MPI.COMM_WORLD.Get_rank() == 0:
        print(bundle)

