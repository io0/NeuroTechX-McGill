

## INSERT NAME HERE

INSERT NAME HERE is an assistive and augmentative communication (AAC) device for individuals with speech and motor disabilities which strives to allow for rapid verbal communication where it is otherwise impossible. INSERT NAME HERE harnesses the power of the P300 event-related potential as measured by the low-cost OpenBCI, an open-source brain-computer interface platform, to allow for text and emoji communication that is solely neural based. Electroencephalography (EEG) is used to detect the P300 induced by a speller matrix when the user-intended row and column flash. This project aims to integrate feedback from potential BCI end-users found in the literature, which highlights specific issues with current EEG-based BCIs, such as speed, cost and difficult set-up, as well as exciting avenues to explore, like interfaces with other electronics. The integration of neuroscience principles, linguistics research, and artificial intelligence methods yields a low-cost, multifunctional and accessible P300-based communication tool. We also expect that the addition of intuitive speech prediction technology and modern interface will improve the standard for AAC devices currently on the market.

For more information on the scientific, market and user research that went into this project, check out our [detailed report](https://github.com/io0/NeuroTechX-McGill-Backend/blob/master/ResearchReport.md)


## Setup
The following hardware are used:
* Open BCI
* 4x AA batteries
* Earlobe clips
* Wet/dry electrodes (+ conductive gel for wet electrodes)
  ** (Optional: Ultracortex)
* Soft measuring tape to locate 10-20 electrode positioning
* Computer and software
* Speller interface (TODO: LINK TO OURS)
* EEG signal processing pipeline (TODO: LINK TO OURS)
(TODO: ADD PICTURES)

## Procedure
After downloading the repository, the dependencies are installed and run using Python command “user.py -p COM6--add streamer_osc”. This connects to the board and the command is sent to “/start” when prompted. The server communication library included with the software emits OSC formatted data to a stream on the local server. A node package called OSC.io is used to re-interpret the OSC data as socket events titled “messages”. From that, socket.io is used to retrieve this data in real-time. The row and column number form the coordinates of the chosen letter or emoji. jQuery is used to animate the grid using a series of reciprocal callbacks to force synchronicity in Javascript by applying a class, then removing a class for the lit-up state. The letter or emoji is then inputted into the textbox and the letter is additionally fed into Awesomplete, a word prediction software. The software then searches its database of English words and displays the top 3 results that begin with that letter. The selection process is repeated for each letter to form complete words. Text-to-speech functions are possible using responsive voice API, which takes text input and provides speech output. 

## Dependancies:

* [Python 2.7](https://www.python.org/download/releases/2.7/) or later
* [Numpy 1.7](http://www.numpy.org/) or later 
* [Yapsy](http://yapsy.sourceforge.net/) -- if using pluging via `user.py`
* [The signal acquisition dependencies](https://github.com/OpenBCI/OpenBCI_Python/blob/master/requirements.txt)

## OpenBCI

OpenBCI is a 8 and 32 bit board with 8 or 16 channels.

This library includes the main open_bci_v3 class definition that instantiates an OpenBCI Board object. This object will initialize communication with the board and get the environment ready for data streaming. This library is designed to work with iOS and Linux distributions. To use a Windows OS, the __init__ function in open_bci_v3.py needs to be changed to establish a serial connection in Windows.
The [Cyton board](http://docs.openbci.com/Hardware/02-Cyton) needs to be properly connected. 

### OpenBCI_Python

The [Python software library](https://github.com/OpenBCI/OpenBCI_Python) is designed to work with OpenBCI hardware.

### Ganglion Board

The Ganglion board relies on Bluetooth Low Energy connectivity (BLE). You should also retrieve the bluepy submodule for a more up-to-date version than the version `1.0.5` available at that time through `pip`. To do so, clone this repository with the `--recursive` flag then type `make` inside `bluepy/bluepy`. Note that you may need to run the script with root privileges to for some functionality, e.g. auto-detect MAC address.

You may also need to alter the settings of your bluetooth adapter in order to reduce latency and avoid packet drops -- e.g. if the terminal spams "Warning: Dropped 1 packets" several times a seconds

For example, on Linux, assuming `hci0` is the name of your bluetooth adapter:

`sudo bash -c 'echo 9 > /sys/kernel/debug/bluetooth/hci0/conn_min_interval'`

`sudo bash -c 'echo 10 > /sys/kernel/debug/bluetooth/hci0/conn_max_interval'`


## Functionality

### Basic usage

The startStreaming function of the Board object takes a callback function and begins streaming data from the board. Each packet it receives is then parsed as an OpenBCISample which is passed to the callback function as an argument. 

OpenBCISample members:
-id:
	int from 0-255. Used to tell if packets were skipped.

-channel_data:
	8 int array with current voltage value of each channel (1-8)

-aux_data:
	3 int array with current auxiliary data. (0s by default)

### user.py

This code provides a simple user interface (called user.py) to handle various plugins and communicate with the board. To use it, connect the board to your computer using the [dongle](http://docs.openbci.com/tutorials/01-GettingStarted). 

Then simply run the code given as an argument the port your board is connected to:
For example, on Linux:
> $python user.py -p /dev/ttyUSB0 

The program should establish a serial connection and reset the board to default settings. When a '-->' appears, you can type a [character]( http://docs.openbci.com/software/01-OpenBCI_SDK)  that will be sent to the board using ser.write. This allows you to change the settings on the board. 

A good first test is to try is to type '?':
>--> ?

This should output the current configuration settings on the board.

Another test would be to change the board settings so that all the pins in the board are internally connected to a test (square) wave. To do so, type:

>--> [

Alternatively, there are 6 test signals pre configured:

> --> /test1 (connect all pins to ground)

> --> /test2 (connect all pins to vcc)

> --> /test3 (Connecting pins to low frequency 1x amp signal)

> --> /test4 (Connecting pins to high frequency 1x amp signal)

> --> /test5 (Connecting pins to low frequency 2x amp signal)

> --> /test6 (Connecting pins to high frequency 2x amp signal)

The / is used in the interface to execute a pre-configured command. Writing anything without a preceding '/' will automatically write those characters, one by one, to the board.

For example, writing 
> -->x3020000X 
will do the following:

‘x’ enters Channel Settings mode. Channel 3 is set up to be powered up, with gain of 2, normal input, removed from BIAS generation, removed from SRB2, removed from SRB1. The final ‘X’ latches the settings to the ADS1299 channel settings register.

Pre-configured commands that use the / prefix are:

test (As explained above) 

> --> /test4

start selected plugins (see below)

> --> /start

Adding the argument "T:number" will set a timeout on the start command.

> --> /start T:5

Stop the steam to issue new commands

> --> /stop

#### Useful commands:
]
Writting to SD card a high frequency square wave (test5) for 3 seconds:
```
$ python user.py -p /dev/ttyUSB0
User serial interface enabled...
Connecting to  /dev/ttyUSB0
Serial established...
View command map at http://docs.openbci.com.
Type start to run. Type /exit to exit.

--> 
OpenBCI V3 8bit Board
Setting ADS1299 Channel Values
ADS1299 Device ID: 0x3E
LIS3DH Device ID: 0x33
Free RAM: 447
$$$
--> /test5
Warning: Connecting pins to high frequency 2x amp signal

--> a
Corresponding SD file OBCI_18.TXT$$$
--> /start T:3

```

NOTE: When writing to the board, the resposne might be delayed. In fact, the board sometimes lags and requires the user to hit enter on the user.py script until you get a response.

#### Ganglion

The Ganglion board is currently supported only on Linux. The communication is made directly through bluetooth (BLE), instead of using a dongle through a serial port. To launch the script, auto-detect the bluetooth MAC address of the nearby board and print values upon `/start`:

> $sudo python user.py --board ganglion --add print

Note that if you want to configure manually the board, the API differs from the Cyton, refer to the proper [documentation](http://docs.openbci.com/OpenBCI%20Software/06-OpenBCI_Ganglion_SDK)

### Plugins

#### Use plugins

Select the print plugin:

> $python user.py -p /dev/ttyUSB0 --add print

Plugin with optional parameter:

> $python user.py -p /dev/ttyUSB0 --add csv_collect record.csv

Select several plugins, e.g. streaming to OSC and displaying effective sample rate:

> $python user.py -p /dev/ttyUSB0 --add streamer_osc --add sample_rate

Note: type `/start` to launch the selected plugins.

#### Create new plugins

Add new functionalities to user.py by creating new scripts inside the `plugins` folder. Your class must inherit from yapsy.IPlugin: see below a minimal example with `print` plugin:

```python
	import plugin_interface as plugintypes
	
	class PluginPrint(plugintypes.IPluginExtended):
		def activate(self):
			print "Print activated"
		
		def deactivate(self):
			print "Goodbye"
			
		def show_help(self):
			print "I do not need any parameter, just printing stuff."
				
		# called with each new sample
		def __call__(self, sample):
			print "----------------"
			print("%f" %(sample.id))
			print sample.channel_data
			print sample.aux_data
```

Describe your plugin with a corresponding `print.yapsy-plugin`:

```
	[Core]
	Name = print
	Module = print

	[Documentation]
	Author = Various
	Version = 0.1
	Description = Print board values on stdout
```
Your plugin should be automatically detected by `user.py`.

#### Existing plugins

* `print`: Display sample values -- *verbose* output!

* `csv_collect`: Export data to a csv file.

* `sample_rate`: Print effective sampling rate averaged over XX seconds (default: 10).

* `streamer_tcp`: Acts as a TCP server, using a "raw" protocol to send value. 
	* The stream can be acquired with [OpenViBE](http://openvibe.inria.fr/) acquisition server, selecting telnet, big endian, float 32 bits, forcing 250 sampling rate (125 if daisy mode is used).
	* Default IP: localhost, default port: 12345

* `streamer_osc`: Data is sent through OSC (UDP layer).
	* Default IP: localhost, default port: 12345, default stream name: `/openbci`
	* Requires pyosc. On linux type either `pip install --pre pyosc` as root, or `pip install --pre --user`.

* `udp_server`: Very simple UDP server that sends data as json. Made to work [with](https://github.com/OpenBCI/OpenBCI_Node)
	* Default IP: 127.0.0.1, default port: 8888

* `streamer_lsl`: Data is sent through [LSL](https://github.com/sccn/labstreaminglayer/).
	* Default EEG stream name "OpenBCI_EEG", ID "openbci_eeg_id1"; default AUX stream name "OpenBCI_AUX", ID "openbci_aux_id1".
	* Requires LSL library. Download last version from [official site](http://sccn.ucsd.edu/pub/software/LSL/SDK/liblsl)-Python-1.10.2.zip and unzip files in a "lib" folder at the same level as `user.py`.

Tip: Type `python user.py --list` to list available plugins and `python user.py --help [plugin_name]` to get more information.

### Scripts

In the `scripts` folder you will find code snippets that use directly the `OpenBCIBoard` class from `open_bci_v3.py`.

Note: copy `open_bci_v3.py` there if you want to run the code -- no proper package yet.

* `test.py`: minimal example, printing values.
* `stream_data.py` a version of a TCP streaming server that somehow oversamples OpenBCI from 250 to 256Hz.
* `upd_server.py` *DEPRECATED* (Use Plugin): [see](https://github.com/OpenBCI/OpenBCI_Node) for implementation example.

## The Team
McGill Enthusiasts for NeuroTechnology et al (MENTAL) is a club whose mandate is to raise awareness and interest in neurotechnology. The team consists of an interdisciniplinary group of dedicated students. 
(TODO: ADD our logo)
