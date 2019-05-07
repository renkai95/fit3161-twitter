import json
import csv
with open("../DATA/irma.json",'r',encoding='utf-8') as json_file:
    dictList=[]
    idDict={}
    
    f= open("../DATA/irma_cleaned.csv","w+",encoding='utf-8',newline='')
    #f.write("{")
    for line in json_file:

        try:
            data = json.loads(line)
            if idDict.get(data['id_str']) is None:
                newDict={}
                idDict[data['id_str']]=data['id_str']
                #f.write('"'+data['id_str']+'":')
                newDict['id_str']=data['id_str']
                newDict['created_at']=data['created_at']
            
                newDict['in_reply_to_status_id_str']=data['in_reply_to_status_id_str']
                newDict['in_reply_to_user_id_str']=data['in_reply_to_user_id_str']
                #print(data)
                
                newDict['in_reply_to_screen_name']=data['in_reply_to_screen_name']
                if newDict['in_reply_to_screen_name']:
                    newDict['in_reply_to_screen_name']=newDict['in_reply_to_screen_name'].encode(encoding='UTF-8',errors='ignore')  
                #if len(data['entities']['hashtags'])>0:

                #    newDict['hashtags']=data['entities']['hashtags'][0]['text']
                newDict['user_id_str']=data['user']['id_str']
                newDict['user_followers_count']=data['user']['followers_count']
                newDict['user_name']=data['user']['name'].encode(encoding='UTF-8',errors='ignore')
                newDict['retweet_count']=data['retweet_count']
                newDict['favorite_count']=data['favorite_count']
                newDict['full_text']=(data['full_text'].replace('\n','')).encode(encoding='UTF-8',errors='ignore')
                dictList.append(newDict)     
                #f.write(json.dumps(newDict))
                #f.write(",\n")
                #f.write("\n")
        except:
            print("")
    #f.write('"last":{}}')
    #print(dictList[0])
    csv_columns=list(dictList[0].keys())
    writer = csv.DictWriter(f, fieldnames=csv_columns,quotechar='|',delimiter=',')
    writer.writeheader()
    for data in dictList:
        #print(data)
        writer.writerow(data)
    f.close()
