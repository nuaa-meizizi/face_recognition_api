import json
class Result(object) :
    return_data = {}
    def __init__(self):
        print '...'
    @classmethod
    def success(self,data = ''):
        self.return_data['code']=0
        if data != '' : self.return_data['data'] = data
        return self.send()
    @classmethod
    def error(self,msg = '',code  = 1):
        self.return_data['code'] = code
        if msg !='': self.return_data['msg'] = msg
        return self.send()
    @classmethod
    def send(self):
      #  header('Content-type: application/json; charset=utf-8')
    #    !self.return_data && self.return_data = []
        print 'send',json.dumps(self.return_data)
        return json.dumps(self.return_data)


