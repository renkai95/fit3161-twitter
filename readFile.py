import json
with open("harvey.json",'r',encoding='utf-8') as json_file:
    idDict={}
    f= open("harvey_cleaned.json","w+")
    f.write("{")
    for line in json_file:
        data = json.loads(line)
        newDict = {}
        if idDict.get(data['id_str']) is None:
            #print(idDict)
            idDict[data['id_str']]=data['id_str']
            f.write('"'+data['id_str']+'":')
            newDict['created_at']=data['created_at']
            newDict['id_str']=data['id_str']
            newDict['in_reply_to_status_id_str']=data['in_reply_to_status_id_str']
            newDict['in_reply_to_user_id_str']=data['in_reply_to_user_id_str']
            newDict['in_reply_to_screen_name']=data['in_reply_to_screen_name']
            newDict['hashtags']=data['entities']['hashtags']
            newDict['user']={}
            newDict['user']['id_str']=data['user']['id_str']
            newDict['user']['followers_count']=data['user']['followers_count']
            newDict['user']['name']=data['user']['name']
            newDict['retweet_count']=data['retweet_count']
            newDict['favorite_count']=data['favorite_count']
            newDict['full_text']=data['full_text']        
            f.write(json.dumps(newDict))
            f.write("\n,")

    f.write('"last":{}}')
    f.close()
