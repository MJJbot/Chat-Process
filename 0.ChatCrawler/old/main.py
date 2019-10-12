import videolist
import video
import sys
startdata = sys.argv[1]

dir = "C:/Users/openk/OneDrive/바탕 화면/SPARK/트위치 다시보기 크롤링/chromedriver/chromedriver.exe"

c1 = ["handongsuk","LCK_Korea","hanryang1125","yapayp30","lol_ambition"]
c2 = ["saddummy","kimdoe","Faker","yumyumyu77","overwatchleague_kr"]
c3 = ["looksam","naseongkim","woowakgood","cocopopp671","2chamcham2"]
c4 = ["kimdduddi","kss7749","ajehr","pacific8815","ddahyoni"]
c5 = ["obm1025","sal_gu","nanajam777","rhdgurwns","so_urf"]
c6 = ["zilioner","jinu6734","jungtaejune","dogswellfish","jammi95"]
c7 = ["alenenwooptv","playhearthstonekr","collet11","beyou0728","silphtv"]
c8 = ["tmxk319","rudbeckia7","sonycast_","xkwhd","sunbaking"]
c9 = ["ch1ckenkun","mister903","nexonkoreaesports","tranth","kangqui"]
c10 = ["h920103","remguri","buzzbean11","nanayango3o","109ace"]

c11 = ["zzamtiger0310","sn400ja","heavyRainism","flurry1989","ses836"]
c12 = ["cherrypach","ok_ja","Funzinnu","teaminven","pjs9073"]
c13 = ["wkgml","dda_ju","mirage720","dlxowns45","drlee_kor"]
c14 = ["tvcrank","kumikomii","nrmtzv","rkdwl12","kanetv8"]
c15 = ["yd0821","steelohs","dkwl025","dingception","yuhwanp"]
c16 = ["team_spiritzero","lucia94","mari0712","qkfhzhal","rooftopcat99"]
c17 = ["gabrielcro","acro_land","moogrr1211","dragon3652","PUBGKorea"]
c18 = ["flowervin","t1_teddy","hwkang2","jmjdoc","rellacast"]
c19 = ["rkdthdus930","dua3362","game2eye","chonana1","cwn222"]
c20 = ["uzuhama","bighead033","jinsooo0","hejin0_0","wlswnwlswn"]

task1 = c1+c6+c11+c16
task2 = c2+c7+c12+c17
task3 = c3+c8+c13+c18
task4 = c4+c9+c14+c19
task5 = c5+c10+c15+c20

print("Input Format: \"C:/Users/openk/OneDrive/바탕 화면/SPARK/chromedriver/chromedriver.exe\"")
dir = './chromedriver'

print("Input Format:\"2019 7 4\"")
date = '2019 6 15'


task = int(startdata)

channels=[]

if(task==1):
    channels = task1
elif(task==2):
    channels = task2
elif(task==3):
    channels = task3
elif(task==4):
    channels = task4
elif(task==5):
    channels = task5
for channel in channels:
    print("----------"+channel+"----------")
    try:
        arr = videolist.get_videolist(dir,channel,date)
    except:
        print("error1")
    try:
        i=1
        for x in arr:
            video.crawl(x,channel)
            print(str(i) + " / " + str(len(arr)))
            i = i+1
        print("----------finish----------")
    except:
        print("error2")
