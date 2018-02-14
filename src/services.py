class DataService:
    def read_data(self):
        return "read data"

    def write_data(self, data_to_write):
        raise Exception("no real service to write to")


class LiveDataService(DataService):
    def read_data(self):
        return "live data read"

    def write_data(self, data_to_write):
        return "wrote live data " + data_to_write


class FakeDataService(DataService):
    def __init__(self):
        pass

    def read_data(self):
        return "fake read data"

    def write_data(self, data_to_write):
        return "fake write data"
