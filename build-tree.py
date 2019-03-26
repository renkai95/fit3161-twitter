
6
7
8
9
10
11
12
13
14
15
 
import ijson
 
 
def parse_json(json_filename):
    with open(json_filename, 'rb') as input_file:
        # load json iteratively
        parser = ijson.parse(input_file)
        for prefix, event, value in parser:
            print('prefix={}, event={}, value={}'.format(prefix, event, value))
 
 
if __name__ == '__main__':
    parse_json('../DATA/irma_cleaned.json')