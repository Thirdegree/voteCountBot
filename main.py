import praw, re
from collections import deque
from time import sleep

accepted_initiators = ["thirdegree", "mtux96"]
done = deque(maxlen = 200)

r = praw.Reddit("voteCountBot by /u/thirdegree")

def _login():
	USERNAME = raw_input("Username?\n> ")
	PASSWORD = raw_input("Password?\n> ")
	r.login(USERNAME, PASSWORD)
	return USERNAME

def inbox_check():
	messages = r.get_unread()
	for i in messages:
		if (not i.was_comment) and (i.author.name in accepted_initiators) and (not (i.id in done)):
			try:
				i.mark_as_read()
				done.append(i.id)
				yay, nay, subreddit, counted_in = get_count(i.body)
				print "Yay: %d, Nay: %d"%(yay, nay)
				post_results(yay, nay, subreddit, counted_in)
			except requests.exceptions.MissingSchema as e:
				print e

def get_count(_url):
	sub = r.get_submission(url = _url)
	sub_comments = praw.helpers.flatten_tree(sub.comments)
	yay = 0
	nay = 0
	for comment in sub_comments:
		match_yes = (re.search(r"(?i)^Yay$|^Yes$", comment.body) != None)
		match_no = (re.search(r"(?i)^Nay$|^No$", comment.body) != None)
		yay += match_yes*1
		nay += match_no*1
	print yay, nay
	return yay, nay, sub.subreddit.display_name, sub.title

def post_results(yay, nay, subreddit, counted_in):
	body_text = "Votes in favor: %s \n\nVotes against: %s"%(yay, nay)
	r.submit(subreddit, "Vote result from %s"%counted_in, body_text)
	sleep(2)

def main():
	try:
		running = True
		while running:
			inbox_check()
			sleep(2)
	except:
		sleep(20)

Trying = True
while Trying:
	try:
		USERNAME = _login()
		Trying = False
	except praw.errors.InvalidUserPass:
		print "Invalid Username/password, please try again."

if __name__ == '__main__':
	main()
