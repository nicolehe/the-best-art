import random

bads = ['atrocious', 'awful', 'cheap', 'crummy',
        'dreadful', 'lousy', 'poor', 'rough', 'sad',
        'unacceptable', 'incorrect', 'not good', 'off',
        'raunchy', 'harmful', 'immoral', 'dangerous',
        'unhealthy', 'wrong', 'evil', 'mean', 'terrible',
        'bad', 'villainous', 'wicked', 'vile', 'despicable',
        'disgusting', 'horrible', 'criminal', 'delinquent',
        'appalling', 'cruel', 'heinous', 'horrendous', 'lousy',
        'nasty', 'shameful', 'ungodly', 'repulsive', 'offensive',
        'loathsome', 'mean', 'terrifying', 'abominable']

for i in range(100):
    random.shuffle(bads)
    for bad in bads:
        print "Trucks are " + bad + ". " ,
