from flask import Flask, render_template, request
import requests
import json
from NYTserects import api_key
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/search')
def search():
    country = request.args.get('country')
    trends = get_trend(country)
    return render_template('search.html', country=country, trends=trends)

@app.route('/search/<trend>')
def get_news(trend):
    '''
    get news of a trend
    trend: trend name
    return: json
    '''
    today = datetime.today().strftime('%Y-%m-%d')
    cache = open_cache(f'news_{trend}_{today}.json')
    if cache == None:
        url = "https://api.nytimes.com/svc/search/v2/articlesearch.json"
        params = {'q': trend, 'api-key': api_key}
        response = requests.get(url, params=params).json() 
        top_news_with_url_and_img = {}
        for i in range(len(response['response']['docs'])):
            top_news_with_url_and_img[response['response']['docs'][i]['headline']['main']] = []
            top_news_with_url_and_img[response['response']['docs'][i]['headline']['main']].append(response['response']['docs'][i]['web_url'])
            # top_news_with_url_and_img[response['response']['docs'][i]['headline']['main']].append(response['response']['docs'][i]['multimedia'][0]['url'])
        save_cache(f'news_{trend}_{today}.json', top_news_with_url_and_img)
    else:
        top_news_with_url_and_img = cache
    return render_template('news.html', trend=trend, top=top_news_with_url_and_img)    

def get_trend(loc):
    '''
    get trend of a location
    loc: location id
    return: json

    '''
    today = datetime.today().strftime('%Y-%m-%d')
    loc_id = get_loc_id(loc)
    if loc_id == None:
        return None
    cache = open_cache(f'trend_{loc}_{today}.json')
    if cache == None:
        url = "https://api.twitter.com/1.1/trends/place.json?"
        payload={}
        headers = {
        'Authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANqNkAEAAAAAGE4dok9Xdo2JMETUzd83dT%2FbbQQ%3DojdPCxtNep21wPeMRxks8gOsxlsoDCpSDY2FtlGjiVpn5ziHPe',
        'Cookie': 'guest_id=v1%3A167038332417705283; guest_id_ads=v1%3A167038332417705283; guest_id_marketing=v1%3A167038332417705283; personalization_id="v1_z0N8FmK/dY4thiNY6w314g=="'
        }
        params = {
            'id': loc_id
        }
        response = requests.get(url, headers=headers, data=payload, params=params).json()
        trends = {}
        for i in range(len(response[0]['trends'])):
            trends[response[0]['trends'][i]['name']] = []
            trends[response[0]['trends'][i]['name']].append(response[0]['trends'][i]['url'])
            trends[response[0]['trends'][i]['name']].append(response[0]['trends'][i]['tweet_volume']) if response[0]['trends'][i]['tweet_volume'] != None else trends[response[0]['trends'][i]['name']].append(0)
            trends = {k: v for k, v in sorted(trends.items(), key=lambda item: item[1][1], reverse=True)}
        save_cache(f'trend_{loc}_{today}.json', trends)
    else:
        trends = cache
    return trends

def get_loc_id(loc):
    '''
    get location id
    loc: location name
    return: location id
    '''
    id_list = json.load(open('id_list.json'))
    for i in range(len(id_list)):
        if loc.lower() in id_list[i]['name'].lower():
            return id_list[i]['woeid']
    print("Location not found")

def open_cache(filename):
    try:
        cache_file = open(filename, 'r')
        cache_contents = cache_file.read()
        cache_dict = json.loads(cache_contents)
        cache_file.close()
    except:
        cache_dict = None
    return cache_dict

def save_cache(filename, cache_dict):
    dumped_json_cache = json.dumps(cache_dict)
    fw = open(filename,"w")
    fw.write(dumped_json_cache)
    fw.close() 

class Node:
  
  def __init__(self,item = 0):
    self.key = item
    self.left,self.right = None,None
  
  
# Root of BST
root = Node()
  
root = None
  
# This method mainly
# calls insertRec()
def insert(key):
  global root
  root = insertRec(root, key)
  
# A recursive function to 
# insert a new key in BST
def insertRec(root, key):
  
  # If the tree is empty,
  # return a new node
  
  if (root == None):
    root = Node(key)
    return root
  
  # Otherwise, recur
  # down the tree 
  if (key < root.key):
    root.left = insertRec(root.left, key)
  elif (key > root.key):
    root.right = insertRec(root.right, key)
  
  # return the root
  return root
  
# A function to do 
# inorder traversal of BST
def inorderRec(root):
  if (root != None):
    inorderRec(root.left)
    print(root.key ,end = " ")
    inorderRec(root.right)
    
def treeins(arr):
  for i in range(len(arr)):
    insert(arr[i])

def main():
    app.run(debug=True)

if __name__ == '__main__':
    main()