/*The client program has the following major steps:
	1) Create a socket
	2) Connect the socket to the address of the server
	3) Send and recieve datapes.h
*/
#include<stdio.h>
#include<stdlib.h>
#include<strings.h>
#include<sys/types.h>
#include<sys/socket.h>
#include<netinet/in.h>
#include<netdb.h>
#include<unistd.h>
#include<string.h>
int count=0;
char *name="im0.jpg";
int receive_image(int socket)
{ // Start function 

int buffersize = 0, recv_size = 0,size = 0, read_size, write_size, packet_index =1,stat;

char imagearray[10241],verify = '1';
FILE *image;

//Find the size of the image
do{
stat = read(socket, &size, sizeof(int));
}while(stat<0);

printf("Packet received.\n");
printf("Packet size: %i\n",stat);
printf("Image size: %i\n",size);
printf(" \n");

char buffer[] = "Got it";

//Send our verification signal
do{
stat = write(socket, &buffer, sizeof(int));
}while(stat<0);

printf("Reply sent\n");
printf(" \n");

image = fopen(name, "w");

if( image == NULL) {
printf("Error has occurred. Image file could not be opened\n");
return -1; }

//Loop while we have not received the entire file yet


int need_exit = 0;
struct timeval timeout = {1000,0};

fd_set fds;
int buffer_fd, buffer_out;

while(recv_size < size) {
//while(packet_index < 2){

    FD_ZERO(&fds);
    FD_SET(socket,&fds);

    buffer_fd = select(FD_SETSIZE,&fds,NULL,NULL,&timeout);

    if (buffer_fd < 0)
       printf("error: bad file descriptor set.\n");

    if (buffer_fd == 0)
       printf("error: buffer read timeout expired.\n");

    if (buffer_fd > 0)
    {
        do{
               read_size = read(socket,imagearray, 10241);
            }while(read_size <0);

            printf("Packet number received: %i\n",packet_index);
        printf("Packet size: %i\n",read_size);


        //Write the currently read data into our image file
         write_size = fwrite(imagearray,1,read_size, image);
         printf("Written image size: %i\n",write_size); 

             if(read_size !=write_size) {
                 printf("error in read write\n");    }


             //Increment the total number of bytes read
             recv_size += read_size;
             packet_index++;
             printf("Total received image size: %i\n",recv_size);
             printf(" \n");
             printf(" \n");
    }

}


  fclose(image);
  printf("Image successfully Received!\n");
  return 1;
  }

void error(char *msg)
{
	printf("%s",msg);
	exit(1);
}

int main(int argc, char **argv)
{
	while(1)
	{
		int sockfd,portno,in;
		struct sockaddr_in serv_addr;
		struct hostent *server;
		char buffer[256];
		if( argc< 3)
		{
			error("Invalid command line arguments.\n");
		}
		portno = atoi(argv[2]);
		sockfd=socket(AF_INET,SOCK_STREAM,0);
		if(sockfd<0)
		{
			error("Couldn't create socket.\n");
		}
		server = gethostbyname(argv[1]);
		if(server==NULL)
		{
			error("Could not find the server.\n");
		}
		bzero((char *)&serv_addr,sizeof(serv_addr));
		serv_addr.sin_family=AF_INET;
		bcopy((char *)server->h_addr,(char*)&serv_addr.sin_addr.s_addr,server->h_length);//copying values of server address
		serv_addr.sin_port = htons(portno);
		if(connect(sockfd,(struct sockaddr *)&serv_addr,sizeof(serv_addr))<0)
		{
			error("Could not connect to server.\n");
		}
		receive_image(sockfd);
		count++;
		name=malloc(sizeof(char)*13);
		snprintf(name,9,"im%d.jpg",count);
		printf("\n\nGetting New Image\n\n");
		sleep(4);
	}
	return 0;
}	
