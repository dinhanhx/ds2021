import mpi4py.MPI as MPI

if __name__ == '__main__':
    portname = MPI.Open_port(MPI.INFO_NULL)

    if MPI.COMM_WORLD.Get_rank() == 0:
        print(f'Portname {portname}')

    client = MPI.COMM_WORLD.Accept(portname, MPI.INFO_NULL)
    bundle = MPI.COMM_WORLD.Recv(2048, MPI.ANY_SOURCE, 2)

    if MPI.COMM_WORLD.Get_rank() == 0:
        print(bundle)

    MPI.COMM_WORLD.Send("Hello from server", client, 3)

