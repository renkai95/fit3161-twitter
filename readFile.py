import json
with open("irma.json",'r',encoding='utf-8') as json_file:
    f= open("irma_cleaned.json","w+")
    for line in json_file:
        data = json.loads(line)
        #print(json.dumps(data,indent=4,sort_keys=True))
        newDict = {}
        newDict['created_at']=data['created_at']
        newDict['id_str']=data['id_str']
        newDict['in_reply_to_status_id_str']=data['in_reply_to_status_id_str']
        newDict['in_reply_to_user_id_str']=data['in_reply_to_user_id_str']
        newDict['in_reply_to_screen_name']=data['in_reply_to_screen_name']
        newDict['entities']=data['entities']
        #print(json.dumps(data['user'],indent=4,sort_keys=True))

        newDict['user']={}
        newDict['user']['followers_count']=data['user']['followers_count']
        
        newDict['user']['name']=data['user']['name']
        #newDict['quoted_status_id_str']=data['quoted_status_id_str']
        #newDict['is_quote_status']=data['is_quote_status']
        newDict['retweet_count']=data['retweet_count']
        newDict['favorite_count']=data['favorite_count']
        newDict['full_text']=data['full_text']
        
        f.write(json.dumps(newDict))
        #print(newDict)
        #print(data['created_at'])
    f.close()
