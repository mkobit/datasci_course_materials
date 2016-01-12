import MapReduce
import sys

mr = MapReduce.MapReduce()

def mapper(record):
    document_id = record[0]
    text = record[1]
    words = text.split()
    for word in words:
      mr.emit_intermediate(word, document_id)

def reducer(key, list_of_values):
    mr.emit((key, list(set(list_of_values))))

if __name__ == '__main__':
    inputdata = open(sys.argv[1])
    mr.execute(inputdata, mapper, reducer)
