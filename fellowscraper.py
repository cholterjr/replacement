#! /usr/bin/python
import urllib
import urllib2
from urllib import urlopen
import re
from xml.dom.minidom import parseString
import smtplib
import string
import os
from bs4 import BeautifulSoup
import unicodedata
import datetime

def scrapepage():
    
    emailList = []
    fellowList = []
    firstURL = "http://www.ventureforamerica.org/2012fellows/"
    middleURL = "http://www.ventureforamerica.org/2013fellows/"
    lastURL = "http://www.ventureforamerica.org/2014fellows/"
    firstPage = urlopen(firstURL).read()
    middlePage = urlopen(middleURL).read()
    lastPage = urlopen(lastURL).read()
    pages = [firstPage, middlePage, lastPage]
    result = ""
    for i in range(0,len(pages)):
        page = pages[i]
        soup = BeautifulSoup(page)
        fellows = soup.find_all(attrs={'class':'entry'})
        for x in range(0, len(fellows)):
            fellowDivs = fellows[x].find_all('div')
            imageURL = str(fellowDivs[0]['style']).split("('")[1].rstrip("');")
            name = fellowDivs[1].find('h4').getText()
            if i<2:
                paragraphs = fellowDivs[1].find(attrs={'class':'school_company'}).find_all('p')
                company = paragraphs[0].getText()
                school = paragraphs[1].getText()
            else:
                company = "N/A"
                school = fellowDivs[1].find(attrs={'class':'school'}).getText().split("<a")[1].strip()
            bio =   fellows[x].find(attrs={'class':'bio'}).getText()
            lastName = name.split(" ")[1].lower()
            HTML = ""
            boxHTML = '<div class="fancy" data-fancybox-group="gallery" id="'+lastName+'Box" rel="gallery1">\
                            <div class="pic" id="actual" style="float:left; background:url(\''+imageURL+'\'); background-size:cover; width:125px; height:160px; margin-right:10px; text-align:center;">\
                                <div class="overlay" style="width:125px; height:160px;">\
                                    <a class="text" ><br><br><br>'+name+'<br>'+school+'</a>\
                                </div>\
                            </div>\
                        </div>'
            popupHTML = '<div id="'+lastName+'Popup"  data-fancybox-group="gallery" >\
                            <div style="display:inline-block; margin:5px;">\
                                <div style="float:left; background:url(\''+imageURL+'\'); background-size:cover; width:167px; height:213px; padding-right:10px;">\
                                </div>\
                                <div style="margin-left:190px;">\
                                    <a>'+bio+'</a>\
                                </div>\
                            </div>\
                        </div>'
            if (i==0):
                year = 12
            elif (i==1):
                year = 13
            else:
                year = 14
            scriptHTML = '<script> $(\''+"#"+lastName+'Box\').data("city", "NA"); $(\''+"#"+lastName+'Box\').data("gender", "ADD IN"); $(\''+"#"+lastName+'Box\').data("class", "'+str(year)+'"); $(\''+"#"+lastName+'Box\').data("company", "'+company+'");</script>'
            result += (boxHTML+scriptHTML+popupHTML)
            result += "\n\n"
            '''result += ("Name: " + name+"\n")
            result += ("Image: " + imageURL+"\n")
            result += ("School: " + school+"\n")
            result += ("Company: " + company+"\n")
            result += ("Bio: " + bio+"\n")
            result += "\n\n"'''

    if (result!=""):
        SUBJECT = "VFA Fellows"
        TO = "cholter09@gmail.com"
        FROM = "cholter09@gmail.com"
        BODY = string.join((
                "From: %s" % FROM,
                "To: %s" % TO,
                "Subject: %s" % SUBJECT ,
                "",
                result
                ), "\r\n")
        HOST = "smtp.gmail.com"
        server = smtplib.SMTP(HOST, 587)
        server.starttls()
        server.login("cholter09", "French123")
        server.sendmail(FROM, TO, BODY.encode("utf-8"))
        server.quit()


scrapepage()


