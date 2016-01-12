import MapReduce
import sys

mr = MapReduce.MapReduce()


# Assume matrix sizes from the sample JSON data
# A is MxK matrix, whereas B is KxN one
M = 5
K = 5
N = 5

def mapper(record):
    matrix_origin, row, column, value = record
    for n in range(N):
        if matrix_origin == 'a':
            destination_cell = (row, n)
            serial_number = column
        else:
            destination_cell = (n, column)
            serial_number = row
        mr.emit_intermediate(destination_cell, (matrix_origin, serial_number, value))

def reducer(key, list_of_values):
    print(key ,list_of_values)
    left_matrix_values = [(item[1], item[2]) for item in list_of_values if item[0] == 'a']
    right_matrix_values = [(item[1], item[2]) for item in list_of_values if item[0] == 'b']

    result = 0
    for left_values in left_matrix_values:
        for right_values in right_matrix_values:
            if left_values[0] == right_values[0]:
                result += left_values[1] * right_values[1]
    mr.emit((key[0], key[1], result))

if __name__ == '__main__':
    inputdata = open(sys.argv[1])
    mr.execute(inputdata, mapper, reducer)
