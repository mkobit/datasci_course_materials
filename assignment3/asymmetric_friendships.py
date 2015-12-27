import MapReduce
import sys

mr = MapReduce.MapReduce()

def mapper(record):
    personA = record[0]
    personB = record[1]
    mr.emit_intermediate((personA, personB), 1)
    mr.emit_intermediate((personB, personA), 1)

def reducer(key, list_of_values):
    total = 0
    for v in list_of_values:
      total += v
    if total < 2:
        mr.emit(tuple(key))

if __name__ == '__main__':
    inputdata = open(sys.argv[1])
    mr.execute(inputdata, mapper, reducer)
