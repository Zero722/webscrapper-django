from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from django.template import loader
from django.conf import settings
from .models import Employee, Configuration
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.proxy import Proxy, ProxyType
from pathlib import Path
import pandas as pd
import json
import os
import csv
import datetime, time
import pprint


# Create your views here.
def webscraping(uploaded_file, scheme_parent_content, scheme_contents):
    dict_list = []

    ts = datetime.datetime.now()
    timestamp = ts.strftime("%m_%d_%Y_%H_%M_%S")
    unique_filename = 'output' + '_' + timestamp
    media_url = settings.MEDIA_ROOT
    upload_path = media_url + '/path_to_upload/'+unique_filename+'.csv'
    dump_path = media_url + '/dumps/'
    folder_path = str(Path(__file__).parents[0])
    chromedriver_path = os.path.join(folder_path, 'chromedriver/chromedriver.exe')
    
    chrome_options = Options()
    chrome_options.add_argument("--headless")
 
    PROXY = "192.168.11.13:8000"
    chrome_options.add_argument('--proxy-server=%s' % PROXY)
    # chrome_options.add_experimental_option("detach", True)

    driver = webdriver.Chrome(executable_path=chromedriver_path,options=chrome_options)

    for file_idx, url in enumerate(uploaded_file):
        
        try:
            driver.get(url)
            # time.sleep(5)
        except:
            return ""
        page_source = driver.page_source
        file_to_write = open(dump_path+"a"+str(file_idx)+".html", "w", encoding="utf-8")
        file_to_write.write(page_source)
        file_to_write.close()
       
        print(url)

        contents = zip(scheme_parent_content, scheme_contents)
        for cat_idx, (parents, childs) in enumerate(contents):
            print(parents.field)
       
            parent_xpath = parents.xpath
            try:
                parent_text: list[WebElement] = driver.find_elements(by=By.XPATH, value=parent_xpath)
                if (len(parent_text)) == 0:
                    parent_text = ["n/a"]
            except:
                parent_text = ["n/a"]
            for field_idx, parent in enumerate(parent_text): 
                print("AAAAAAAAAAAAAA")   
                for idx, child in enumerate(childs):
                    to_extract = "textContent"

                    child_xpath = '(' + parent_xpath + ')' + '[' + str(field_idx+1) + ']' + child.xpath
                    
                    xpath_list = child_xpath.split('/')
                    
                    if xpath_list[-1][0] == "@":
                        child_xpath = child_xpath.removesuffix(xpath_list[-1])
                        while child_xpath[-1] == '/':
                            child_xpath = child_xpath.removesuffix('/')
                        to_extract = (xpath_list[-1]).replace('@','')
                        # print(to_extract)

                    try:
                        print(child_xpath)
                        extracted_data = (driver.find_element(by=By.XPATH, value=child_xpath).get_attribute(to_extract)).strip()

                    except:
                        extracted_data="n/a"

                    obj = { "Index": str(str(file_idx+1)+'.'+str(cat_idx+1)+'.'+str(field_idx+1)+'.'+str(idx+1)), "Field": parents.field+'_'+child.field, "Value": extracted_data }
                    # print("obj",obj)
                    # print(obj)
                    dict_list.append(obj)

    # print(dict_list)
    with open(upload_path, 'w', encoding='utf8', newline='') as output_file:
        fc = csv.DictWriter(output_file, fieldnames=dict_list[0].keys())
        fc.writeheader()
        fc.writerows(dict_list)
        # break

    return unique_filename
    

def index(request):
    template = loader.get_template('projects/index.html')
    context = {}
    return HttpResponse(template.render(context, request))


def details(request, fname): 
    employees = Employee.objects.filter(first_name__iexact = fname)

    template = loader.get_template('projects/detail.html')
    context = {
        'employees': employees,
        'fname': fname,
    }
    return HttpResponse(template.render(context, request))


def add_json_to_db(uploaded_file, **kwargs):

    scheme_name_list = []

    if "get_scheme_name" in kwargs.keys() and kwargs["get_scheme_name"]:
        fl = (False, None)
    else:
        fl = False


    try:
        uploaded_json_file = json.loads(uploaded_file.read())
    
        for data in uploaded_json_file:
            if "name" in data:

                if "content" in data:
                    for content in data["content"]:
                        if "is_parent" in content and content["is_parent"] == "True":
                            if "field" in content and "xPath" in content:
                                field = content["field"].lower()
                                xpath = content["xPath"]
                                scheme_name = data["name"].lower()

                                if "parent_field" in content:
                                    parent_field = content["parent_field"]
                                else:
                                    parent_field = None
                                duplicate_data = Configuration.objects.filter(scheme_name = scheme_name, parent_field = parent_field, field = field).count()
                                
                                if duplicate_data == 0:
                                    print("Create")
                                    scheme = Configuration.objects.filter(scheme_name = scheme_name)
                                    if(scheme.count() == 0):
                                        config = Configuration(scheme_name = scheme_name, parent_field = parent_field, is_parent = True, field = field, xpath = xpath, created = timezone.now())
                                    else:
                                        earliest = Configuration.objects.filter(scheme_name = scheme_name).earliest('created')
                                        config = Configuration(scheme_name = scheme_name, parent_field = parent_field, is_parent = True, field = field, xpath = xpath, created = earliest.created)
                                        
                                    config.save()
                                
                                else:
                                    print("Update")
                                    config = Configuration.objects.get(scheme_name = scheme_name, parent_field = parent_field, field = field)
                                    config.is_parent = True
                                    config.xpath = xpath
                                    config.save()

                            else:
                                return fl
    
                        if "is_parent" in content and (content["is_parent"] != "True" and content["is_parent"] != "False"):
                            return fl
                        
                else:
                    return fl

                scheme_name_list.append(data["name"])

            else:
                return fl

        for data in uploaded_json_file:
            if "name" in data:
                if "content" in data:
                    for content in data["content"]:
                        if not ("is_parent" in content) or content["is_parent"] == "False":
                            if "field" in content and "xPath" in content:
                                field = content["field"].lower()
                                xpath = content["xPath"]
                                scheme_name = data["name"].lower()

                                if "parent_field" in content:
                                    parent_field = content["parent_field"]
                                else:
                                    parent_field = None

                                parent_exists = Configuration.objects.filter(scheme_name = scheme_name, field = parent_field, is_parent = True).count()

                                if parent_exists == 0:
                                    return fl

                                else:
                                    duplicate_data = Configuration.objects.filter(scheme_name = scheme_name, parent_field = parent_field, field = field).count()
                                    
                                    if duplicate_data == 0:
                                        print("Create")
                                        scheme = Configuration.objects.filter(scheme_name = scheme_name)
                                        print(scheme.count())
                                        if(scheme.count() == 0):
                                            config = Configuration(scheme_name = scheme_name, parent_field = parent_field, is_parent = False, field = field, xpath = xpath, created = timezone.now())
                                        else:
                                            earliest = Configuration.objects.filter(scheme_name = scheme_name).earliest('created')
                                            print(earliest.field)
                                            x=earliest.created
                                            config = Configuration(scheme_name = scheme_name, parent_field = parent_field, is_parent = False, field = field, xpath = xpath, created = earliest.created)
                                            
                                        config.save()

                                    
                                    else:
                                        print("Update")
                                        config = Configuration.objects.get(scheme_name = scheme_name, parent_field = parent_field, field = field)
                                        config.is_parent = False
                                        config.xpath = xpath
                                        config.save()

                            else:
                                return fl
    
                        if "is_parent" in content and (content["is_parent"] != "True" and content["is_parent"] != "False"):
                            return fl

                else:
                    return fl

            else:
                return fl

    except:
        return fl    

    if "get_scheme_name" in kwargs.keys() and kwargs["get_scheme_name"]:
        return True, scheme_name_list
    else:
        return True
                

def upload_page(request): 
    context = {}    
    scheme_list = Configuration.objects.values_list('scheme_name', flat=True).distinct().order_by('scheme_name')
    context['scheme_list'] = scheme_list
    if 'latest_url' in request.COOKIES.keys():
        latest_url = request.COOKIES['latest_url']
        context['latest_url'] = latest_url

    return render(request, 'projects/upload.html', context)

def upload_both_page(request): 
    context = {}    
    
    if 'latest_url' in request.COOKIES.keys():
        latest_url = request.COOKIES['latest_url']
        context['latest_url'] = latest_url

    return render(request, 'projects/upload_both.html', context)


def list_config(request):
    context = {}
    scheme_list = Configuration.objects.values_list('scheme_name', flat=True).distinct().order_by('scheme_name')
    context['scheme_list'] = scheme_list
    return render(request, 'projects/list_config.html', context)


def view_config(request, scheme_name):
    context = {}
    scheme_parent_content = Configuration.objects.filter(scheme_name=scheme_name, is_parent=True).order_by('field')
    scheme_contents = []
    for contents in scheme_parent_content:
        scheme_content = Configuration.objects.filter(scheme_name=scheme_name, parent_field=contents.field)
        scheme_contents.append(scheme_content)

    contents = zip(scheme_parent_content, scheme_contents)

    if scheme_parent_content:
        has_data = True
    else:
        has_data = False
  
    context['has_data'] = has_data
    context['contents'] = contents
    context['scheme_name'] = scheme_name
    return render(request, 'projects/view_config.html', context)


def uploadjson(request):
    print("Config JSON Upload")
    context = {}
    if request.method == 'POST':
      
        uploaded_file = request.FILES.get('file')
        print(uploaded_file.name)

        if uploaded_file.content_type == 'application/json':
            flag = add_json_to_db(uploaded_file)
            if flag:
                context['message'] = "Your file has been uploaded"
            else:
                context['message'] = "The format of config file is not correct"        
        else:
            context['message'] = "Please upload json file"

    print(context)

    return JsonResponse(context)


def edit_config(request, scheme_name):
    context = {}
    scheme_parent_content = Configuration.objects.filter(scheme_name=scheme_name, is_parent=True).order_by('field')
    scheme_contents = []
    for contents in scheme_parent_content:
        scheme_content = Configuration.objects.filter(scheme_name=scheme_name, parent_field=contents.field).order_by('field')
        scheme_contents.append(scheme_content)

    contents = zip(scheme_parent_content, scheme_contents)

    if scheme_parent_content:
        has_data = True
    else:
        has_data = False
  
    context['has_data'] = has_data
    context['contents'] = contents
    context['scheme_name'] = scheme_name
    return render(request, 'projects/edit.html', context)


def edit_scheme(request):
    context = {}
    db_id = request.POST.get("db_id")
    xpath = request.POST.get("xpath")

    config = Configuration.objects.get(id = db_id)
    config.xpath = xpath                            
    config.save()

    return JsonResponse(context)


def uploadcsv(request):
    print("apple")
    context = {}
    
    uploaded_file = request.FILES.get('file') 
    if uploaded_file.name.endswith('.csv'):
        scheme_name = request.POST.get("scheme_name")
        scheme_parent_content = Configuration.objects.filter(scheme_name=scheme_name, is_parent=True).order_by('field')
        scheme_contents = []
        for contents in scheme_parent_content:
            scheme_content = Configuration.objects.filter(scheme_name=scheme_name, parent_field=contents.field).order_by('field')
            scheme_contents.append(scheme_content)


    else:
        context['message'] = "Please upload csv file"
        response = JsonResponse(context)
        return response

    uploaded_df = pd.read_csv(uploaded_file)
    uploaded_list = uploaded_df.values.tolist()
    url_list =  [url for urls in uploaded_list for url in urls]

    print(scheme_parent_content)
    print(scheme_contents)

    url = webscraping(url_list, scheme_parent_content, scheme_contents)
    print(url)
    if url == "":
        context['message'] = url
        response = JsonResponse(context)
        return response

    context['message'] = "Download File has been ready. You may download it"
    context['urls'] = url

    response = JsonResponse(context)
    response.set_cookie(key = 'latest_url', value = url)

    return response


def upload_csv_json(request):
    context = {}
    uploaded_json_file = request.FILES.get('json_file')
    uploaded_csv_file = request.FILES.get('csv_file') 

    print(uploaded_json_file.name)

    if uploaded_json_file.content_type == 'application/json':
        if uploaded_csv_file.name.endswith('.csv'):
            flag, scheme_name_list = add_json_to_db(uploaded_json_file, get_scheme_name=True)
            if flag:
                context['message'] = "Your file has been uploaded"
                scheme_parent_content = Configuration.objects.filter(scheme_name__in=scheme_name_list, is_parent=True).order_by('field')
                scheme_contents = []
                for contents in scheme_parent_content:
                    scheme_content = Configuration.objects.filter(scheme_name=contents.scheme_name, parent_field=contents.field).order_by('field')
                    scheme_contents.append(scheme_content)

                uploaded_df = pd.read_csv(uploaded_csv_file)
                uploaded_csv_list = uploaded_df.values.tolist()
                url_list =  [url for urls in uploaded_csv_list for url in urls]

                url = webscraping(url_list, scheme_parent_content, scheme_contents)
                if url == "Error: Invalid URL":
                    context['message'] = "Your file has been uploaded. " + url
                    response = JsonResponse(context)
                    return response

                context['message'] = "Your file has been uploaded. " + "Download File has been ready. You may download it"
                context['urls'] = url

                response = JsonResponse(context)
                response.set_cookie(key = 'latest_url', value = url)

                return response

                
            else:
                context['message'] = "The format of config file is not correct"
                return JsonResponse(context)  
        else:
            context['message'] = "Please upload csv file"
            return JsonResponse(context)

    else:
        context['message'] = "Please upload json file"
        return JsonResponse(context)