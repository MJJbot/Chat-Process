import requests 
import json
import sys
import re


def get_html(url):
    _html = ""
    resp = requests.get(url)
    if resp.status_code == 200:
        _html = resp.text
    return _html

def doubleDigit(num):
    if num < 10 :
        return '0'+str(num)
    else:
        return str(num)


def crawl(v_id,channel):
    
        
    if sys.version_info[0] == 1:
        reload(sys)
        sys.setdefaultencoding('utf-8')
    
    
    videoId = v_id
    clientId = "2wfgpbv6m25wyog31zy6q7ubkazlpr"
    

    chat = []
    user = []
    
    nextCursor = ''
    
    params = {}
    params['client_id'] = clientId

    i = 0
    
    while True :
        if i == 0 :
            URL = 'https://api.twitch.tv/v5/videos/'+videoId+'/comments?content_offset_seconds=0' 
            i += 1
        else:
            URL = 'https://api.twitch.tv/v5/videos/'+videoId+'/comments?cursor=' 
            URL +=  nextCursor   
            
       
        
        response = requests.get(URL, params=params)
        
        j = json.loads(response.text)
        
        for k in range(0,len(j["comments"])):
            # timer = j["comments"][k]["content_offset_seconds"]
            
            # timeMinute = int(timer/60)
            
            # if timeMinute >= 60 :
            #     timeHour = int(timeMinute/60)
            #     timeMinute %= 60
            # else :
            #     timeHour = int(timeMinute/60)
    
            # timeSec = int(timer%60)
            
            if(j["comments"][k]["commenter"]["display_name"]!="싹둑" and j["comments"][k]["commenter"]["display_name"]!="Nightbot"):
                # time.append(doubleDigit(timeHour)+':'+doubleDigit(timeMinute)+':'+doubleDigit(timeSec))
                user.append(j["comments"][k]["commenter"]["display_name"])
                chat.append(j["comments"][k]["message"]["body"])
       
        if '_next' not in j:
            break
        
        nextCursor = j["_next"]
            
    
    f = open(channel+".txt", 'at', encoding='UTF8')
    for x in range(0, len(chat)):
        '''f.write('[')
        f.write(str(time[x]))
        f.write(']')
        f.write(' ')
        f.write('<')'''
        f.write(str(user[x]))
        f.write('\t')
        f.write(str(chat[x]))
        f.write("\n")
            
    f.write("\n")
    f.close()

if __name__ == "__main__":
    crawl(sys.argv[1])
