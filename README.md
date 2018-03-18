# chattERP

ChattERP is an assistive and augmentative communication (AAC) device for individuals with speech and motor disabilities which strives to allow for rapid verbal communication where it is otherwise impossible. ChattERP harnesses the power of the P300 event-related potential as measured by the low-cost OpenBCI, an open-source brain-computer interface platform, to allow for text and emoji communication that is solely neural based. Electroencephalography (EEG) is used to detect the P300 induced by a speller matrix when the user-intended row and column flash. This project aims to integrate feedback from potential BCI end-users found in the literature, which highlights specific issues with current EEG-based BCIs, such as speed, cost and difficult set-up, as well as exciting avenues to explore, like interfaces with other electronics. The integration of neuroscience principles, linguistics research, and artificial intelligence methods yields a low-cost, multifunctional and accessible P300-based communication tool. We also expect that the addition of intuitive speech prediction technology and modern interface will improve the standard for AAC devices currently on the market.

For more information on the scientific, market and user research that went into this project, check out our [detailed report](https://github.com/io0/NeuroTechX-McGill-Backend/blob/master/ResearchReport.md)

## Setup
**1. Hardware**
   - Open BCI
      - 4x AA batteries 
      - Earlobe clips    
      - Wet/dry electrodes (+ conductive gel for wet electrodes)   
      - (Optional: Ultracortex)   
   - Soft measuring tape to locate 10-20 electrode positioning

**2. Computer & Software**
   - Speller interface (LINK TO OURS)
   - EEG signal processing pipeline (LINK TO OURS)
   
**3. Equipment**
(TODO: ADD PICTURES)

## Procedure
EEG signals are acquired in real time by invoking `python user.py -p COM6 --add streamer_osc` on the command line, with COM6 specifying the OpenBCI port. See [README_OpenBCI_Python.md](https://github.com/io0/NeuroTechX-McGill/blob/master/README_OpenBCI_Python.md) for more details. This connects to the board, and allows the user to send the command `/start` to commence acquisition.
Training data for the classifier is located in `training_data.csv` and can be replaced at any time with more recent calibration sessions.

## Dependencies:

* [Python 2.7](https://www.python.org/download/releases/2.7/) or later
* [Numpy 1.7](http://www.numpy.org/) or later
* Signal acquisition dependencies located in [`requirements.txt`](https://github.com/io0/NeuroTechX-McGill/blob/master/requirements.txt)
## Signal processing

![Response plot](avg_response.png)!
## Speller interface
The server communication library included with the software emits OSC formatted data to a stream on the local server. A node package called OSC.io is used to re-interpret the OSC data as socket events titled “messages”. From that, socket.io is used to retrieve this data in real-time. The row and column number form the coordinates of the chosen letter or emoji. jQuery is used to animate the grid using a series of reciprocal callbacks to force synchronicity in Javascript by applying a class, then removing a class for the lit-up state. The letter or emoji is then inputted into the textbox and the letter is additionally fed into Awesomplete, a word prediction software. The software then searches its database of English words and displays the top 3 results that begin with that letter. The selection process is repeated for each letter to form complete words. Text-to-speech functions are possible using responsive voice API, which takes text input and provides speech output.

![Alt Text](https://media.giphy.com/media/9PvaOvdBv9OXTfxfGY/giphy.gif)

## The Team
McGill Enthusiasts for NeuroTechnology et al (MENTAL) is a club whose mandate is to raise awareness and interest in neurotechnology. The team consists of an interdisciniplinary group of dedicated students.
![Alt Text](https://github.com/io0/NeuroTechX-McGill/blob/master/MENTAL_logo.png | width=100)
