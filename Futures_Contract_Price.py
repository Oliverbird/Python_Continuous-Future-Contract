from urllib.request import urlopen as uReq
from urllib.request import Request
from bs4 import BeautifulSoup as soup
import re
import datetime

#Create a CME futures contracts list where putting the futures contractc specifications
ListName = "Future contracts URLs list"
OpenList = open(ListName,"r")

#Create a csv file includes the headers
filename = "Futures contracts infomation.csv"
OpenFile= open(filename,"w")
headers = "Futures Contracts,Base Symbols,Catogory,Time Zone,Start Day,Start Time,End Day,End Time,Halt Days,Halt Start Time,Halt End Time" + "\n"
OpenFile.write(headers)

#Number of websites want to scrap
n=int(OpenList.readline())

#Looping through the websites in the list
try:
    for num in range(n):

        #Call the list and read the websites line by line
        theList=OpenList.readline()

        #Get the website access and create a BeautifulSoup4 object
        AccessCME=Request(theList,headers={"User-Agent":"Mozilla/5.0"})
        CMEPage=uReq(AccessCME).read()
        page_soup=soup(CMEPage,"html.parser")

        ####Start to extract data####

        #FuturesContracts
        cme=page_soup.find("div",{"class":"cmeProduct section"})
        FuturesContracts=cme.span.text.strip()

        #BaseSymbol
        possible_tds=page_soup.find_all('td',attrs={'class':"prodSpecAtribute"})
        try:
            if possible_tds:
                parent_td=[td for td in possible_tds if 'Product' in td.text][0]
                target = parent_td.fetchNextSiblings('td')[0].text.strip()
                #Remove the unnecessary texts
                first_take=re.sub('CME Globex:\s', '', target)
                BaseSymbol=re.sub('CME ClearPort:.*', '', first_take)

        except:
                print('Found an error\nDoes't find the symbol of "+str(FuturesContracts)\n"Please remove the Url of "+str(FuturesContracts) +' from the text file and delete the row of '+str(FuturesContracts)+' from the CSV file'')
                # print("Does't find the symbol of "+str(FuturesContracts))
                # print("Please remove the Url of "+str(FuturesContracts) +' from the text file and delete the row of '+str(FuturesContracts)+' from the CSV file'+'\n')

        #Catogory
        Urls=str(page_soup.find('link')).split('/')
        Catogory=Urls[4].upper()

        #The whole description of trading hours
        possible_tds=page_soup.find_all('td',attrs={'class':'prodSpecAtribute'})
        parent_td=[td for td in possible_tds if 'Trading' in td.text][0]
        #Some of the trading hours is in the next tag
        if 'CME Globex:'== parent_td.fetchNextSiblings('td')[0].text:
                Target=parent_td.fetchNextSiblings('td')[1].text
        else:
                Target=parent_td.fetchNextSiblings('td')[0].text
                Target=re.sub('CME Globex:\s', '', Target)
        TradingHours=re.sub('\n.*', "",Target)
        #Standardized the data
        TradingHours=TradingHours.replace("SUN","SUNDAY").replace("FRI:","FRIDAY").replace('a.m.','AM').replace('p.m.','PM').replace(",","")

            #Spliting Trading hours into a list
        TradingHours_list=TradingHours.upper().split(" ")

            #Splitting trading hours to Start days,Start time, End day
        Start_day=TradingHours_list[0]
        Start_time=TradingHours_list[3]+" "+TradingHours_list[4].replace('P.M.','PM')
        End_day=TradingHours_list[2]

            #Splitting the Halt start timie, Halt end time, and Time zone
        a='12:00:00 AM'
        b=datetime.datetime.strptime(a,'%I:%M:%S %p')+datetime.timedelta(seconds=-1)
        c=b.strftime('%I:%M:%S %p')
        Halt_days='Sun (Mon) (Tue) (Wed) (Thur) (Fri) Sat'

        if Category =='AGRICULTURAL':
            Time_zone=TradingHours_list[8]

            End_time=TradingHours_list[16]+' '+TradingHours_list[17]

            Halt_start_time=a+'  '+('('+TradingHours_list[6]+" "+TradingHours_list[7]+'|'+TradingHours_list[16]+" "+TradingHours_list[17]+')'+'  ')*5+'  '+ a

            #830am-1(s)
            Halt_end_time_1=TradingHours_list[13]+" "+TradingHours_list[14]
            Halt_end_time_2=datetime.datetime.strptime(Halt_end_time_1,'%I:%M %p')+datetime.timedelta(seconds=-1)
            Halt_end_Time_3=Halt_end_time_2.strftime('%I:%M:%S %p')
            #7pm-1(s)
            Halt_end_time_4=TradingHours_list[3]+" "+TradingHours_list[4]
            Halt_end_time_5=datetime.datetime.strptime(Halt_end_time_4,'%I:%M %p')+datetime.timedelta(seconds=-1)
            Halt_end_Time_6=Halt_end_time_5.strftime('%I:%M:%S %p')
            Halt_end_Time=Halt_end_Time_6+'  '+('('+Halt_end_Time_3+'|'+Halt_end_Time_6+')'+'  ')*4+'('+Halt_end_Time_3+'|'+c+')'+'  '+c

        if Category =='ENERGY':
            if TradingHours_list[27] == 'CT)':
                Time_zone='ET'

                End_time=TradingHours_list[6]+' '+TradingHours_list[7]

                Halt_start_time=a+'  '+('('+TradingHours_list[6]+" "+TradingHours_list[7]+')'+'  ')*5+'  '+ a

                Halt_end_time_1=TradingHours_list[3]+" "+TradingHours_list[4]
                Halt_end_time_2=datetime.datetime.strptime(Halt_end_time_1,'%I:%M %p')+datetime.timedelta(seconds=-1)
                Halt_end_Time_3=Halt_end_time_2.strftime('%I:%M:%S %p')
                Halt_end_Time=Halt_end_Time_3+'  '+('('+Halt_end_Time_3+')'+'  ')*4+'('+c+')'+'  '+c

        if Category =='EQUITY-INDEX':
            if TradingHours_list[10]=='(ET)':
                Time_zone='ET'

                End_time=TradingHours_list[6]+' '+TradingHours_list[7]
                d='4:15 PM'
                e='4:29:59 PM'
                Halt_start_time=a+'  '+('('+ d +'|'+TradingHours_list[6]+" "+TradingHours_list[7]+')'+'  ')*5+'  '+ a

                Halt_end_time_1=TradingHours_list[3]+" "+TradingHours_list[4]
                Halt_end_time_2=datetime.datetime.strptime(Halt_end_time_1,'%I:%M %p')+datetime.timedelta(seconds=-1)
                Halt_end_Time_3=Halt_end_time_2.strftime('%I:%M:%S %p')

                Halt_end_Time=Halt_end_Time_3+'  '+('('+ e +'|'+Halt_end_Time_3+')'+'  ')*4+'('+ e + "|" + c +')'+'  '+c

        if Category =='FX':
            if TradingHours_list[8]=='CT':
                Time_zone=TradingHours_list[8]
            else:
                Time_zone='ET'

            End_time=TradingHours_list[6]+' '+TradingHours_list[7]

            Halt_start_time=a+'  '+('('+TradingHours_list[6]+" "+TradingHours_list[7]+')'+'  ')*5+'  '+ a

            Halt_end_time_1=TradingHours_list[3]+" "+TradingHours_list[4]
            Halt_end_time_2=datetime.datetime.strptime(Halt_end_time_1,'%I:%M %p')+datetime.timedelta(seconds=-1)
            Halt_end_Time_3=Halt_end_time_2.strftime('%I:%M:%S %p')
            Halt_end_Time=Halt_end_Time_3+'  '+('('+Halt_end_Time_3+')'+'  ')*4+'('+c+')'+'  '+c

        if Category =='INTEREST-RATES':
            if TradingHours_list[3] =='5:00':
                Time_zone='CT'
            else:
                Time_zone='ET'

            End_time=TradingHours_list[6]+' '+TradingHours_list[7]

            Halt_start_time=a+'  '+('('+TradingHours_list[6]+" "+TradingHours_list[7]+')'+'  ')*5+'  '+ a

            Halt_end_time_1=TradingHours_list[3]+" "+TradingHours_list[4]
            Halt_end_time_2=datetime.datetime.strptime(Halt_end_time_1,'%I:%M %p')+datetime.timedelta(seconds=-1)
            Halt_end_Time_3=Halt_end_time_2.strftime('%I:%M:%S %p')
            Halt_end_Time=Halt_end_Time_3+'  '+('('+Halt_end_Time_3+')'+'  ')*4+'('+c+')'+'  '+c

        if Category =='METALS':
            if TradingHours_list[3]=='6:00':
                Time_zone='ET'
            End_time=TradingHours_list[6]+' '+TradingHours_list[7]

            Halt_start_time=a+'  '+('('+TradingHours_list[6]+" "+TradingHours_list[7]+')'+'  ')*5+'  '+ a

            Halt_end_time_1=TradingHours_list[3]+" "+TradingHours_list[4]
            Halt_end_time_2=datetime.datetime.strptime(Halt_end_time_1,'%I:%M %p')+datetime.timedelta(seconds=-1)
            Halt_end_Time_3=Halt_end_time_2.strftime('%I:%M:%S %p')
            Halt_end_Time=Halt_end_Time_3+'  '+('('+Halt_end_Time_3+')'+'  ')*4+'('+c+')'+'  '+c

        #Write data to CSV file
        OpenFile.write(FuturesContracts + "," + BaseSymbol + "," + Catogory + ',' + Time_zone + ","+ Start_day + ","+ Start_time + "," + End_day + "," + End_time + ',' + Halt_days+',' + Halt_start_time+','+ Halt_end_Time +"\n")
        print(num)
        print(FuturesContracts + '\n')

except:
    print('Finished. Go through the output above to see if there are any errors.')

OpenFile.close
OpenList.close