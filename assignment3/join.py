import MapReduce
import sys

mr = MapReduce.MapReduce()

def mapper(record):
    table = record[0]
    order_id = record[1]
    mr.emit_intermediate(order_id, record)

def reducer(key, list_of_values):
    orders = [item for item in list_of_values if item[0] == u'order']
    for order in orders:
        for line_item in [item for item in list_of_values if item[0] == u'line_item']:
            joined = list(order)
            joined.extend(line_item)
            mr.emit(joined)

if __name__ == '__main__':
    inputdata = open(sys.argv[1])
    mr.execute(inputdata, mapper, reducer)
