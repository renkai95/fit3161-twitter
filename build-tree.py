import csv
harvey_id={}
replied_to={}
replied_to_id={}

with open('../DATA/harvey_ids.csv') as inputFile:
    for row in inputFile:
        harvey_id[row]=''
    f = open('../DATA/harvey_replies.csv')
    for row in f:
        temp=row.split(',')
        replied_to[temp[1]]=''
        replied_to_id[temp[0]]=''
    f.close()
repliesFound=0
for k in replied_to:
    try: 
        harvey_id[k]
        repliesFound+=1
    except KeyError:
        pass

print(repliesFound)
print(len(harvey_id))