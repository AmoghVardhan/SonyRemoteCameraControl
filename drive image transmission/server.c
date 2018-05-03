#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<sys/socket.h>
#include<arpa/inet.h>
#include<unistd.h>
#include<errno.h>
char *name="IMG_0001.jpg";
char *gps="gps1.txt";
int count=1;
int send_image(int socket)
{
	FILE *picture;
	int size, read_size, stat, packet_index;
	char send_buffer[10240], read_buffer[256];
	packet_index = 1;
	picture = fopen(name, "r");
   	printf("Getting Picture Size\n");
	if(picture == NULL)
	{
        	printf("Error Opening Image File");
	}
   	//printf("aaa\n");
   	fseek(picture, 0, SEEK_END);
   	size = ftell(picture);
   	fseek(picture, 0, SEEK_SET);
  	printf("Total Picture size: %i\n",size);
	//Send Picture Size
   	printf("Sending Picture Size\n");
   	write(socket, (void *)&size, sizeof(int));
	//Send Picture as Byte Array
   	printf("Sending Picture as Byte Array\n");
	do
	{
		//Read while we get errors that are due to signals.
      		stat=read(socket, &read_buffer , 255);
      		printf("Bytes read: %i\n",stat);
   	} while (stat < 0);
	printf("Received data in socket\n");
   	printf("Socket data: %s\n", read_buffer);
	while(!feof(picture))
	{
   		//while(packet_index = 1){
      		//Read from the file into our send buffer
      		read_size = fread(send_buffer, 1, sizeof(send_buffer)-1, picture);
		//Send data through our socket
	      	do
		{
       			 stat = write(socket, send_buffer, read_size);
      		}while (stat < 0);
		printf("Packet Number: %i\n",packet_index);
     	 	printf("Packet Size Sent: %i\n",read_size);
      		printf(" \n");
      		printf(" \n");
      		packet_index++;
		//Zero out our send buffer
      		bzero(send_buffer, sizeof(send_buffer));
     	}
}
int main(int argc , char *argv[])
{
	while(1)
	{
		printf("\n\nSending image %s\n\n",name);
	        /*char cm[45];
		cm[0]='.';
		cm[1]='/';
		cm[2]='c';
		cm[3]='h';
		cm[4]='d';
		cm[5]='k';
		cm[6]='p';
		cm[7]='t';
		cm[8]='p';
		cm[9]=' ';
		cm[10]='-';
		cm[11]='e';
		cm[12]='"';
		cm[13]='c';
		cm[14]='o';
		cm[15]='n';
		cm[16]='n';
		cm[17]='e';
		cm[18]='c';
		cm[19]='t';
		cm[20]='"';
		cm[21]=' ';
		cm[22]='-';
		cm[23]='e';
		cm[24]='"';
		cm[25]='r';
		cm[26]='e';
		cm[27]='c';
		cm[28]='"';
		cm[29]=' ';
		cm[30]='-';
		cm[31]='e';
		cm[32]='"';
		cm[33]='r';
		cm[34]='e';
		cm[35]='m';
		cm[36]='o';
		cm[37]='t';
		cm[38]='e';
		cm[39]='s';
		cm[40]='h';
		cm[41]='o';
		cm[42]='o';
		cm[43]='t';
		cm[44]='"';
		cm[45]='\0';
		system(cm);*/
		int portno;
		portno=atoi(argv[1]);
		system("ls");
		int socket_desc , new_socket , c, read_size,buffer = 0;
      		struct sockaddr_in server , client;
      		char *reading;
      		//Create socket
     		socket_desc = socket(AF_INET , SOCK_STREAM , 0);
      		if (socket_desc == -1)
      		{
        	 	printf("Could not create socket");
      		}
      		//Prepare the sockaddr_in structure
      		server.sin_family = AF_INET;
      		server.sin_addr.s_addr = INADDR_ANY;
      		server.sin_port = htons( portno );
        	int r=1;
      		if(setsockopt(socket_desc,SOL_SOCKET,SO_REUSEADDR,(char*)&r,sizeof(r))<0)
        	{
        	        printf("Unable to make socket reusable.\n");
        	        exit(0);
        	}
     	 	//Bind
     		if( bind(socket_desc,(struct sockaddr *)&server , sizeof(server)) < 0)
     		{
       			puts("bind failed");
       			return 1;
     		}
		puts("bind done");
		//Listen
     		listen(socket_desc , 3);
      		//Accept and incoming connection
      		puts("Waiting for incoming connections...");
      		c = sizeof(struct sockaddr_in);
     		if((new_socket = accept(socket_desc, (struct sockaddr *)&client,(socklen_t*)&c)))
		{
			puts("Connection accepted");
        	}
		fflush(stdout);
		if (new_socket<0)
    		{
      			perror("Accept Failed");
      			return 1;
    		}
		send_image(new_socket);
		//send_gps(new_socket);
    		close(socket_desc);
    		fflush(stdout);
		count++;
		name=malloc(sizeof(char)*13);
		if(count<=9)
		{
			snprintf(name,13,"IMG_000%d.jpg",count);
			//printf("IMAGE NAME:%s\n",name);
		}
		if(count>=10 && count<=99)
			snprintf(name,13,"IMG_00%d.jpg",count);
		if(count>=100)
			snprintf(name,13,"IMG_0%d.jpg",count);
	}
    	return 0;
}
