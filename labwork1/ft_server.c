#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <arpa/inet.h>
#define SIZE 2048

void write_file(int sockfd)
{
    int n;
    FILE *fp;
    char *filename = "recv_guid_lists.txt";
    char buffer[SIZE];

    fp = fopen(filename, "w");
    while (1) 
    {
        n = recv(sockfd, buffer, SIZE, 0);
        if (n <= 0)
        {
            break;
            return; // End the function before writing null to the file
        }
        fprintf(fp, "%s", buffer);
        bzero(buffer, SIZE);
    }
}

int main()
{
    char *ip = "127.0.0.1";
    int port = 8080;
    
    // Create server socket
    int sockfd = socket(AF_INET, SOCK_STREAM, 0);
    if(sockfd < 0) 
    {
        perror("Error in socket");
        exit(1);
    }
    printf("Server socket created successfully.\n");

    // Add server info
    struct sockaddr_in server_addr;
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = port;
    server_addr.sin_addr.s_addr = inet_addr(ip);

    // Bind server port
    int e = bind(sockfd, (struct sockaddr*)&server_addr, sizeof(server_addr));
    if(e < 0) 
    {
        perror("Error in bind");
        exit(1);
    }
    printf("Binding successfull.\n");

    // Listen for the client
    if(listen(sockfd, 10) == 0)
    {
        printf("Listening....\n");
    }
    else
    {
        perror("Error in listening");
        exit(1);
    }

    // Accept the client
    struct sockaddr_in new_addr;
    socklen_t addr_size;
    addr_size = sizeof(new_addr);
    int new_sock = accept(sockfd, (struct sockaddr*)&new_addr, &addr_size);

    // Recieve file from the client
    write_file(new_sock);
    printf("Data written in the file successfully.\n");

    return 0;
}