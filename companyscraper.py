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
    companyList = []
    companiesFile = open("VFA_Companies.txt", "r+")
    totalCompanies = companiesFile.read()
    URL = "http://www.ventureforamerica.org/2014partners/"
    page = urlopen(URL).read()
    soup = BeautifulSoup(page)
    result = ""
    companyTables = soup.find_all('tbody')
    for x in range(1, len(companyTables)):
        companies = companyTables[x].find_all('tr')
        city = ""
        if (x==1):
            city = "Baltimore"
        elif (x==2):
            city = "Cincinatti"
        elif (x==3):
            city = "Cleveland"   
        elif (x==4):
            city = "Columbus"
        elif (x==5):
            city = "Detroit" 
        elif (x==6):
            city = "Las Vegas"
        elif (x==7):
            city = "Miami"
        elif (x==8):
            city = "New Orleans"
        elif (x==9):
            city = "Philadelphia"
        elif (x==10):
            city = "Providence"
        elif (x==11):
            city = "San Antonio"
        elif (x==12):
            city = "St. Louis"
        else:
            break
        for i in range(0, len(companies)):  
            event = companies[i]
            info = companies[i].find_all('td')
            if (len(info[0].find_all('img'))>0):
                image = info[0].find_all('img')[0]['src']
            else:
                image = "No logo provided"
            #print info[1].find('p')
            name = info[1].find('p')['id']
            text = info[1].find('p').getText()
            if (info[1].find('a').has_attr('href')):
                link = info[1].find('a')['href']
            else:
                link = "No company website provided"
            if (totalCompanies.find(name)==-1):
                companiesFile.write("%s\n" % name)
                result += ("Company: " + name+"\n")
                result += ("Image: " + image+"\n")
                result += ("Description: " + text+"\n")
                result += ("City: " + city+"\n")
                result += ("Link: " + link+"\n")
                result += "\n\n"

    if (result!=""):
        SUBJECT = "VFA Companies"
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