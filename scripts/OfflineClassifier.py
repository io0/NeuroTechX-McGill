import pandas as pd
import numpy as np
from pandas.plotting import scatter_matrix
import matplotlib.pyplot as plt
from scipy.signal import butter, lfilter
from sklearn import model_selection
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC




'''extract from imported csv file'''
import pandas as pd
df=pd.read_csv('sub4_ses4_39_data.csv', sep=',',header=None)
eeg_raw = df.values
df=pd.read_csv('sub4_ses4_39_stimuli.csv', sep=',',header=None)
stimuli = df.values
df=pd.read_csv('sub4_ses4_39_timepoints.csv', sep=',',header=None)
timepoints = df.values
df=pd.read_csv('sub4_ses4_39_target.csv', sep=',',header=None)
target = df.values


df=pd.read_csv('sub4_ses1_39_data.csv', sep=',',header=None)
eeg_raw2 = df.values
df=pd.read_csv('sub4_ses1_39_stimuli.csv', sep=',',header=None)
stimuli2 = df.values
df=pd.read_csv('sub4_ses1_39_timepoints.csv', sep=',',header=None)
timepoints2 = df.values
df=pd.read_csv('sub4_ses1_39_target.csv', sep=',',header=None)
target2 = df.values

df=pd.read_csv('sub4_ses2_39_data.csv', sep=',',header=None)
eeg_raw3 = df.values
df=pd.read_csv('sub4_ses2_39_stimuli.csv', sep=',',header=None)
stimuli3 = df.values
df=pd.read_csv('sub4_ses2_39_timepoints.csv', sep=',',header=None)
timepoints3 = df.values
df=pd.read_csv('sub4_ses2_39_target.csv', sep=',',header=None)
target3 = df.values


def butter_bandpass(lowcut, highcut, fs, order):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a


def butter_bandpass_filter(data, lowcut, highcut, fs, order):
    b, a = butter_bandpass(lowcut, highcut, fs, order)
    y = lfilter(b, a, data)
    return y

def filter_(data, lowcut, highcut, fs, order):
   nyq = 0.5 * fs
   b, a = butter(1, [lowcut/nyq, highcut/nyq], btype='band')
   for i in range(0, order):
       data = lfilter(b, a, data)
   return data




'''takes a target stimuli # and extracts time segments for this stimuli
returns a 2D array with each segment timepoints'''
def extract_target_channel(trace, timepoints, stimuli, pic_num, fs, index_cut):
    seg_length = int(fs*0.7)
    y=0
    while timepoints[y]<index_cut:
        y=y+1
    segments = []
    timepoints=timepoints-index_cut
    for x in range(y, len(timepoints)):
        if stimuli[x]==pic_num and (timepoints[x]+seg_length)<len(trace):
            segment = trace[int(timepoints[x]):int(timepoints[x]+seg_length)]
            segments.append(segment)
    segs = np.asarray(segments)
    return segs


'''separate the dataset into distinct segments for each picture stimuli
returns a multidimentional list'''
def extract_all_pics(trace, timepoints, stimuli, fs, index_cut):
    all_pic_segments = []
    for pic in range(1,7):        
        pic_segment = extract_target_channel(trace, timepoints, stimuli, pic, fs, index_cut)
        all_pic_segments.append(pic_segment)
    return all_pic_segments

'''apply filter and downsample over all channels'''
def filter_downsample_all(channels, num_channels, index_cut, lowcut, highcut, order, org_fs, downsample_fs):
    processed = []
    for x in range(0,num_channels):
        channel = channels[x,:]
        #initially apply a first pass filter then cut
        ch_filtered_butter_init = butter_bandpass_filter(channel, lowcut, highcut, org_fs, 1)
        ch_filtered_butter = butter_bandpass_filter(ch_filtered_butter_init[index_cut:len(ch_filtered_butter_init)], lowcut, highcut, org_fs, order)
        step = int(org_fs/downsample_fs)
        ch_downsample = ch_filtered_butter[::step]
        processed.append(ch_downsample)
    processed = np.asarray(processed)
    return processed


'''apply filter and downsample over all channels'''
def alt_filter_downsample_all(channels, num_channels, index_cut, lowcut, highcut, order, org_fs, downsample_fs):
    processed = []
    for x in range(0,num_channels):
        channel = channels[x,:]
        ch_filtered_butter_init = filter_(channel, lowcut, highcut, org_fs, order)
        ch_filtered_butter = ch_filtered_butter_init[index_cut:len(ch_filtered_butter_init)]
        step = int(org_fs/downsample_fs)
        ch_downsample = ch_filtered_butter[::step]
        processed.append(ch_downsample)
    processed = np.asarray(processed)
    return processed



'''computes a list of time segments for all channels and pictures, gives list[channel][image][trace]'''
def pic_channel_all (channels, num_channels, stimuli, timepoints, org_fs, downsample_fs, index_cut):
    downsample_index_cut=int((downsample_fs/org_fs)*index_cut)
    downsample_timepoints=(downsample_fs/org_fs)*timepoints
    all_pic_segments = []
    for x in range(0,num_channels):
        ch_all_pic = extract_all_pics(channels[x,:], downsample_timepoints, stimuli, downsample_fs, downsample_index_cut)
        all_pic_segments.append(ch_all_pic)
    return all_pic_segments

'''this function will take a 2D array of time segments, and remove those that 
have a variance above a given threshold relative to the average variance of 
the dataset'''    
'''the threshold value must be between 0 and 1'''
def outlier_removal(traces, threshold):
    var_trace = np.array([])
    for trace in traces:
        var_trace = np.insert(var_trace, len(var_trace), np.var(trace))
    mean_var = np.mean(var_trace)
    indices = np.array([])
    var_threshold=mean_var*threshold
    for x in range(0, len(var_trace)):
        if var_trace[x]>var_threshold:
            indices = np.insert(indices, len(indices), x)
    if len(indices)==0:
        return traces
    cleaned_traces = np.delete(traces, indices.astype(int), 0)
    return cleaned_traces

'''function to remove outliers until no sample fall out of the threshold'''
def repeated_removal(traces, threshold):
    prev_traces = np.zeros([2, 2])
    while len(traces[:,0])!=len(prev_traces[:,0]):
        prev_traces=traces
        traces = outlier_removal(traces, threshold)
    return traces



'''parameters'''
Fs_Hz = 2048 #original sampling frequency
lowcut=1
highcut=12
order=6 #order of the bandpass filter
index_cut=5000 #indixes that are cut after first filtering at original Fs
seg_length=0.7
downsample_fs=64 #frequency for downsampling
num_channels = 34
threshold = 2

'''run analysis over two independent training sessions, to test performance on a third one'''
#preprocessing of all channels
preprocessed_eeg = alt_filter_downsample_all(eeg_raw, num_channels, index_cut, lowcut, highcut, order, Fs_Hz, downsample_fs)
complete_data = pic_channel_all(preprocessed_eeg, num_channels, stimuli[0,:], timepoints[0,:], Fs_Hz, downsample_fs, index_cut)


preprocessed_eeg2 = alt_filter_downsample_all(eeg_raw2, num_channels, index_cut, lowcut, highcut, order, Fs_Hz, downsample_fs)
complete_data2 = pic_channel_all(preprocessed_eeg2, num_channels, stimuli2[0,:], timepoints2[0,:], Fs_Hz, downsample_fs, index_cut)

preprocessed_eeg3 = alt_filter_downsample_all(eeg_raw3, num_channels, index_cut, lowcut, highcut, order, Fs_Hz, downsample_fs)
complete_data3 = pic_channel_all(preprocessed_eeg3, num_channels, stimuli3[0,:], timepoints3[0,:], Fs_Hz, downsample_fs, index_cut)





'''PLoting the avergage traces: Analysis over 8 p300 channels'''
#channels: O1, Oz, O2, PO3, Pz, PO4, P3, P4
channels = np.array([11, 12, 13, 14, 15, 16, 17, 18])


sorted_p300_data = []
for y in range(0,6):
    pic_channels = []
    for x in channels:
        pic_trace = complete_data2[x][y]
        cleaned_pic_trace = repeated_removal(pic_trace, threshold)
        pic_channels.append(cleaned_pic_trace)
    sorted_p300_data.append(pic_channels)

length = len(sorted_p300_data[0][0][0,:])

#calculate the mean trace for each image
means = []
for y in range(0,6):
    all_ch_means = np.zeros([num_channels,length])
    for x in range(0,len(channels)):
        pic_trace = sorted_p300_data[y][x]
        all_ch_means[x,:] = np.mean(pic_trace,0)
    means.append(np.mean(all_ch_means, 0))
        
plt.figure(1)
for x in range(0,6):
    plt.plot(means[x])


non_target = np.zeros([5, length])
j=0
for x in range(0,6):
    if x!=int(target[0]-1):        
        non_target[j,:] = means[x]
        j=j+1
        

mean_non_target=np.mean(non_target, 0)

plt.figure(2)
plt.plot(mean_non_target)
plt.plot(means[int(target[0]-1)])




'''Analysis over 8 p300 channels'''
#channels: O1, Oz, O2, PO3, Pz, PO4, P3, P4
channels = np.array([11, 12, 13, 14, 15, 16, 17, 18])


dataset = []
num_trace_pic = [] #sets the number of traces for a given pic
for y in range(0,6):
    num_traces = 0
    for x in channels:
        traces = complete_data[x][y]
        length = len(traces[:,0])
        num_traces = num_traces + length
        for i in range(0, length):
            if y+1==target[0,0]:
                dataset.append(np.append(traces[i,:],1))
            else:
                dataset.append(np.append(traces[i,:],0))
        traces = complete_data2[x][y]
        length = len(traces[:,0])
        num_traces = num_traces + length
        for i in range(0, length):
            if y+1==target2[0,0]:
                dataset.append(np.append(traces[i,:],1))
            else:
                dataset.append(np.append(traces[i,:],0))
    num_trace_pic.append(num_traces)

dataset3 = []
num_trace_pic3 = [] #sets the number of traces for a given pic
for y in range(0,6):
    num_traces = 0
    for x in channels:
        traces = complete_data3[x][y]
        length = len(traces[:,0])
        num_traces = num_traces + length
        for i in range(0, length):
            if y+1==target3[0,0]:
                dataset3.append(np.append(traces[i,:],1))
            else:
                dataset3.append(np.append(traces[i,:],0))
    num_trace_pic3.append(num_traces)



#Validation set
array = np.array(dataset)
size = len(array[0,:])
X = array[:,0:size-2]
Y = array[:,size-1]

validation_size = 0.25
seed = 7
X_train, X_validation, Y_train, Y_validation = model_selection.train_test_split(X, Y, test_size=validation_size, random_state=seed)


#train the classifier and predict the prob for each trace to be a p300
lda = LinearDiscriminantAnalysis()
lda = lda.fit(X_train, Y_train)
Prob = lda.predict_proba(array[:,0:size-2])

array3 = np.array(dataset3)
Prob = lda.predict_proba(array3[:,0:size-2])


#calculate the mean prob for each pic
target_probs = []
first_index = 0
for x in range(0, 6):
    length = num_trace_pic3[x]
    target_probs.append(np.mean(Prob[first_index:length+first_index,1]))
    first_index = first_index + length

#print what is the prob for each pic
for x in range(0, 6):
    print("Estimated prob for pic #" + str(x+1) + " is " + str(target_probs[x]))

#select the pic with largest probability as a guess
guess_target = target_probs.index(max(target_probs)) + 1
print("The target is pic #" + str(guess_target))
if guess_target==target3:
    print("Good guess!")
else:
    print("Bad guess.")

