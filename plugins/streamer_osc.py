
# requires python-osc
from pythonosc import osc_message_builder
from pythonosc import udp_client
import plugin_interface as plugintypes
from sklearn.lda import LDA
import time

# Use OSC protocol to broadcast data (UDP layer), using "/openbci" stream. (NB. does not check numbers of channel as TCP server)

class Classifier():
    def __init__(self,
                 start_time,    #start time in seconds
                 channels = [0,1,2],
                 num_trials=5,
                 num_rows=6,
                 num_columns=6,
                 flash=0.2,
                 inter_flash=0.1,
                 inter_trial=1,
                 inter_mega_trial=3):
        self.lda = LDA()
        self.fs = 250
        self.started = False
        self.collecting = False
        self.buffer = []
        self.data = []
        self.samples_in_data = num_trials * (num_rows + num_columns) * (flash + inter_flash) * self.fs
        self.samples_since_last = 0
        self.num_samples = 0
        self.channels = channels
        self.start_time = start_time
        self.start_index = None
        self.inter_mega_trial = inter_mega_trial
        self.counter = 0
        #print(start_time)
    def add_sample(self, sample):
        self.counter += 1
        if self.collecting:
            self.data.append(sample.channel_data[self.channels])
            self.num_samples += 1
            if self.num_samples == self.samples_in_data:
                self.reset()
                print(self.counter)
        else:
            self.buffer.append(sample.channel_data[self.channels])
            self.samples_since_last += 1
            if self.started:
                if self.samples_since_last == self.inter_mega_trial * self.fs:
                    self.collecting = True
                    print(self.counter)
            else: 
                if time.time() >= self.start_time:
                    self.started = True
                    self.collecting = True
                    print(self.counter)
    def reset(self):
        self.buffer = self.data[-250*5:]
        self.data = []
        self.samples_since_last = 0
        self.num_samples = 0
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
        
        self.clf = Classifier(time.time() + 5)  #initialize classifier
        print(self.clf.start_time)
    # From IPlugin: close connections, send message to client
    def deactivate(self):
        self.client.send_message("/quit")
        
    # send channels values
    def __call__(self, sample):
        # silently pass if connection drops
        try:
            #print(sample.id)
            self.clf.add_sample(sample)
            self.client.send_message(self.address, sample.channel_data)
        except:
            return

    def show_help(self):
        print("""Optional arguments: [ip [port [address]]]
            \t ip: target IP address (default: 'localhost')
            \t port: target port (default: 12345)
            \t address: select target address (default: '/openbci')""")
