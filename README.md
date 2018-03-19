
# chattERP

We take the ease with which we communicate with others in our daily lives for granted -- when communication becomes laborious, or impossible, this can have a severe negative impact on an individual's life.

ChattERP is an assistive and augmentative communication (AAC) device for individuals with speech and motor disabilities, providing an interface for rapid verbal communication where this is otherwise impossible. ChattERP harnesses the power of the P300 event-related potential (ERP), a waveform reflecting decision-making, as measured by the low-cost OpenBCI, an open-source brain-computer interface platform. The identification of this neural marker of decision allows for communication that is solely based on neural activity. Electroencephalography (EEG) is used to detect the P300 induced by a speller matrix, ultimately allowing for identification of a single cell in the matrix. The identification of a single row occurs when the P300 signal is detected during the flash of the row of interest, and then again with the flash of the column of interest, thus isolating the cell containing the desired symbol. This project aims to integrate feedback from potential AAC end-users found in the literature. These individuals have highlighted specific issues with current EEG-based BCIs, such as speed, cost, difficulty of set-up, and non-user-friendly interfaces. In addition to these problems with current speller systems, users have also proposed exciting avenues to explore, such as interfacing neural spellers with other electronics. 

We have researched these concerns, and created a system which prioritizes communication efficiency, ease of use, interpretability, integration with other electronics, and user comfort. The interface has been optimized for efficiency, and user experience has been improved with options to communicate using text or emoji symbols as shortcuts. The integration of neuroscience principles, linguistics research, and artificial intelligence classifier algorithms yields a low-cost, multifunctional, and accessible P300-based communication tool. We expect that the addition of intuitive speech prediction technology and an interpretable modern interface will improve the standard for AAC devices currently on the market.


For more information on the scientific, market and user research that went into this project, check out our [detailed report](https://github.com/io0/NeuroTechX-McGill-Backend/blob/master/ResearchReport.md).

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
- `\frontend` contains all modules pertaining to the frontend display

## Setup
**1. Hardware**
   - Open BCI Cyton Board
      - 4x AA batteries 
      - 2x Earlobe clips (Ground and mastoid reference) 
      - Wet/dry electrodes (+ conductive gel for wet electrodes)   
      - (Optional: Ultracortex)   
   - Soft measuring tape to locate 10-20 electrode positioning

**2. Computer & Software**
   - [Speller interface](https://github.com/io0/NeuroTechX-McGill/blob/master/frontend/README.md)
   - [EEG signal processing pipeline](https://github.com/io0/NeuroTechX-McGill/blob/master/classifier.py)
   - Tested on Windows 10
   - Frontend runs on [Google Chrome](https://www.google.com/chrome/)

## Procedure

**A. Backend procedure** <br>
EEG signals are acquired in real time by invoking `python user.py -p COM6 --add streamer_osc` on the command line, with COM6 specifying the OpenBCI port. See [README_OpenBCI_Python.md](https://github.com/io0/NeuroTechX-McGill/blob/master/README_OpenBCI_Python.md) for more details. This connects to the board, and allows the user to send the command `/start` to commence acquisition.

This is the command line output with model probability predictions:
![Command](/figures/plugin_activation.png) 

The plugin looks for training data in `data`. Files in `data` can be replaced at any time with more recent calibration sessions.

**B. Frontend procedure** <br>
1. Download LTS version of [Node.js](https://nodejs.org/en/download/current/)
2. Open terminal and migrate to the `NeuroTechX-McGill/frontend/` directory on your computer
3. Run `npm install` in terminal -- this will install all necessary dependencies
4. Launch chattERP by running `node app` in terminal
5. Open Google Chrome and go to [localhost:3000](http://localhost:3000)


## Dependencies
* [Python 2.7](https://www.python.org/download/releases/2.7/) or later
* [Numpy 1.7](http://www.numpy.org/) or later
* [Pandas 0.22.0](https://pandas.pydata.org/)
* [SciPy 1.0](https://www.scipy.org/)
* [Matplotlib 2.2.0](https://matplotlib.org/)
* [Scikit-learn 0.19.1](http://scikit-learn.org/stable/)
* Signal acquisition dependencies located in [`requirements_signal.txt`](https://github.com/io0/NeuroTechX-McGill/blob/master/requirements_signal.txt)
* Frontend dependencies located in [`requirements_frontend.txt`](https://github.com/io0/NeuroTechX-McGill/blob/master/requirements_frontend.txt)

## Signal processing
![Preprocessing pipeline](/figures/preprocessing_pipeline.png)

Channel data were filtered, split into windows of 600 ms starting at stimulus onset, and downsampled to 25 Hz. We applied a butterworth 0.5 - 20 Hz bandpass filter using scipy. The result is a vector with 15 features that can be passed to the LDA classifier. With our pipeline, we were able to obtain validation accuracies of 82%.

Parameters for filtering and downsampling were chosen through offline analysis of P300 recording sessions. We were able to obtain the following plot using electrodes PO3 and PO4.

![Response plot](/figures/avg_response.png)

## Prediction pipeline
The classifier module manages data and performs predictions at intervals specified by the frontend. Upon initialization, session variables are created and the LDA model is fit to pre-recorded data.

Given the occurrence of sample drifting and unreliable arrival times, we decided to use a predetermined stimulus onset start time and the known sampling frequency to determine when to predict P300. Since samples are guaranteed to arrive in sequence, we use the sample count to mediate prediction blocks. 

Data is stored in a buffer in the inter-trial time so that filtering is passed through the buffer before the trial data, eliminating filtering artifacts.

Once three trials (showings of each row and column) have occurred, the block of trial data is processed as described above and epoched. Epochs are then grouped by the column or row that had been shown and passed to the LDA model, which outputs the probability of P300 for the epoch. The group with the highest average probability among the row groups and among the column groups is selected as the prediction.

## Speller interface
The server communication library included with the software emits OSC formatted data to a stream on the local server. A node package called OSC.io is used to re-interpret the OSC data as socket events titled “messages”. From that, socket.io is used to retrieve this data in real-time. The row and column number form the coordinates of the chosen letter or emoji. jQuery is used to animate the grid using a series of reciprocal callbacks to force synchronicity in Javascript by applying a class, then removing a class for the lit-up state. The letter or emoji is then inputted into the textbox and the letter is additionally fed into Awesomplete, a word prediction software. The software then searches its database of English words and displays the top 3 results that begin with that letter. The selection process is repeated for each letter to form complete words. Text-to-speech functions are possible using responsive voice API, which takes text input and provides speech output.


<img src="https://media.giphy.com/media/1BhDpEtftozn6M0naw/giphy.gif" width="1000" height="500">

## Future Steps
We would like to implement real-time data visualization in conjunction with the speller, so that the signal can be monitored more easily. As well, instead of recording training data beforehand, we would like to add an online calibration phase.

## The Team
[McGill Enthusiasts for NeuroTechnology et al (MENTAL)](https://www.facebook.com/McGillNeurotech/) is a club whose mandate is to raise awareness and interest in neurotechnology.
The team consists of an interdisciplinary group of dedicated undergraduate students from McGill University.

<img src="https://github.com/io0/NeuroTechX-McGill/blob/master/MENTAL_logo.png" width="100" height="100">
