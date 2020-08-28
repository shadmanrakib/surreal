f = open('data.csv')
data = f.read()
f.close()

data = data.split('\n')[1:-1]

sep_data = []
for row in range(len(data)):
    sep_data.append(data[row].split(','))

data = sep_data

def low_to_high(d):
    return sorted(d, key=lambda x: float(x[2]), reverse=False)
def high_to_low(d):
    return sorted(d, key=lambda x: float(x[2]), reverse=True)
def alphabetical(d):
    return sorted(d, key=lambda x: x[0], reverse=False)
def reversed_alphabetical(d):
    return sorted(d, key=lambda x: x[0], reverse=True)

def store(d):
    return (for x 
