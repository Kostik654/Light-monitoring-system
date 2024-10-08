

class PortItem:
    def __init__(self, port_: int, service_name_: str, excepted_codes_: list[int] = None):
        self.Port = port_
        self.ServiceName = service_name_
        self.ExceptedCodes = excepted_codes_
