from selenium import webdriver
import codecs




def get_videolist(dir, channel, date):
    chromedriver_dir = dir

    start_url = "https://www.twitch.tv/"+channel+"/videos?filter=archives&sort=time"

    # Start
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('lang=ko_KR')
    chrome_options.add_argument('--no-sandbox') # required when running as root user. otherwise you would get no sandbox errors. 
    driver = webdriver.Chrome(chromedriver_dir, chrome_options=chrome_options)
    driver.implicitly_wait(3)
    #file = codecs.open("output.txt", "a", encoding="utf-8")
    driver.get(start_url)
    videos = driver.find_elements_by_xpath("""//a[@data-test-selector="preview-card-titles__primary-link"]""")

    #months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
    y = int(date.split()[0])
    m = int(date.split()[1])
    d = int(date.split()[2])

    dates = driver.find_elements_by_xpath("""//img[@data-test-selector="preview-card-thumbnail__image-selector"]""")
    num=0
    for i in dates:
        x = i.get_attribute("title").split()
        yy = int(x[0].rstrip('년'))
        mm = int(x[1].rstrip('월'))
        dd = int(x[2].rstrip('일'))
        
        if y<yy:
            num = num+1
            
        elif y==yy:
            if m < mm:
                num = num+1
                
            elif m == mm:
                if d <= dd:
                    num = num+1
                    

    videolist = []
    
    #f = open(channel+" videolist.txt","w",encoding="utf-8")
    i=0
    for video in videos:
        videolist.append(video.get_attribute("href")[29:38])       
        if i == num:
            break
        i=i+1

    driver.quit()
    return videolist
