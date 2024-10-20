

class JobManagerDefaults:

    def __init__(self):

        # defaults in secs
        self.sip_timeout_default = 15
        self.curl_timeout_default = 5
        self.mongo_timeout_default = 5
        self.socket_timeout_default = 5

        self.sip_interval_default = 60
        self.curl_interval_default = 60
        self.mongo_interval_default = 60
        self.socket_interval_default = 60
