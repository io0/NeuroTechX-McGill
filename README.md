
# chattERP

ChattERP is an assistive and augmentative communication (AAC) device for individuals with speech and motor disabilities which strives to allow for rapid verbal communication where it is otherwise impossible. ChattERP harnesses the power of the P300 event-related potential as measured by the low-cost OpenBCI, an open-source brain-computer interface platform, to allow for text and emoji communication that is solely neural based. Electroencephalography (EEG) is used to detect the P300 induced by a speller matrix when the user-intended row and column flash. This project aims to integrate feedback from potential BCI end-users found in the literature, which highlights specific issues with current EEG-based BCIs, such as speed, cost and difficult set-up, as well as exciting avenues to explore, like interfaces with other electronics. The integration of neuroscience principles, linguistics research, and artificial intelligence methods yields a low-cost, multifunctional and accessible P300-based communication tool. We also expect that the addition of intuitive speech prediction technology and modern interface will improve the standard for AAC devices currently on the market.

For more information on the scientific, market and user research that went into this project, check out our [detailed report](https://github.com/io0/NeuroTechX-McGill-Backend/blob/master/ResearchReport.md)

## Contents
- `\scripts` contains scripts for offline analysis and visualization
	- `offline_classifier.py` contains code for preprocessing, LDA training and classification of known-good P300 data from Hoffman et al. 2007
	- `offline_classifier_openbci.py` contains code for preprocessing, LDA training and classification of our own data recorded using the OpenBCI
- `\data` contains sample data from our recording sessions
	- `raw_training.txt` contains raw data from 2 channels
	- `target.txt` contains the start index of 200 target stimulations
	- `nontarget.txt` contains the start index of 1000 nontarget stimulations
- `\classifier.py` is the main module for real-time P300 detection
- `\plugins\streamer_osc.py` streams predictions to OSC clients
- `\open_bci_v3.py` and `\user.py` instantiate the board and feed data to our plugin

## Setup
**1. Hardware**
   - Open BCI Cyton Board
      - 4x AA batteries 
      - Earlobe clips    
      - Wet/dry electrodes (+ conductive gel for wet electrodes)   
      - (Optional: Ultracortex)   
   - Soft measuring tape to locate 10-20 electrode positioning

**2. Computer & Software**
   - Speller interface (TODO: LINK TO OURS)
   - EEG signal processing pipeline (TODO: LINK TO OURS)
   
**3. Equipment**
(TODO: ADD PICTURES)

## Procedure
EEG signals are acquired in real time by invoking `python user.py -p COM6 --add streamer_osc` on the command line, with COM6 specifying the OpenBCI port. See [README_OpenBCI_Python.md](https://github.com/io0/NeuroTechX-McGill/blob/master/README_OpenBCI_Python.md) for more details. This connects to the board, and allows the user to send the command `/start` to commence acquisition.
The plugin looks for training data in `data`. Files in `data` can be replaced at any time with more recent calibration sessions.

## Dependencies:

* [Python 2.7](https://www.python.org/download/releases/2.7/) or later
* [Numpy 1.7](http://www.numpy.org/) or later
* [Pandas 0.22.0](https://pandas.pydata.org/)
* [SciPy 1.0](https://www.scipy.org/)
* [Matplotlib 2.2.0](https://matplotlib.org/)
* [Scikit-learn 0.19.1](http://scikit-learn.org/stable/)
* Signal acquisition dependencies located in [`requirements.txt`](https://github.com/io0/NeuroTechX-McGill/blob/master/requirements.txt)

## Signal processing
Channel data were filtered, split into windows of 600 ms starting at stimulus onset, and downsampled to 25 Hz. We applied a butterworth 0.5 - 20 Hz bandpass filter using scipy.signal.
Parameters for filtering and downsampling were chosen through offline analysis of P300 recording sessions. We were able to obtain the following plot using electrodes O1 and O2.
![Response plot](/figures/avg_response.png)

## Prediction pipeline
The classifier module manages data and performs predictions at intervals specified by the frontend. Upon initialization, session variables are created and the LDA model is fit to pre-recorded data.
Given the occurrence of sample drifting and unreliable arrival times, we decided to use a predetermined stimulus onset start time and the known sampling frequency to determine when to predict P300. Since samples are guaranteed to arrive in sequence, we use the sample count to mediate prediction blocks. 
Data is stored in a buffer in the inter-trial time so that filtering is passed through the buffer before the trial data, eliminating filtering artifacts.
Once three trials (showings of each row and column) have occurred, the block of trial data is processed as described above and epoched. Epochs are then grouped by the column or row that had been shown and passed to the LDA model, which outputs the probability of P300 for the epoch. The group with the highest average probability among the row groups and among the column groups is selected as the prediction.

## Speller interface
The server communication library included with the software emits OSC formatted data to a stream on the local server. A node package called OSC.io is used to re-interpret the OSC data as socket events titled “messages”. From that, socket.io is used to retrieve this data in real-time. The row and column number form the coordinates of the chosen letter or emoji. jQuery is used to animate the grid using a series of reciprocal callbacks to force synchronicity in Javascript by applying a class, then removing a class for the lit-up state. The letter or emoji is then inputted into the textbox and the letter is additionally fed into Awesomplete, a word prediction software. The software then searches its database of English words and displays the top 3 results that begin with that letter. The selection process is repeated for each letter to form complete words. Text-to-speech functions are possible using responsive voice API, which takes text input and provides speech output.
<img src="https://media.giphy.com/media/9PvaOvdBv9OXTfxfGY/giphy.gif" width="1000" height="500">


## The Team
McGill Enthusiasts for NeuroTechnology et al (MENTAL) is a club whose mandate is to raise awareness and interest in neurotechnology.
The team consists of an interdisciniplinary group of dedicated students.
<img src="https://github.com/io0/NeuroTechX-McGill/blob/master/MENTAL_logo.png" width="500" height="500">
