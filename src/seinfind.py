from lxml import html
import requests
import re

# Root URL where Seinfeld scripts are sourced
url = 'http://www.seinfeldscripts.com/'
script_list = 'seinfeld-scripts.html'

# Get the HTML page and parse it into a tree
page = requests.get(url + script_list)
tree = html.fromstring(page.content)

#Episodes Titles and link to page where script is held
episodes = tree.xpath('//td/a/text()')
episode_links = tree.xpath('//td/a/@href')

'''
Given the link to the script and generate the tree from this
We find all the p-tags under the content-div, and join it as one string.
Some scripts have the body in one p-tag while others have line by line encase in p tags.
'''
def script_parse(u):
  script_page = requests.get(url + u)
  script_tree = html.fromstring(script_page.content)
  script_lines = script_tree.xpath('//div[@id="content"]/p/text()')
  return ''.join(script_lines)

'''
Would like to replace re.finditer with re.search to ignore case.
Case can be an issue depending on the punctuation of the script

Given the text we're searchign for and the script (as a string),
we find all index instances of the text within the script.
Create a list of tuples by searching for the surrounding periods near those indexes.
Take the text between these values as a list of lines, and eliminate duplicates
'''
def script_res(search_line,script):
  idxs = [m.start() for m in re.finditer(search_line,script)]
  l = len(search_line)
  t_ind = [(- script[::-1].find('.',-n),script.find('.',n+l)+1) for n in idxs]
  res = [script[t[0]:t[1]] for t in t_ind]
  return list(dict.fromkeys(res))

'''
Given the search text iterate through all scripts to find the text.
If there are results print the title of the episode along with resulting hits.
'''
def script_iter(search_line):
  for n in range(len(episodes)):
    t_s = script_parse(episode_links[n].strip())
    res = script_res(search_line,t_s)
    if res:
      print(episodes[n])
      for r in res:
        print(r)
      print()

#Ask user for search text
def get_search():
  print('Enter the line you\'re looking for: ')
  return input()

if __name__ == "__main__":
  script_iter(get_search())

