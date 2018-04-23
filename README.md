## Controling a Vehicular Robot using EEG Brain Waves

We are going to use an EEG sensor to control a bot using neurosky mindwave headband.

The code is tested on Ubuntu 64bit system.

### Follow the following process to use the code:

* **Install Blueman In Ubuntu**. 
  The first step would be to find the pair your device. For that you can install blueman in   ubuntu and then run it from
  terminal using 
  ```bash
  blueman-manager &
  ```
  After that you can search your device and then pair it with your system. Once paired, you can now connect it to serial port.
  Whenever you need to communicate with the device, you can connect it to serial port by right clicking on the mindwave. After use you should disconnect the device to make the port free for communication again.
 
* **Compile neurosky_parser.cpp**.
  Now you can use the neurosky_parser.cpp file to read and parse data from the serial port. To compile the code, use:
  ```bash
  g++ neurosky_parser.cpp -o neurosky_parser
  ```
  Now connect you device to serial port using blueman manager. It should show 
  ```bash
  connect to port /dev/rfcomm0
  ```
  Now run the c++ code using 
  ```bash
  sudo ./neurosky_parser 
  ```
  It will ask you to enter your password. Enter the password and then press Enter. Now you should be seeing some output in the terminal. It will generate a file called csv.txt that has the csv format output that we will need at a later stage. For more detail refer to code.

* **To Visualise Live Data**.
  Now since you are running the file, the code is also creating a file called plot.txt. This file will be used to visualise the current output. To see that you must have python version 3.4. Open a new terminal while keeping the current processes running. Go the folder where the codes are saved and type:
  ```bash
  python3.4 plot_waves.py
  ```
  It will show you the live graph of EEG power in following bands:
  ```bash
  delta, theta, low-alpha, high-alpha, low-beta, high-beta, low-gamma, medium-gamma
  ```

After collecting the data:

* **Make Data for Machine Learning part**. 
We will need two kind of files, one which follows the normal routine of test subject, and other would be which the user was forcefully blinking for a large duration. Make sure that both the data sets are large in number. Once you do that, you are ready to create the test data from training part. Open the merge_file.py and edit the two lines to the name of your file:
  ```bash
  blink = open('saty_blink.csv', 'r').read()
  normal = open('saty_normal.csv', 'r').read()
  ```
  Then run the following command from terminal:
    ```bash
  python3.4 merge_file.py > data.csv
  ```
  This will create the csv file for the neural network training.
