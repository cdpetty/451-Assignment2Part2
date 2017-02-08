import sys

class HexString(object):
    __opcodes = { 
        'ADD': ['00', '01', '02', '03', '04', '05'],
        'PUSH': ['06'], 
        'POP': ['07'],
        'CALL': ['9A'], 
        'CMP': ['38', '39', '3A', '3B', '3C', '3D'],
        'MOV': ['88, 89', '8A', '8B', '8C', '8E'],
        'LEA': ['8D'],
        'TEST': ['84', '85', 'A8', 'A9']
    }

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
        
    def score_has_opcodes(self):
        print self.hexString.count('00')
        print self.hexString
        if not self.hexString:
            raise Exception('hexString not initialized')
        else:
            total_opcodes_count = 0
            for opcode in self.__opcodes:
                for opcode in self.__opcodes[opcode]:
                    total_opcodes_count += self.hexString.count(opcode)

            avg_num_instr= len(self.hexString) / 6 

            percentage_ranges = [.9, .8, .5, .2]
            
            for percentage in percentage_ranges:
                if avg_num_instr*percentage < total_opcodes_count and total_opcodes_count < (1 - percentage + 1)*avg_num_instr:
                    self.scores['has_opcodes'] = percentage*100
                    break

            print 'Score:', self.scores['has_opcodes']
            print 'avg_num_instructions:', avg_num_instr
            print 'num opcodes:', total_opcodes_count
            
                    






if __name__=='__main__':
    filename = raw_input('What is the filename with the hex string in question: ')

    hex_string = HexString(filename)
    hex_string.score_has_opcodes()
    

