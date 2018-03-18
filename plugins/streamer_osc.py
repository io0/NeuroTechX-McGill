
# requires python-osc
from pythonosc import osc_message_builder
from pythonosc import udp_client
import plugin_interface as plugintypes
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn import model_selection
import time
from scipy import signal
import numpy as np

# Use OSC protocol to broadcast data (UDP layer), using "/openbci" stream. (NB. does not check numbers of channel as TCP server)

class Classifier():
    def __init__(self,
                 start_time,    #start time in seconds
                 channels = [0,1,2],
                 num_trials=3,
                 num_rows=6,
                 num_columns=6,
                 flash=0.2,
                 inter_flash=0.1,
                 inter_mega_trial=3):
        self.column_order = [5, 3, 2, 0, 4, 1, 3, 2, 0, 1, 5, 4, 3, 4, 0, 5, 2, 1]
        self.row_order = [1, 4, 2, 5, 0, 3, 3, 2, 5, 0, 1, 4, 4, 0, 2, 3, 1, 5]
        self.num_rows = num_rows
        self.num_columns = num_columns
        self.lda = LinearDiscriminantAnalysis()
        self.fs = 250
        self.started = False
        self.collecting = False
        self.buffer = []
        self.data = []
        self.stimulus_time = int((inter_flash + flash) * self.fs)
        self.trial_length = self.stimulus_time * (num_rows + num_columns)
        self.samples_in_data = num_trials * self.trial_length
        self.samples_since_last = 0
        self.num_samples = 0
        self.channels = channels
        self.start_time = start_time
        self.inter_mega_trial = inter_mega_trial
        self.counter = 0
        self.window_length = int(0.6 * 250)
        #print(start_time)
        
        self.lowcut = 0.5
        self.highcut = 20
        self.ds_factor = 3
        
        self.train()
    def train(self):
        data = np.loadtxt('data/raw_training.txt',
                      delimiter=',')
        stims = np.loadtxt('data/target.txt', dtype=np.uint)
        nstims = np.loadtxt('data/nontarget.txt', dtype=np.uint)
        data = self.filter_(data)
        # Epoch and downsample
        t_ep1 = self.epoch_data_by_stims(data, stims)
        t_ep = t_ep1[:, ::self.ds_factor]
        n_ep1 = self.epoch_data_by_stims(data, nstims)
        n_ep = n_ep1[:, ::self.ds_factor]
        
        # Prepare inputs for classifier
        t_ep = np.hstack((t_ep, np.ones([t_ep.shape[0],1])))
        n_ep = np.hstack((n_ep, np.zeros([n_ep.shape[0],1])))
        X = np.vstack((t_ep, n_ep))[:,:-1]
        Y = np.vstack((t_ep, n_ep))[:,-1]
        ''' Testing classifier
        seed = 7
        X_train, X_validation, Y_train, Y_validation = model_selection.train_test_split(X, Y, test_size=0.2, random_state=seed)
        kfold = model_selection.KFold(n_splits=10, random_state=seed)
        cv_results = model_selection.cross_val_score(self.lda, X_train, Y_train, cv=kfold, scoring='accuracy')
        print(cv_results)
        '''
        self.lda.fit(X,Y)
        
        
    def add_sample(self, sample):
        message = ''
        self.counter += 1
        if self.collecting:
            self.data.append(sample.channel_data[0:2])
            self.num_samples += 1
            if self.num_samples == self.samples_in_data:
                print(self.counter)
                message = self.run_prediction()
                self.reset()
        else:
            self.buffer.append(sample.channel_data[0:2])
            self.samples_since_last += 1
            if self.started:
                if self.samples_since_last == self.inter_mega_trial * self.fs:
                    self.collecting = True
                    print(self.counter)
            else: 
                if time.time() > self.start_time:
                    self.started = True
                    self.collecting = True
                    print(self.counter)
        return message
    def reset(self):
        self.buffer = self.data[-250*5:]
        self.data = []
        self.samples_since_last = 0
        self.num_samples = 0
        self.collecting = False
    def run_prediction(self,):

        buffer_length = len(self.buffer)
        all_data = np.vstack((np.array(self.buffer), np.array(self.data)))
        filtered_data = self.filter_(all_data)
        REALdata = filtered_data[buffer_length:]    # cut out filtering artifacts/buffer
        print(REALdata.shape)
        data = self.epoch_data(REALdata)
        rows = self.extract(data, row=True)
        rows = rows[:,:,::self.ds_factor]
        columns = self.extract(data, row=False)
        columns = columns[:,:,::self.ds_factor]
        print(rows.shape)
        probs = np.array([np.mean(self.lda.predict_proba(row), axis=0) for row in rows])
        print(probs)
        pred_row = np.argmax(probs[:, 1])
        probs = np.array([np.mean(self.lda.predict_proba(column), axis=0) for column in columns])
        pred_col = np.argmax(probs[:, 1])
        message = str(pred_row) + str(pred_col)
        return message

    def filter_(self,arr):
       nyq = 0.5 * self.fs
       order = 1
       b, a = signal.butter(order, [self.lowcut/nyq, self.highcut/nyq], btype='band')
       for i in range(0, 5):
           arr = signal.lfilter(b, a, arr, axis=0)
       return arr
       
    def epoch_data(self, arr):
        new_arr = []
        i = 0 
        while i <= len(arr) - self.window_length:
            window = arr[i:i+self.window_length].T
            window = np.mean(window, axis=0)
            new_arr.append(window)
            i += self.stimulus_time
        if (i < len(arr)):
            window = arr[i:].T
            window = np.mean(window, axis=0)
            b = np.zeros([self.window_length - len(window)]) # zero pad
            window = np.hstack((window,b))
            new_arr.append(window)
        n = np.array(new_arr)
        print(n.shape)
        return n
    def epoch_data_by_stims(self, arr, stims):
        new_arr = []
        for i in stims:
            window = arr[i:i+self.window_length].T
            window = np.mean(window, axis=0)
            if np.max(np.abs(window)) < 300:
                new_arr.append(window)
        n = np.array(new_arr)
        print(n.shape)
        return n
    def extract(self, arr, row=True):
        if row:
            order = self.row_order
            num_ = self.num_rows
            arr = arr[[0,1,2,3,4,5,12,13,14,15,16,17,24,25,26,27,28,29]]
        else: 
            order = self.column_order
            num_ = self.num_columns
            arr = arr[[6,7,8,9,10,11,18,19,20,21,22,23,30,31,32,33,34,35]]
        new_arr = [[] for i in range (0, num_)]
        for i, elem in enumerate(order):
            new_arr[elem].append([arr[i]])
        return np.squeeze(np.array(new_arr))



class StreamerOSC(plugintypes.IPluginExtended):
    """

    Relay OpenBCI values to OSC clients

    Args:
      port: Port of the server
      ip: IP address of the server
      address: name of the stream
    """
        
    def __init__(self, ip='localhost', port=12345, address="/openbci"):
        # connection infos
        self.ip = ip
        self.port = port
        self.address = address
        self.clf = Classifier(time.time())  #initialize classifier
        print(self.clf.start_time)
        
    # From IPlugin
    def activate(self):
        if len(self.args) > 0:
            self.ip = self.args[0]
        if len(self.args) > 1:
            self.port = int(self.args[1])
        if len(self.args) > 2:
            self.address = self.args[2]
        # init network
        print("Selecting OSC streaming. IP: " + self.ip + ", port: " + str(self.port) + ", address: " + self.address)
        self.client = udp_client.SimpleUDPClient(self.ip, self.port)
        
    # From IPlugin: close connections, send message to client
    def deactivate(self):
        self.client.send_message("/quit")
        
    # send channels values
    def __call__(self, sample):
        # silently pass if connection drops
        try:
            #print(sample.id)
            message = self.clf.add_sample(sample)
            if message != '':
                print(message)
                self.client.send_message(self.address, message)
        except:
            return

    def show_help(self):
        print("""Optional arguments: [ip [port [address]]]
            \t ip: target IP address (default: 'localhost')
            \t port: target port (default: 12345)
            \t address: select target address (default: '/openbci')""")
