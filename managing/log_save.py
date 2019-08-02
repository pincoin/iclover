
class UserLogs(object):
    def __init__(self,**kwargs):
        if 'user' in kwargs:
            self.user = kwargs['user']
        if 'url' in kwargs:
            self.url = kwargs['url']
        if 'action' in kwargs:
            self.action = kwargs['action']
        if 'model_name' in kwargs:
            self.model_name = kwargs['model_name']
        if 'model_id' in kwargs:
            self.model_id = kwargs['model_id']
        print(self.__dict__)

class ImageSearchLogs(object):
    def __init__(self,**kwargs):
        if 'user' in kwargs:
            self.user = kwargs['user']
        if 'q' in kwargs:
            self.q = kwargs['q']
        if 'action' in kwargs:
            self.action = kwargs['action']
        if 'model_name' in kwargs:
            self.model_name = kwargs['model_name']
        if 'model_id' in kwargs:
            self.model_id = kwargs['model_id']
        print(self.__dict__)