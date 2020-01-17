from bs4 import BeautifulSoup
import requests
import html2text
import pandas as pd

#create states to loop through, put a dash instead of space to work for the urls
states = ["Alabama","Alaska","Arizona","Arkansas","California","Colorado",
  "Connecticut","Delaware","Florida","Georgia","Hawaii","Idaho","Illinois",
  "Indiana","Iowa","Kansas","Kentucky","Louisiana","Maine","Maryland",
  "Massachusetts","Michigan","Minnesota","Mississippi","Missouri","Montana",
  "Nebraska","Nevada","New-Hampshire","New-Jersey","New-Mexico","New-York",
  "North-Carolina","North-Dakota","Ohio","Oklahoma","Oregon","Pennsylvania",
  "Rhode-Island","South-Carolina","South-Dakota","Tennessee","Texas","Utah",
  "Vermont","Virginia","Washington","West-Virginia","Wisconsin","Wyoming","District-of-Columbia"]

#make the states lowercase
states = [x.lower() for x in states]

#create a range for collapsibles to then use for format
collapsibles = [x for x in range(14)]
collapsibles = collapsibles[1:]

#create the column names
titles = ['State',
'Voter registration deadlines',
'Election day registration',
'Voter registration rules',
'How to register to vote',
'Absentee ballot application deadlines',
'Absentee ballot rules',
'How to get an absentee ballot',
'Once you get your absentee ballot',
'Early voting starts',
'Early voting ends',
'In-person voter ID requirements',
'Absentee voter ID requirements',
'Voted absentee ballots are due']

df = pd.DataFrame()

for i in states:
  r = requests.get("https://www.vote.org/state/{0}/".format(i))
  #soup = BeautifulSoup(r.text.encode('utf-8').strip(), 'html.parser')
  soup = BeautifulSoup(r.text.encode("ascii", errors="ignore"), 'html.parser')
  df2 = pd.DataFrame({'State':i},index=[0])
  for x in collapsibles:
    voter_info = html2text.html2text(str(soup.find(id="collapsible-{0}".format(x))))
    df2['{0}'.format(titles[x])] = voter_info #append all the collapsibles
    offsite_links = [a['href'] for a in soup.find_all('a', href=True)]
    link_names = [a.text for a in soup.find_all('a', href=True)]
    offsite_links = offsite_links[38:44]
    link_names = link_names[38:44]
    for i in range(6):
      df2['offsite_link{0}'.format(i)] = offsite_links[i]
      df2['offsite_link_desc{0}'.format(i)] = link_names[i]
      #df2['offsite_desc'] = link_names[i]
    #df3 = pd.DataFrame([ x.split('**') for x in df2['Voter registration deadlines'].tolist() ])
    #df4 = pd.DataFrame([ x.split('**') for x in df2.iloc[:,12].tolist() ])
  df = df.append(df2, ignore_index = True)
  #df = pd.concat([df, df3,df4], axis=1)
#df = df.transpose()
#print(df)
df.to_csv("voter_reg_states_info.csv")