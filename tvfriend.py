import urllib2
from urllib2 import urlopen
from xml.dom.minidom import parseString
from sys import exit

checklist = ["x","X"]
SHOWINFO_URL = 'http://services.tvrage.com/feeds/showinfo.php?sid='
SEARCH_URL = "http://services.tvrage.com/feeds/search.php?show="

def program_open():
	print """
Welcome to TV Friend. What would you like to do?
	1. Show me what's on the tube tonight.
	2. Show me what's on the tube tomorrow night.
	3. Show me all the stuff playing this week.
	4. List the shows I follow.
	5. Add a show to my list.
	6. Remove a show from my list.	
	Q. Quit
"""
	tv_friend_runner()

def tv_friend_runner():
	next = raw_input(" >>> ").strip()
	if next in ('1', '2', '3', '6'):
		pass
	elif next == "4":
		printShows()
	elif next == "5":
		queryForShow()
	elif next.lower() == 'q':
		exit(0)
	else:
		print "Invalid input."
		tv_friend_runner()	
		
def printList(l):
	for a, show in enumerate(l):
		print "\t %d. - %s" % (a + 1, show)
		checklist.append(a + 1)
	
def getShowInfo(show_id, tag):
	url = SHOWINFO_URL + str(show_id)
	f = urlopen(url)
	data = f.read()
	f.close()
	dom = parseString(data)
	for node in dom.getElementsByTagName(tag):
		xmlTag = node.toxml()
		xmlData = xmlTag.replace('<%s>' % tag, '').replace('</%s>' % tag, '')
		return xmlData
		
#showid = "24493"
#url = "http://services.tvrage.com/myfeeds/episodeinfo.php?key=UHJXhYnjU5MYMXKqOgwM&sid=" + showid

def queryForShow():
	search_show = urllib2.quote(raw_input("Which show would you like to follow? > "))
	search = SEARCH_URL + str(search_show)
	search_file = urlopen(search)
	searchdata = search_file.read()
	search_file.close()
	dom = parseString(searchdata)
	search_name_list = []
	search_id_list = []

	##load the show name from the xml	
	for node in dom.getElementsByTagName('name'):  # visit every node <name/>
		xmlNameTag = node.toxml()
		xmlNameData = xmlNameTag.replace('<name>','').replace('</name>','')
		search_name_list.append(xmlNameData)

	##load the showid from the xml
	for node in dom.getElementsByTagName('showid'): # visit every node <showid/>
		xmlIDTag = node.toxml()
		xmlIDData = xmlIDTag.replace('<showid>','').replace('</showid>','')
		search_id_list.append(int(xmlIDData))

	printList(search_name_list)

	show_selection = raw_input("Which of these is the show you meant? > ")
	
	##loop input if input is bad, else allow a way out, or copy good info to file
	while str(show_selection) not in str(checklist):
		print "Invalid input. Press x to exit."
		show_selection = raw_input("Which of these is the show you meant? > ")
	if show_selection.lower() == "x":
		program_open()
	else:
		check_cancelled_url = SHOWINFO_URL + str(search_id_list[int(show_selection) - 1])
		cancel_file = urlopen(check_cancelled_url)
		cancel_data = cancel_file.read()
		cancel_file.close()
		dom = parseString(cancel_data)
		for node in dom.getElementsByTagName('status'):
			xmlCancelTag = node.toxml()
			xmlCancelData = xmlCancelTag.replace('<status>','').replace('</status>','')
			if "Canceled" in xmlCancelData:
				print "Sorry, but %s appears to have been cancelled!" % search_name_list[int(show_selection) -1]
				raw_input("Press any key to continue.")
				print "\n\n\n"
				program_open()
			else:
				#add to file 'shows.txt'/ return to program
				search_write = search_name_list[int(show_selection) -1] + "\n" + str(search_id_list[int(show_selection ) - 1]) + "\n"				
				try:
					f = open("shows.txt", "r+")
				except IOError:
					open('shows.txt', 'w')
					f = open('shows.txt', 'r+')
				store = f.read()
				if search_write in store:
					print "You were already following %s!" % search_name_list[int(show_selection) -1]
					f.close()
					raw_input("Press any key to continue.")
					print "\n\n\n"
					program_open()
				else:
					f.seek(0)
					f.write(store + search_write)
					f.close()
    				print "%s saved to your collection!" % search_name_list[int(show_selection) -1]
    				raw_input("Press any key to continue.")
    				print "\n\n\n"
    				program_open()
    				
    				
def printShows():
	shows = []
	showfile = open("shows.txt", "r")
	for show in showfile:
		shows.append(show.rstrip())
	showfile.close()
	shownames = []
	showid = []
	for show in shows:
		if (shows.index(show) + 1) % 2 != 0:
			shownames.append(show)
		else:
			showid.append(show)
	printList(shownames)
	show_selection = raw_input("Would you like more info on one of these shows? > ")
	while str(show_selection) not in str(checklist):
		print "Invalid input. Press x to exit."
		show_selection = raw_input("Would you like more info on one of these shows? > ")
	if show_selection.lower() == "x":
		program_open()
	else:
#		choice_id = showid[int(show_selection) - 1]
		showid = str(showid[int(show_selection) - 1])
		print "Name: %s" % getShowInfo(showid, 'showname')
		print "Seasons: %s" % getShowInfo(showid, 'seasons')
		print "Airday / Time: %s, %s" % (getShowInfo(showid, 'airday'), getShowInfo(showid, 'airtime'))
		

#	for show in shows:
#		print show
#	for show in shows
	


#	if show.index in shows % 2 == 0:
#		show_name += show
#		print show
#	else:
#		show_id += show
#		print show 

#	print search_name_list
#	print search_id_list

program_open()

#print node.toxml()
#xmlTag = dom.getElementsByTagName('name')[:].toxml() #[0] after ('name')

#file = urlopen(url)
#data = file.read()
#file.close()
#dom = parseString(data)

#xmlTag = dom.getElementsByTagName('name')[0].toxml()
#xmlData=xmlTag.replace('<name>','').replace('</name>','')
#print xmlTag
#print xmlData
