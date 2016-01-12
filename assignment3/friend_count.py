import MapReduce
import sys

mr = MapReduce.MapReduce()

def mapper(record):
    personA = record[0]
    mr.emit_intermediate(personA, 1)

def reducer(key, list_of_values):
    total = 0
    for amount in list_of_values:
      total += amount
    mr.emit((key, total))

if __name__ == '__main__':
    inputdata = open(sys.argv[1])
    mr.execute(inputdata, mapper, reducer)
