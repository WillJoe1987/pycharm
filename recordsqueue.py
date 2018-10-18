class recordsqueue:

    topsize = 100
    recordslist = []

    def get_size(self):
        return self.recordslist.__len__()

    def push(self, record = None):
        if(record == None):
            return self.get_size()
        else:
            if(self.recordslist.__len__() >= self.topsize):
                self.recordslist.pop()
            self.recordslist.insert(0,record)
            return self.get_size()

    def get_by_index(self, index = 0):
        if index>=0&index<self.get_size():
            return self.recordslist[index]

    def format_msg(self, msg):
        return msg

    def grid(self):
        len = self.get_size()
        result = ''
        for i in range(len):
            result = result + '\n' + str(self.get_by_index(len - i -1))
        return result


if __name__ == '__main__':
    rs = recordsqueue()
    rs.push(1)
    rs.push('2')
    rs.push([])
    print(rs.grid())
    for i in range(97):
        rs.push('['+str(i)+']')
    print(rs.grid())
    for i in range(23):
        rs.push('[' + str(i) + 'asd]')
    print(rs.grid())