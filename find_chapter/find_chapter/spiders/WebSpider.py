import scrapy
import pandas as pd
import json
import pprint
from scrapy_splash import SplashRequest

class WebSpider(scrapy.Spider):
    name="webscrap"

    start_urls=[
        'https://bni-india.in/find-a-chapter/'
    ]

    def parse(self,response):
        business_name=response.css('div.wpb_wrapper').css('h5').css('a::text').extract()
        mail_url=response.css('div.wpb_wrapper').css('p').css('strong').css("a::attr('href')").extract()
        name_mob=response.css('div.wpb_wrapper').css('p::text').extract()
        
        chapter=[]
        email=[]
        
        for i in range(0,len(mail_url)):
            if i % 2 == 0:
                email.append(mail_url[i])
            else:
                chapter.append(mail_url[i])
                
        name=[]
        mob=[]
        
        for i in name_mob:
            if i.find('Mr.') == 0:
                name.append(i)
            if i.find('+') == 0:
                mob.append(i)
        
        demo=[]
                
        for i in name_mob:
            if i.find('Mr.') == 0:
                demo.append(i)

        
        data=[]
        
        for i in range(0,len(name)):
            dict1=[business_name[i],name[i],mob[i],email[i],chapter[i]]
            data.append(dict1)
            
        df=pd.DataFrame(data,columns=['Business Name','Name','Phone','Email','Chapter'])
        
        df.to_excel('data.xlsx')
        
        request = scrapy.Request(url="http://bni-gurgaon.in/en-IN/findachapter", dont_filter=True,callback=self.parse_p)
        request.meta['dont_redirect'] = False
        
        yield request
        
               
       
        
    def parse_p(self, response):
        ad_url=response.css('p.legend').css("a::attr('href')").extract()
        request = scrapy.Request(url="http://bni-gurgaon.in/en-IN/"+ad_url[0], dont_filter=True,callback=self.parse_p1)
        request.meta['dont_redirect'] = False
        
        
        yield request

    def parse_p1(self, response):
        request = scrapy.Request(url="http://bni-gurgaon.in/en-IN/chapterlist?chapterName=&chapterCity=&chapterArea=&chapterMeetingDay=&chapterMeetingTime=&regionIds=3906", dont_filter=True,callback=self.parse_p2)
        request.meta['dont_redirect'] = False
        
        data={'chapterName':'','chapterCity':'','chapterArea':'','chapterMeetingDay':'','chapterMeetingTime':'','regionIds':"3906"}
 
        yield SplashRequest(url="http://bni-gurgaon.in/en-IN/chapterlist?chapterName=&chapterCity=&chapterArea=&chapterMeetingDay=&chapterMeetingTime=&regionIds=3906",callback=self.parse_p4,args={'wait':1})

        
        
    def parse_p4(self, response):
        print(response.css('div#chapterList'))    

    def parse_p2(self, response):
        languages = {"availableLanguages":[{"type":"published","url":"http:\/\/bni-gurgaon.in\/en-IN\/chapterlist","descriptionKey":"English (IN)","id":47,"localeCode":"en_IN"}],"activeLanguage":{"id":47,"localeCode":"en_IN","descriptionKey":"English (IN)"}}
        parameters="chapterName=&chapterCity=&chapterArea=&chapterMeetingDay=&chapterMeetingTime=&regionIds=3906"
        languages["availableLanguages"][0]["type"]="published"
        languages["availableLanguages"][0]["url"]="http://bni-gurgaon.in/en-IN/chapterlist"
        languages["availableLanguages"][0]["descriptionKey"]="English (IN)"
        languages["availableLanguages"][0]["id"]="47"
        languages["availableLanguages"][0]["localeCode"]="en_IN"
        languages["activeLanguage"]["id"]="47"
        languages["activeLanguage"]["localeCode"]="en_IN"
        languages["activeLanguage"]["descriptionKey"]="English (IN)"
        pageMode="Live_Site"
        cmsv3="true"
        mappedWidgetSettings='[{"key":74,"name":"Chapter - Region","value":"Chapter - Region"},{"key":75,"name":"City","value":"City"},{"key":76,"name":"Area","value":"Area"},{"key":77,"name":"Meeting Day","value":"Meeting Day"},{"key":78,"name":"Meeting Time","value":"Meeting Time"},{"key":79,"name":"Showing","value":"Showing"},{"key":80,"name":"to","value":"to"},{"key":81,"name":"of","value":"of"},{"key":82,"name":"entries","value":"entries"},{"key":303,"name":"Zero Records","value":"Zero Records"}]'        
          
        data={"parameters":parameters,"""languages["availableLanguages"][0]["type"]""":languages["availableLanguages"][0]["type"],"""languages["availableLanguages"][0]["url"]""":languages["availableLanguages"][0]["url"],"""languages["availableLanguages"][0]["descriptionKey"]""":languages["availableLanguages"][0]["descriptionKey"],"""languages["availableLanguages"][0]["id"]""":languages["availableLanguages"][0]["id"],"""languages["availableLanguages"][0]["localeCode"]""": languages["availableLanguages"][0]["localeCode"],"""languages["activeLanguage"]["id"]""":languages["activeLanguage"]["id"],"""languages["activeLanguage"]["localeCode"]""":languages["activeLanguage"]["localeCode"],"""languages["activeLanguage"]["descriptionKey"]""":languages["activeLanguage"]["descriptionKey"],"pageMode":pageMode,"cmsv3":cmsv3,"mappedWidgetSettings":mappedWidgetSettings}
        
        #scrapy.FormRequest.from_response(response,formdata=data,callback=self.parse_p3)
        yield scrapy.FormRequest('http://bni-gurgaon.in/bnicms/v3/frontend/chapterlist/display',callback=self.parse_p3,formdata={"parameters":"chapterName=&chapterCity=&chapterArea=&chapterMeetingDay=&chapterMeetingTime=&regionIds=3906","languages":languages,"pageMode":pageMode,"cmsv3":cmsv3,"mappedWidgetSettings":mappedWidgetSettings})

        
    def parse_p3(self,response):
        print("done")
        print(response.css("title"))

      
       
