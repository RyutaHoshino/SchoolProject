import pandas
from random import choice,randint
from datetime import datetime
list_data = [(choice(['S','A','B','C','D']), datetime.fromtimestamp(randint(1485874800, 1487754616))) for i in range(100)]
df = pandas.DataFrame(list_data, columns=['rank', 'datetime'])
df
