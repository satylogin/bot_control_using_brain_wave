/*
	CODE: read data from command.txt as evaluated from decision.py

	Author: Satyarth Agrahari

	License: free to edit and distribute
*/

#include <stdio.h>
#include <bits/stdc++.h>
#include <fstream>
#include <unistd.h>
#include <fcntl.h>
#include <termios.h>
#include <errno.h>

using namespace std;

int main() 
{
	/*
		connect to the bluetooth serial stream to
		write data to arduino
	*/
	int stream = open("/dev/rfcomm2", O_RDWR | O_NOCTTY | O_NONBLOCK);
	cout << stream << endl;

	/*
		open the file which contains the command
		evaluated by decision.py 
	*/	
	std::ofstream get_command;
	get_command.open("command.txt", std::ios_base::in);

	/*
		make a finite but large loop to make sure that
		loop finished and stream gets closed
	*/
	int n = 2000000;
	while (n-- > 0) {
		char s[2];
		get_command >> s;
		write(stream, s, (ssize_t)2);
	}

	/*
		close the stream
	*/
	close(stream);

	return 0;
}
