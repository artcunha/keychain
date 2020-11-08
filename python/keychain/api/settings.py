

class Settings(object):
    def __init__(self, settings):
        self.__dict__ = settings

    def items(self):
        return self.__dict__.items()
    
    def as_dict(self):
        return self.__dict__
        
st = Settings({"a":0})
st.a = 1
