import json
import csv
import ntpath
import os
def readFileCsv(inFile,outFile):
    with open(inFile,'r',encoding='utf-8') as json_file:
        dictList=[]
        idDict={}
        
        f= open(outFile,"w+",encoding='utf-8',newline='')
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
                        newDict['in_reply_to_screen_name']=newDict['in_reply_to_screen_name']#.encode(encoding='UTF-8',errors='ignore')  
                    #if len(data['entities']['hashtags'])>0:

                    #    newDict['hashtags']=data['entities']['hashtags'][0]['text']
                    newDict['user_id_str']=data['user']['id_str']
                    newDict['user_followers_count']=data['user']['followers_count']
                    newDict['user_name']=data['user']['name']#.encode(encoding='UTF-8',errors='ignore')
                    newDict['retweet_count']=data['retweet_count']
                    newDict['favorite_count']=data['favorite_count']
                    newDict['full_text']=(data['full_text'].replace('\n',''))#.encode(encoding='UTF-8',errors='ignore')
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
def insertDb(cursor,infile):
    cursor.execute('SET GLOBAL connect_timeout=28800')
    cursor.execute('SET GLOBAL wait_timeout=28800')
    cursor.execute('SET GLOBAL interactive_timeout=28800')
    cursor.execute("""CREATE TABLE `"""+ntpath.basename(infile).split('.')[0]+"""` (
  `id_str` bigint(20) DEFAULT NULL,
  `created_at` text,
  `in_reply_to_status_id_str` text,
  `in_reply_to_user_id_str` text,
  `in_reply_to_screen_name` text,
  `user_id_str` bigint(20) DEFAULT NULL,
  `user_followers_count` int(11) DEFAULT NULL,
  `user_name` text,
  `retweet_count` int(11) DEFAULT NULL,
  `favorite_count` int(11) DEFAULT NULL,
  `full_text` text
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
""")
    cursor.execute("""
    LOAD DATA INFILE '"""+os.path.dirname(os.path.abspath(infile))+'\\\\'+ntpath.basename(infile)+"""' 
    INTO TABLE """+ntpath.basename(infile).split('.')[0]+r""" 
    FIELDS TERMINATED BY ',' 
    ENCLOSED BY '|'
    ESCAPED BY ''
    LINES TERMINATED BY '\r\n'
    IGNORE 1 LINES;
    
    """)
    cursor.execute("commit;")
if __name__=="__main__":
    readFileCsv("../DATA/harvey2days.json","../DATA/harvey2daysoutput.csv")