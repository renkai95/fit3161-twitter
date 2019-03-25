import json
with open("irma.json",'r',encoding='utf-8') as json_file:
    idDict={}
    f= open("irma_cleaned.json","w+")
    f.write("{")
    for line in json_file:
        data = json.loads(line)
        newDict = {}
        if idDict.get(data['id_str']) is None:
            #print(idDict)
            idDict[data['id_str']]=data['id_str']
            f.write('"'+data['id_str']+'":')
            newDict['created_at']=data['created_at']
            #newDict['id_str']=data['id_str']
            newDict['in_reply_to_status_id_str']=data['in_reply_to_status_id_str']
            newDict['in_reply_to_user_id_str']=data['in_reply_to_user_id_str']
            newDict['in_reply_to_screen_name']=data['in_reply_to_screen_name']
            if len(data['entities']['hashtags'])>0:

                newDict['hashtags']=data['entities']['hashtags'][0]['text']
            newDict['user_id_str']=data['user']['id_str']
            newDict['user_followers_count']=data['user']['followers_count']
            newDict['user_name']=data['user']['name']
            newDict['retweet_count']=data['retweet_count']
            newDict['favorite_count']=data['favorite_count']
            newDict['full_text']=data['full_text']        
            f.write(json.dumps(newDict))
            f.write(",\n")

    f.write('"last":{}}')
    f.close()
