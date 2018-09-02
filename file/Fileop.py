class fileop:
    filename = "d://s.txt"
    file = False
    def create(self):
        self.file = open(self.filename,'w+')

    def write(self):
        print("write")
        if(self.file):
            self.file.write("hellow")
            self.close()
            self.file = False
        else:
            self.create()
            self.write()

    def close(self):
        self.file.close()

    def write(self, content):
        print("write1")
        if(self.file):
            self.file.write(content)
            self.close()
            self.file = False
        else:
            self.create()
            self.write(content)
