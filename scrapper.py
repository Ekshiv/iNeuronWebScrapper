import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq
import json

import logging

logging.basicConfig(filename='log_data.log',level=logging.INFO,format = '%(asctime)s - %(levelname)s - %(message)s')


## Getting list of courses

def get_course_list(search_url):
    try:
        uClient = uReq(search_url)
        ineuron_page = uClient.read()
        uClient.close()
        ineuron_lxml = bs(ineuron_page,'html.parser') # parsing the webpage as HTML
        json_output = bs(str(ineuron_lxml.findAll("script",{'type':"application/json"},'html.parser'))) # seacrhing for appropriate tag to redirect to the product link
        logging.info('Data retrieved successfully')
        test = json_output.script.text
        data = json.loads(test)
        course_key = data["props"]["pageProps"]["initialState"]["init"]["courses"].keys()
        course_list= list(course_key)
        return course_list
        logging.info('Scrapping course list done successfully !!!')
    except Exception as e:
        logging.error(e)



## Fetching course urls

def get_course_urls(course_list):
    url_list = []

    try:
        for i in range(len(course_list)):
            url_list.append("https://courses.ineuron.ai/" + course_list[i].replace(" ", "-"))

        return url_list

    except Exception as e:
        logging.error(e)
        logging.debug("Failed to generate urls")





## Converting html data to Json

def get_html_req_json_data(urls):
    try:
        uClient = uReq(urls)
        course_page = uClient.read()
        uClient.close()
        course_lxml = bs(course_page,'lxml')
        course_json_output = bs(str(course_lxml.findAll("script",{'type':"application/json"})))
        course_text = course_json_output.script.text
        course_data = json.loads(course_text)
        return course_data
    except Exception as e:
        logging.info("Failed to get json data from html file")
        logging.error(e)



def get_course_details(course_urls):
    course_data_list = []
    try:
        for i in range(len(course_urls)):
            data = get_html_req_json_data(course_urls[i])
            course_data_list.append(data)
        return course_data_list
    except Exception as e:
        logging.info('Failed to get course details')
        logging.error(e)


def get_curriculum(c_data):
    return_list = []
    try:
        list1 = len(list(c_data["props"]["pageProps"]["data"]['meta']['curriculum'].keys()))
        c_list = list(c_data["props"]["pageProps"]["data"]['meta']['curriculum'].keys())
        for i in range(list1):
            length = len(list(c_data["props"]["pageProps"]["data"]['meta']['curriculum'][c_list[i]]['items']))
            for j in range(length):
                #             print((c_data["props"]["pageProps"]["data"]['meta']['curriculum'][c_list[i]]['items'][j]['title']))
                return_list.append(
                    c_data["props"]["pageProps"]["data"]['meta']['curriculum'][c_list[i]]['items'][j]['title'])
        return return_list
    except Exception as e:
        logging.info('Failed to get curriculum data')
        logging.error(e)




def get_curriculum_headings(c_data1):
    return_list1 = []
    try:
        list2 = len(list(c_data1["props"]["pageProps"]["data"]['meta']['curriculum'].keys()))
        c_list1 = list(c_data1["props"]["pageProps"]["data"]['meta']['curriculum'].keys())
        for i in range(list2):
            return_list1.append(c_data1["props"]["pageProps"]["data"]['meta']['curriculum'][c_list1[i]]['title'])
        return return_list1
    except Exception as e:
        logging.info('Failed to get curriculum headings')
        logging.error(e)



def get_project_headings(c_data2):
    return_list2 = []
    try:
        list3 = len(list(c_data2["props"]["pageProps"]["data"]['meta']['projects'].keys()))
        c_list1 = list(c_data2["props"]["pageProps"]["data"]['meta']['projects'].keys())
        for i in range(list3):
            return_list2.append(c_data2["props"]["pageProps"]["data"]['meta']['projects'][c_list1[i]]['title'])
        return return_list2
    except Exception as e:
        logging.info('Failed to get Project headings overview')
        logging.error(e)




def get_projects(c_data3):
    return_list3 = []
    try:
        list4 = len(list(c_data3["props"]["pageProps"]["data"]['meta']['projects'].keys()))
        c_list = list(c_data3["props"]["pageProps"]["data"]['meta']['projects'].keys())
        for i in range(list4):
            length = len(list(c_data3["props"]["pageProps"]["data"]['meta']['projects'][c_list[i]]['items']))
            for j in range(length):
    #             print((c_data["props"]["pageProps"]["data"]['meta']['curriculum'][c_list[i]]['items'][j]['title']))
                return_list3.append(c_data3["props"]["pageProps"]["data"]['meta']['projects'][c_list[i]]['items'][j]['title'])
        return return_list3
    except Exception as e:
        logging.info('Failed to get project details')
        logging.error(e)



## Fetching details of all courses

def scrap_course_data(course_data):
    l = []

    try:
        for i in range(len(course_data)):
            data1 = dict()
            data1['title'] = course_data[i]["props"]["pageProps"]["data"]["title"]
            data1['isJobGuaranteeProgram'] = course_data[i]["props"]["pageProps"]["data"]["isJobGuaranteeProgram"]
            data1['description'] = course_data[i]["props"]["pageProps"]["data"]['details']['description']

            if 'pricing' not in course_data[i]["props"]["pageProps"]["data"]['details']:
                data1['pricing'] = 'NULL'
                data1['projects'] = "NUll"
                data1['projects_overview'] = "NUll"
                data1['curriculum'] = 'NULL'
                data1['curriculum_overview'] = 'NULL'
                data1['requirements'] = 'NULL'
                data1['features'] = 'NULL'
                data1['learn'] = 'NULL'

                l.append(data1)

                continue

            else:
                if course_data[i]["props"]["pageProps"]["data"]['details']['pricing']['isFree']:
                    data1['pricing'] = 0
                else:
                    data1['pricing'] = course_data[i]["props"]["pageProps"]["data"]['details']['pricing']['IN']

                if (len(list(course_data[i]["props"]["pageProps"]["data"]['meta']['projects'].keys())) == 0):
                    data1['projects'] = "NUll"
                    data1['projects_overview'] = "NUll"
                else:
                    data1['projects'] = get_projects(course_data[i])
                    data1['projects_overview'] = get_project_headings(course_data[i])

                data1['curriculum'] = get_curriculum(course_data[i])
                data1['curriculum_overview'] = get_curriculum_headings(course_data[i])
                data1['requirements'] = course_data[i]["props"]["pageProps"]["data"]['meta']['overview']['requirements']
                data1['features'] = course_data[i]["props"]["pageProps"]["data"]['meta']['overview']['features']
                data1['learn'] = course_data[i]["props"]["pageProps"]["data"]['meta']['overview']['learn']

                l.append(data1)
        logging.info('Successfully Scrapped the data')
        return l
    except Exception as e:
        logging.info('Failed to scrap the data')
        logging.error(e)