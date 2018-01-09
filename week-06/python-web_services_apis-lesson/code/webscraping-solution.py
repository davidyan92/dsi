'''
CLASS: Web Scraping with Beautiful Soup
What is web scraping?
- Extracting information from websites (simulates a human copying and pasting)
- Based on finding patterns in website code (usually HTML)
What are best practices for web scraping?
- Scraping too many pages too fast can get your IP address blocked
- Pay attention to the robots exclusion standard (robots.txt)
- Let's look at http://www.facebook.com/robots.txt
What is HTML?
- Code interpreted by a web browser to produce ("render") a web page
- Let's look at example.html
- Tags are opened and closed
- Tags have optional attributes
How to view HTML code:
- To view the entire page: "View Source" or "View Page Source" or "Show Page Source"
- To view a specific part: "Inspect Element"
- Safari users: Safari menu, Preferences, Advanced, Show Develop menu in menu bar
- Let's inspect example.html
'''

# read the HTML code for a web page and save as a string
# with open('example.html', 'rU') as f:
#    html = f.read()

# read the HTML code using requests
import requests
html = requests.get()

# convert HTML into a structured Soup object
from bs4 import BeautifulSoup
b = BeautifulSoup(html)

# print out the object
print b
print b.prettify()

# 'find' method returns the first matching Tag (and everything inside of it)
b.find(name='body')
b.find(name='h1')

# Tags allow you to access the 'inside text'
b.find(name='h1').text

# Tags also allow you to access their attributes
b.find(name='h1')['id']

# 'find_all' method is useful for finding all matching Tags
b.find(name='p')        # returns a Tag
b.find_all(name='p')    # returns a ResultSet (like a list of Tags)

# ResultSets can be sliced like lists
len(b.find_all(name='p'))
b.find_all(name='p')[0]
b.find_all(name='p')[0].text
b.find_all(name='p')[0]['id']

# iterate over a ResultSet
results = b.find_all(name='p')
for tag in results:
    print tag.text

# limit search by Tag attribute
b.find(name='p', attrs={'id':'scraping'})
b.find_all(name='p', attrs={'class':'topic'})
b.find_all(attrs={'class':'topic'})

# limit search to specific sections
b.find_all(name='li')
b.find(name='ul', attrs={'id':'scraping'}).find_all(name='li')

'''
EXERCISE ONE
'''

# find the 'h2' tag and then print its text
b.find(name='h2').text

# find the 'p' tag with an 'id' value of 'lab' and then print its text
b.find(name='p', attrs={'id':'lab'}).text

# find the first 'p' tag and then print the value of the 'id' attribute
b.find(name='p')['id']

# print the text of all four resources
results = b.find_all(name='li')
for tag in results:
    print tag.text

# print the text of only the API resources
results = b.find(name='ul', attrs={'id':'api'}).find_all(name='li')
for tag in results:
    print tag.text
