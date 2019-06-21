import scrapy
from scrapy_splash import SplashRequest
import pandas as pd
import re


class SplashSpider(scrapy.Spider):
    name = "jsscraper"
    cha_i=0
    data=[]
    start_urls = ["http://bni-gurgaon.in/en-IN/chapterlist?chapterName=&chapterCity=&chapterArea=&chapterMeetingDay=&chapterMeetingTime=&regionIds=3906"]

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url=url, callback=self.parse,args={"wait":3})

    def parse(self, response):
        
        link=response.css("a.linkone").css("a::attr(href)").extract()   
        self.chapter=response.css("a.linkone").css("a::text").extract()  
        
        for i in range(0,len(link)):
            cha_i=i
            request = SplashRequest(url="http://bni-gurgaon.in/en-IN/"+link[i], callback=self.parse_p1,args={"wait":3})
            yield request
            
    def parse_p1(self, response):
        link=response.css("a.linkone").css("a::attr(href)").extract()  
        member_name=response.css("a.linkone").css("a::text").extract()
        
   

        for i in range(0,len(link)):
            request = SplashRequest(url="http://bni-gurgaon.in/en-IN/"+link[i], callback=self.parse_p2,args={"wait":3})
            yield request
            
        self.df=pd.DataFrame(self.data,columns=['State','City','Chapters','Members Names','Business Name','Profession/Speciality','Phone','Direct','Mobile','CompanyWebsite','Address','My Business Text','Idea Referral','My ideal referral partner','Top product'])

        self.df.to_excel('data.xlsx')
  
            
    def parse_p2(self, response):      
        member_name1=response.css("div.rowProfileDetail").css("div").css("h2::text").extract()
        
        member_name=""
        try:
            member_name=member_name1[0]
        except:
            print "error"
        
        profession_speciality="" 
        try:
            profession_speciality=response.css("div.rowProfileDetail").css("div").css("p::text").extract()[0]
        except:
            print "error"
        phone_web=response.css("div.contactCol").css("div").css("p").extract()
        company_addr=response.css("div.companyCol").css("p").css("strong::text").extract()
        
        business_text=""
        
        try:
            business_text=response.css("div.rowBusiness").css("div.holder").css("div").css("p::text").extract()[0]
        except:
            print "error"
        ideal_refer1=response.css("div.rowTwoCol").css("div.holder").css("div").css("p::text").extract()
        top_product=response.css("div.rowTwoCol").css("div.holder").css("div").css("p::text").extract()
        my_ideal_refer_pat1=response.css("div.rowTwoCol").css("div.holder").css("div").css("p::text").extract()
        
        company_info=response.css("div.rowTwoCol").css("div.holder").css("div").extract()
        
        
        
        try:
             
                
            s=""
            for i in str(company_info):
                s=s+i
            ide_ref=""
            
            print s
                            
            if s in "Ideal Referral":
                print s
                #st=s.index('Ideal Referral')
                
                #print st
                #for i in range(st,len(st)):
                    #if i != "</p>":
                        #ide_ref=ide_ref+i
                    #else:
                        #print ide_ref
                        #break
                        
                
            
        except:
            print "c_error"
            
        my_ideal_refer_pat=""
        try:     
          my_ideal_refer_pat=" ".join(map(str, my_ideal_refer_pat1)).strip()
        except:
            print("error")


        business_name=""
        try:
            business_name=company_addr[0]
        except:
            print "error"
            
        ideal_refer=""
        try:     
          ideal_refer=" ".join(map(str, ideal_refer1)).strip()
        except:
            print("error")
       
        
        phone=""
        mobile=""
        direct=""
        
        try:
            phone=str(phone_web[0])
            x = re.split("\s", phone)
            while("" in x) : 
                x.remove("") 
                
            try:
                ind=x.index('Phone')
                ind=ind+1
                phone=x[ind]
               
                start=phone.index('i')+2
                end=phone.rindex('b')-2
               
                s=phone[start:end]
                phone=s

            except:
                pass

            try:
                ind=x.index('Mobile')
                ind=ind+1
                mobile=x[ind]

                start=mobile.index('i')+2
                end=mobile.rindex('b')-2
                
                s=mobile[start:end]
                mobile=s

            except:
                pass


            try:
                ind=x.index('Direct')
                ind=ind+1
                
                direct=x[ind]
                
                start=direct.index('i')+2
                end=direct.rindex('b')-2
                
                s=direct[start:end]
                direct=s


            except:
                pass

            
        except Exception as e:
            print e
           
        website="" 
        try:
            website=response.css("div.contactCol").css("div").css("p").css('a::text').extract()[0]
        except:
            print "error"
 
        city=""
        try:
            city=company_addr[5]
        except:
            print "error"
            
      
        state=""
        try:
            state=company_addr[6]
        except:
            print "error"

        try:
            del company_addr[0]
        except:
            print "error"
            
        address=""
        try:     
          address=" ".join(map(str, company_addr)).strip()
        except:
            print("error")
            
        chapter_f=self.chapter[self.cha_i]

#        self.df=pd.DataFrame(self.data,columns=['State','City','Chapters','Members Names','Business Name','Profession/Speciality','Phone','Direct','Mobile','CompanyWebsite','Address','My Business Text','Idea Referral','My ideal referral partner','Top product'])
        
                                                   
       
        list=[state,city,chapter_f,member_name,business_name,profession_speciality,phone,direct,mobile,website,address,business_text,ideal_refer,my_ideal_refer_pat,top_product]
        
        self.data.append(list)
        
        
        
        
            
          

           
             
