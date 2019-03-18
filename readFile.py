import json
with open("harvey.json",'r',encoding='utf-8') as json_file:
    f= open("harvey_cleaned.json","w+")
    f.write("{")
    for line in json_file:
        data = json.loads(line)
        newDict = {}
        newDict['created_at']=data['created_at']
        newDict['id_str']=data['id_str']
        newDict['in_reply_to_status_id_str']=data['in_reply_to_status_id_str']
        newDict['in_reply_to_user_id_str']=data['in_reply_to_user_id_str']
        newDict['in_reply_to_screen_name']=data['in_reply_to_screen_name']
        newDict['entities']=data['entities']
        newDict['user']={}
        newDict['user']['followers_count']=data['user']['followers_count']
        newDict['user']['name']=data['user']['name']
        newDict['retweet_count']=data['retweet_count']
        newDict['favorite_count']=data['favorite_count']
        newDict['full_text']=data['full_text']        
        f.write(json.dumps(newDict))
        f.write("\n,")

    f.write("{}}")
    f.close()
