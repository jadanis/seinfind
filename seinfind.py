from lxml import html
import requests
import re

url = 'http://www.seinfeldscripts.com/'
script_list = 'seinfeld-scripts.html'

page = requests.get(url + script_list)
tree = html.fromstring(page.content)

episodes = tree.xpath('//td/a/text()')
episode_links = tree.xpath('//td/a/@href')

def script_parse(u):
  script_page = requests.get(url + u)
  script_tree = html.fromstring(script_page.content)
  script_lines = script_tree.xpath('//div[@id="content"]/p/text()')
  return ''.join(script_lines)

'''
Would like to replace re.finditer with re.search to ignore case.
Case can be an issue depending on the punctuation of the script
'''
def script_res(search_line,script):
  idxs = [m.start() for m in re.finditer(search_line,script)]
  l = len(search_line)
  t_ind = [(- script[::-1].find('.',-n),script.find('.',n+l)+1) for n in idxs]
  res = [script[t[0]:t[1]] for t in t_ind]
  return list(dict.fromkeys(res))

def script_iter(search_line):
  for n in range(len(episodes)):
    t_s = script_parse(episode_links[n].strip())
    res = script_res(search_line,t_s)
    if res:
      print(episodes[n])
      for r in res:
        print(r)
      print()


def get_search():
  print('Enter the line you\'re looking for: ')
  return input()

script_iter(get_search())

