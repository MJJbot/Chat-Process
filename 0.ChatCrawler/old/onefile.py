
channellist1 = ["handongsuk","LCK_Korea","hanryang1125","yapayp30","lol_ambition"]
channellist2 = ["saddummy","kimdoe","Faker","yumyumyu77","overwatchleague_kr"]
channellist3 = ["looksam","naseongkim","woowakgood","cocopopp671","2chamcham2"]
channellist4 = ["kimdduddi","kss7749","ajehr","pacific8815","ddahyoni"]
channellist5 = ["obm1025","sal_gu","nanajam777","rhdgurwns","so_urf"]
channellist6 = ["zilioner","jinu6734","jungtaejune","dogswellfish","jammi95"]
channellist7 = ["alenenwooptv","playhearthstonekr","collet11","beyou0728","silphtv"]
channellist8 = ["tmxk319","rudbeckia7","sonycast_","xkwhd","sunbaking"]
channellist9 = ["ch1ckenkun","mister903","nexonkoreaesports","tranth","kangqui"]
channellist10 = ["h920103","remguri","buzzbean11","nanayango3o","109ace"]

channellist11 = ["zzamtiger0310","sn400ja","heavyRainism","flurry1989","ses836"]
channellist12 = ["cherrypach","ok_ja","Funzinnu","teaminven","pjs9073"]
channellist13 = ["wkgml","dda_ju","mirage720","dlxowns45","drlee_kor"]
channellist14 = ["tvcrank","kumikomii","nrmtzv","rkdwl12","kanetv8"]
channellist15 = ["yd0821","steelohs","dkwl025","dingception","yuhwanp"]
channellist16 = ["team_spiritzero","lucia94","mari0712","qkfhzhal","rooftopcat99"]
channellist17 = ["gabrielcro","acro_land","moogrr1211","dragon3652","PUBGKorea"]
channellist18 = ["flowervin","t1_teddy","hwkang2","jmjdoc","rellacast"]
channellist19 = ["rkdthdus930","dua3362","game2eye","chonana1","cwn222"]
channellist20 = ["uzuhama","bighead033","jinsooo0","hejin0_0","wlswnwlswn"]



channellist = channellist1+channellist2+channellist3+channellist4+channellist5+channellist6+channellist7+channellist8+channellist9+channellist10+channellist11+channellist12+channellist13+channellist14+channellist15+channellist16+channellist17+channellist18+channellist19+channellist20
mainfile = "chatting_1to100.txt"
output = open(mainfile,'w',encoding='UTF-8')
for i in channellist:
    print(i)
    try:
        videofile = i+".txt"
        input = open(videofile,'r',encoding='UTF-8')
        txt = input.readlines()
        for k in range(len(txt)):
            line = txt[k]
            output.write(line+'\n')
        output.write('\n')
        

        input.close()

    except:
        continue


output.close()