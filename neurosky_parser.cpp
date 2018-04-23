/*
	file: get and parse data from neurosky mindwave.
		then log the recieved data in form of payload 
		length and data row. can use decode file to
		convert the row to readable format.
	
	author: satyarth agrahari 
	
	permission: free to edit and distribute code.
*/


/*
	required headers to be imported
*/
#include <stdio.h>
#include <bits/stdc++.h>
#include <fstream>

using namespace std;

#define SYNC	0xAA		// byte used to synchronise the communication
#define EXCODE	0x55		// extended code sync byte. Currently not used in transmission
#define PORT 	"/dev/rfcomm0"	// bluetooth serial port
#define CSV	"csv.txt"	// to log data in csv format
#define JSON	"json.txt"	// to log data in json format
#define PFILE	"log.txt"	// to log the plen and payload data
#define PLOT	"plot.txt"	// to write data for plot purpose

/*
	data fields that are switched on by default
	in the sensor headband. each data is symbolised
	by their specific code. Check the parse method for
	more details.
*/
struct node {
	unsigned char battery_level;
	unsigned char poor_signal;
	unsigned char heart_rate;
	unsigned char attention;
	unsigned char meditation;
	unsigned char eight_bit_raw_wave;
	unsigned char raw_marker;
	
	short raw_wave;
	float EEG_power[8];
	int ASIC_EEG_power[8];
	unsigned short RR_interval;
};

/*
	hack to create a IEEE single
	precision float type using the
	bit representation.
*/
union to_float {
	float f;
	int x;
} num;

/*
	function to parse the payload field and set the 
	signals to the recieved values.
*/
void parse_payload(unsigned char payload[256], unsigned char plen);

/*
	to print the data in a more redable format
*/
void print(struct node data);

/*
	to log data in csv format in the file.
	See implementation for write sequence.
*/
void csv_in_file(struct node data);

/*
	method to write important data in 
	a file. The data will be used for
	plotting the live graph.
*/
void print_in_file(struct node data);

/*
	------------------------------------------------------------ MAIN METHOD ----------------------------------------------------------------------------
*/
int main() 
{
	FILE *stream = NULL;
	
	/*
		method to log data in file: log.txt
		make sure to clear the log.txt file 
		if it exist before running the code.
	*/
	std::ofstream outfile;
	outfile.open("log.txt", std::ios_base::app);

	unsigned char c;
	unsigned char plen = 0;
	unsigned char payload[256];

	int checksum;
	int i;

	/*
		open the serial port to start recieving data
		from the headband.
	*/
	stream = fopen(PORT, "r");

	while (true) {
		/*
			check for first 2 sync bytes.
		*/
		fread(&c, 1, 1, stream);
		if (c != SYNC) continue;
		
		fread(&c, 1, 1, stream);
		if (c != SYNC) continue;

		/*
			find the first non sync byte.
			that should br the length of the
			paayload field
		*/
		while (true) {
			fread(&plen, 1, 1, stream);
			if (plen != SYNC) break;
		}
		/*
			max length of payload cannot exceed 169.
			this shows error in transmission.
		*/
		if (plen > 169) continue;


		/*
			read the payload field and store it in 
			an payload array. This will be used for
			verification of checksum and then parsing 
			the obtained data.
		*/
		fread(payload, 1, plen, stream);

	
		/*
			calculate the checksum. 
			algo: calculate the sum of payload field.
			take the first 8 bits.
			take the ones compliment.
			match with the aquired checksum variable.
		*/
		checksum = 0;
		for (i = 0; i < plen; ++i) checksum += payload[i];
		checksum = (~(checksum & 0xFF)) & 0xFF;

		/*
			verify that the recieved checksum and the 
			calculated checksum matches.
		*/
		fread(&c, 1, 1, stream);
		if (checksum != c) {
			continue;
		}

		/*
			also log the payload data in the file. We only 
			need the payload length and the payload data.
			But it should only be inserted after verifying the checksum.
		*/
		outfile << plen << " ";
		for (i = 0; i < plen; ++i) outfile << payload[i] << " ";
		
		/*
			parse the recieved data and calculate the desired
			field data.
		*/
		if (plen > 4) parse_payload(payload, plen);
	}

	/*
		close the serial stream.
	*/
	fclose(stream);

	return 0;
}

/*
	----------------------------------------------------------  MAIN ENDS ---------------------------------------------------------------------------
*/

/*
	to parse the payload field. Should only be used after 
	the checksum is verified. It sets the local variable data
	of type node to the values recieved.
	payload structure (<EXCODE>)<CODE>(<LEN>)<DATA>. [things in () are optional]
	@param:	1. payload: It the payload data after the verification of checksum
		2. plen: It is the length of the payload field.
*/
void parse_payload(unsigned char payload[256], unsigned char plen) 
{
	unsigned char idx = 0;
	unsigned char code;
	unsigned char len;
	unsigned char extended_code_level;
	unsigned short x_data;

	struct node data;
	int i;
	
	/*
		clear the data field so no 
		anonymous data is left.
	*/
	memset(&data, 0, sizeof(data));

	while (idx < plen) {
		/*
			to calculate the extended code 
			level. This is currently always 0.
		*/
		extended_code_level = 0;
		while (payload[idx] == EXCODE) {
			extended_code_level++;
			idx++;
		}	

		/*
			to get the kind of the data recieved
		*/
		code = payload[idx++];
		
		len = 1;
		/*
			if the code value is greater than 0x7F
			then the length field is present.
		*/	
		if (code > 0x7F) {
			/*
				this will be the length of the data.
			*/
			len = payload[idx++];
		}

		/*
			check the kind of current data. 
			for description, see report header: CODE Definitions Table
			in the code implementation report.
		*/
		switch (code) {
			case 0x01: data.battery_level = payload[idx++]; break;
			case 0x02: data.poor_signal = payload[idx++]; break;
			case 0x03: data.heart_rate = payload[idx++]; break;
			case 0x04: data.attention = payload[idx++]; break;
			case 0x05: data.meditation = payload[idx++]; break;
			case 0x06: data.eight_bit_raw_wave = payload[idx++]; break;
			case 0x07: data.raw_marker = payload[idx++]; break;
			case 0x80: 
				unsigned char a, b;
				a = payload[idx++];
				b = payload[idx++];
				data.raw_wave = (((short) a) << 8) | ((short) b);
				break;
			case 0x81:
				for (i = 0; i < 8; ++i) {
					num.x = 0;
					num.x |= (payload[idx++]); num.x <<= 8;
					num.x |= (payload[idx++]); num.x <<= 8;
					num.x |= (payload[idx++]); num.x <<= 8;
					num.x |= (payload[idx++]);
			
					data.EEG_power[i] = num.f;
				}
				break;
			case 0x83:
				for (i = 0; i < 8; ++i) {
					int x = 0;
					x |= (payload[idx++]); x <<= 8;
					x |= (payload[idx++]); x <<= 8;
					x |= (payload[idx++]);
					data.ASIC_EEG_power[i] = x;
				}
				break;
			case 0x86:
				x_data = 0;
				x_data |= (payload[idx++]); x_data <<= 8;
				x_data |= (payload[idx++]);
				data.RR_interval = x_data;
				break;
			default:
				idx += len;
		}
	}

	print(data);
	csv_in_file(data);
	print_in_file(data);
}

/*
	print data in a more readable format.
	@param:	1. data: struct node type that contains the parsed values.
*/
void print(struct node data) 
{
	printf("\n\n\n");
	printf("battery level = %d\n", data.battery_level);
	printf("poor_signal: %d, heart rate: %d, attention: %d, meditation: %d, 8 bit raw wave: %d, raw marker %d\n", 
		data.poor_signal, data.heart_rate, data.attention, data.meditation, data.eight_bit_raw_wave, data.raw_marker);
	printf("raw_wave: %d, R R interval: %d\n", data.raw_wave, data.RR_interval);
	//printf("EEG Power: ");
	//for (int i = 0; i < 8; ++i) printf("%f ", data.EEG_power[i]);
	printf("ASIC_EEG Power: ");
	for (int i = 0; i < 8; ++i) printf("%d ", data.ASIC_EEG_power[i]);
}

/*
	to log the required data in a csv format.
	the sequence of data will be:
	attention, meditation, ASIC EEG power[0 to 7], RR interval <endl>
	@param: 1. data: the variable containing all the data
*/
void csv_in_file(struct node data)
{
	/*
		open the file stream in append mode
	*/
	std::ofstream csvfile;
	csvfile.open(CSV, std::ios_base::app);
	
	/*
		log the data in the file
	*/
	csvfile << (int)data.attention << ", " << (int)data.meditation << ", ";
	for (int i = 0; i < 7; ++i) csvfile << data.ASIC_EEG_power[i] << ", ";
	csvfile << data.ASIC_EEG_power[7] << endl;
}

/*
	method to write important data in 
	a file. The data will be used for
	plotting the live graph.
*/
void print_in_file(struct node data) 
{
	/*
		open the file stream in write mode
	*/
	std::ofstream plotfile;
	plotfile.open(PLOT, std::ios_base::out);

	/*
		log data for plot in file
	*/
	plotfile << (int)data.attention << ", " << (int)data.meditation << ", ";
	for (int i = 0; i < 7; ++i) plotfile << data.ASIC_EEG_power[i] << ", ";
	plotfile << data.ASIC_EEG_power[7] << endl;
}
