import sys

class HexString(object):
    # Static variables
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
    __unlikely_opcode_combos = [
        'C3C3','CBCB', 'C3CB', 'CBC3', # RETs
        'E9E9', 'C3E9', 'E9C3',  'CBE9', 'E9CB' # JMPs and RETs
    ]
    __score_range = [-100 + -100 + -75, 100 + 25 + 25]

    def __init__(self, filename):
        # Read in the hex string
        self.hexString = ''
        self.read_file(filename)

        # Initialize score data
        self.scored = False
        self.total_score = 0
        self.scores = {}

    # Read in the file
    def read_file(self, filename):
        with open(filename, 'r') as infile:
            self.hexString = infile.read().upper()
        
    def score_has_opcodes(self):
        '''Assign a score between -100 and 100 based on how many potential
        opcodes could be in the hexstring compared to the average number of 
        opcodes there would be in an instruction sequence of the same length 
        as the hex string'''
        total_opcodes_count = 0
        
        # for each opcode, add up the number of that opcode counted in the string
        for opcode in self.__opcodes:
            for opcode in self.__opcodes[opcode]:
                total_opcodes_count += self.hexString.count(opcode)

        avg_num_instr= len(self.hexString) / 6 
        
        # If the number of counted instructions is within 10% of
        # the average num instructions for hexString
        if avg_num_instr*.8 < total_opcodes_count and \
            total_opcodes_count < 1.2*avg_num_instr:
            self.scores['has_opcodes'] = 100
        # If the number of counted instructions is within between 
        # 10% and 30% of the average num instructions for hexString
        elif avg_num_instr*.7 < total_opcodes_count and \
            total_opcodes_count < 1.3*avg_num_instr:
            self.scores['has_opcodes'] = 50
        # If the number of counted instructions is within between 
        # 50% and 30% of the average num instructions for hexString
        elif avg_num_instr*.5 < total_opcodes_count and \
            total_opcodes_count < 1.5*avg_num_instr:
            self.scores['has_opcodes'] = -50
        # If the number of counted instructions is less than 50 %
        # of the average num instructions for hexString
        else:
            self.scores['has_opcodes'] = -100

        return self.scores['has_opcodes']

    
    def score_has_unlikely_opcode_seq(self):
        '''Assign a score between -100 and 25 based on the frequency of unlikely
        operation combinations, e.g. having two RETs back to back, or two JMPs
        back to back'''
        # Begin with a score of postive 25
        unlikely_combo_score = 25

        # for each unlikely combo found, subtract 50 points from the score
        for unlikely_combo in self.__unlikely_opcode_combos:
            unlikely_combo_score -= self.hexString.count(unlikely_combo)*50

        # Score cannot be lower than -100
        self.scores['unlikely_combos'] = unlikely_combo_score if unlikely_combo_score >= -100 else -100

        return self.scores['unlikely_combos'] 
    
    def score_padding(self):
        '''Assign a score between -75 and 25 based on the amount of padding (00)
        in the file. The more padding, the lower the score'''
        padding_score = 0

        # calculate the amoutn of padding and the ratio of padding to other content
        padding_amount = self.hexString.count('00')
        padding_ratio = padding_amount / float((len(self.hexString)/2))

        # Award score accordingly, more padding = lower score
        if padding_ratio > .75:
            padding_score = -75
        elif padding_ratio > .5:
            padding_score = -25
        else:
            padding_score = 25

        self.scores['padding'] = padding_score
        return self.scores['padding']
        


    def score(self):
        '''Calculate all scores and sum them up'''
        if not self.hexString:
            raise Exception('hexString not initialized')
        else:
            # Call all score functions
            self.score_has_opcodes()
            self.score_has_unlikely_opcode_seq()
            self.score_padding()

            # Sum up scores
            for score_category in self.scores:
                self.total_score += self.scores[score_category]

            self.scored = True
            return self.total_score

    def results_string(self):
        '''Output final decision'''
        if not self.scored:
            # Throw exception if we have not yet scored the string
            raise Exception('hexString has not yet been scored')
        else:
            # If we have a negative total score, then this string has been predicted data
            if self.total_score < 0:
                perc_acc = int(float(self.total_score / float((self.__score_range[0])))*100)
                return 'This is *DATA* with ' + str(perc_acc) + '% confidence per our algorithm'
            # If we have a positive total score, then this string hasbeen predicted instructions
            elif self.total_score >= 0:
                perc_acc = int(float(self.total_score / float((self.__score_range[1])))*100)
                return 'This is *INSTRUCTIONS* with ' + str(perc_acc) + '% confidence per our algorithm'



# Main function
if __name__=='__main__':
    # If they passed in arguments
    if len(sys.argv) > 1:
        for filename in sys.argv[1:]:
            # Iterate over files and score them
            print 'Evaluating Filename:', filename
            hex_string = HexString(filename)
            score = hex_string.score()
            print hex_string.results_string()
            print '------------------------------------------'
    else:
        # Prompt user for file and score
        filename = raw_input('What is the filename with the hex string in question: ')
        hex_string = HexString(filename)
        score = hex_string.score()
        print hex_string.results_string()
        

