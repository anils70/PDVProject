import sys
print(sys.version)

table_1=[[1,2,3],[4,5,6]]
#print(len(table_1), 'breadth:',len(table_1[0]))

#for i in range(1,4):
#    if i in table_1:
#        print('found ', i)
idx = 0
test_dict = {}
for row in table_1:
    lis = [row[i] for i in range(len(row)) if i != idx]
    test_dict[row[idx]]= lis

print(test_dict)
