from lxml import html
import requests
import re
import sys
import itertools

# Root URL where Seinfeld scripts are sourced
url = 'http://www.seinology.com/'
script_list = 'scripts-english.shtml'

# Get the HTML page and parse it into a tree
page = requests.get(url + script_list)
tree = html.fromstring(page.content)

#Episodes Titles and link to page where script is held
episodes = tree.xpath('//td//a/text()')
#episode_links = tree.xpath('//td/a/@href')

'''
Given the link to the script and generate the tree from this
We find all the p-tags under the content-div, and join it as one string.
Some scripts have the body in one p-tag while others have line by line encase in p tags.
'''
def script_parse(u):
  
  try:

    episode_num = re.findall(r'[0-9]+',u)
    # Seinology episode link format
    u = 'scripts/script-' + episode_num[0] + '.shtml'
    # Retrieve page
    script_page = requests.get(url + u)
    # create tree
    script_tree = html.fromstring(script_page.content)
    # substitute whitsepace for plain space and strip result
    script_lines = [ re.sub(r'\s', ' ', l) for l in script_tree.xpath('//p//text()') ]
    return script_lines
  except:
    return []

def sent_find(script):
  regex = r'([A-Z][^\.!?]*[\.!?])'
  return re.findall(regex,script)

'''
Would like to replace re.finditer with re.search to ignore case.
Case can be an issue depending on the punctuation of the script
Given the text we're searchign for and the script (as a string),
we find all index instances of the text within the script.
Create a list of tuples by searching for the surrounding periods near those indexes.
Take the text between these values as a list of lines, and eliminate duplicates
'''
def script_res(search_line,script):
  
  res = [r for r in sent_find(script) if r.find(search_line) > -1]
  return res

'''
Given the search text iterate through all scripts to find the text.
If there are results print the title of the episode along with resulting hits.
'''
def script_iter(search_line):
  for e in episodes:
    t_s = script_parse(e)
    res = list(itertools.chain(*[ script_res(search_line,s) for s in t_s ]))
    if res:
      print(e)
      for r in res:
        print(r)
      print()

#Ask user for search text
def get_search():
  print('Enter the line you\'re looking for: ')
  return input()

def seinfind():
  script_iter(get_search())

if __name__ == "__main__":
  search_line = sys.argv[2]
  script_iter(search_line)
  #script_iter(get_search())
