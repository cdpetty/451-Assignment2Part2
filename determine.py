import sys

class HexString(object):
    __opcodes = { 
        'ADD': ['00', '01', '02', '03', '04', '05'],
        'PUSH': ['06'], 
        'POP': ['07'],
        'CALL': ['9A'], 





    def __init__(self, filename):
        # Read in the hex string
        self.hexString = ''
        self.read_file(filename)

        # Initialize score data
        self.total_score = 0
        self.scores = {}

    def read_file(self, filename):
        with open(filename, 'r') as infile:
            self.hexString = infile.read()
        
    def 





if __name__=='__main__':
    filename = raw_input('What is the filename with the hex string in question: ')

    hex_string = HexString(filename)
    

