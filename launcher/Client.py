import MySQLdb
import sys
import time
import hashlib
from hashlib import md5
from uuid import getnode as get_mac
import os

mac = get_mac()

print mac 

db = MySQLdb.connect(host="localhost",port=3306,user="root",passwd="",db="tthr")
cur = db.cursor()


def hashThis(stri):
	p = hashlib.md5()
	p.update(stri.encode('utf-8'))
	return p.hexdigest()




def register():
	user = raw_input("Username: ")
	print "Note: Passwords can be 20 characters at max."
	passw = raw_input("Password: ")
	confpass = raw_input("Confirm password: ")
	if confpass.lower() != passw.lower():
		print "Passwords do not match!"
		register()
	print "Almost done!"
	email = raw_input("E-mail: ")
	confemail = raw_input("Confirm E-mail: ")
	if email.lower() != confemail.lower():
		print "Emails do not match!"
		register()
	hashedpass = hashThis(passw)
	date = time.strftime("%Y-%m-%d")
	rlmac = str(mac)
	add_user = """INSERT INTO alpha(username,
         password, email, lastlogin, ids, canplay, mac, access)
         VALUES ('"""+ user +"""', '"""+ hashedpass +"""', '"""+ email +"""', '"""+ date +"""', 'none yet', 'True', '"""+ rlmac +"""', 700)""" 
	
	try:
		cur.execute(add_user)
		print "Account made!"
		db.commit()
	except Exception,e:
		print "Username already exists!"
		register()
	
def record(what, who, reason, staff):
	add_user = """INSERT INTO records(what,
	 who, reason, staff)
	 VALUES ('"""+ what +"""', '"""+ who +"""', '"""+ reason +"""', '"""+ staff +"""')""" 
	cur.execute(add_user)
	db.commit()

def ban(person):
	user = raw_input("Please verify this ban with your username: ")
	reason = raw_input("Why did you ban this person?\n")
	record("Ban", person, reason, user)
	cur.execute ("""
	UPDATE alpha
	SET canplay='False'
	WHERE username=%s
	""", (person)) 
	db.commit()
	print "Banned "+ person +". Banned recorded."
def setAccess(person, level):
	user = raw_input("Verify your username: ")
	reason = raw_input("Why did you set this person's access? (lowered it because they aren't staff, made it higher because they're new staff, etc\n")
	record("Set access to "+ str(level) +"", person, reason, user)
	cur.execute ("""
	UPDATE alpha
	SET access=%d
	WHERE username=%s
	""", (level, person))
	db.commit()
	print "Set "+ person +"'s access to "+ str(level) +""
def deleteAccount(person):
	user = raw_input("Enter YOUR username: ")
	reason = raw_input("Why did you delete this person's account?\n")
	record("Deleted account", person, reason, user)
	cur.execute("DELETE FROM `alpha` WHERE username = '"+ person +"'")
	db.commit()

def admLoop(access):
	choice = raw_input("What would you like to do?\n")
	if choice.lower() == 'ban':
		per = raw_input("Who would you like to ban?\n")
		inp = raw_input("Are you sure you want to ban "+ per +"?\nIf this is a wrongful reason, you will be removed from the team.")
		if inp.lower().startswith('y'):
			ban(per)
		elif inp.lower().startswith('n'):
			print "Glad you didn't ban "+ per +" :)"
		else:
			print ""+ inp +" isn't yes or no."
	if choice.lower() == 'setaccess':
		if access != 700:
			print "Sorry, you don't have enough power to setaccess."
		else:
			user = raw_input("Username: ")
			access = int(raw_input("Access :"))
			setAccess(user, access)
	if choice.lower() == 'delete account':
		persontodelete = raw_input("Who do you want to delete?: ")
		delinp = raw_input("Are you ABSOLUTELY sure you want to do this? You can never reverse this. ")
		if delinp.lower() == 'yes':
			print "If you say so..."
			deleteAccount(persontodelete)
		


def login():
	user = raw_input("Username: ")
	passw = raw_input("Password: ")
	date = time.strftime("%Y-%m-%d")
	cur.execute("select * from alpha Where username = '"+ user +"'")
	row = cur.fetchone()
	try:
		realuser = row[0]
		realpass = row[1]
		email = row[2]
		lastlogin = row[3]
		ids = row[4]
		canplay = row[5]
		mac = row[6]
		global access
		access = row[7]
		if canplay == 'True':
			canplay = True
		if canplay == 'False':
			canplay = False
		
	except TypeError:
		print "No username %s, sorry." %user
		login()
	hashedpass = hashThis(passw)
	if hashedpass != realpass:
		print "Incorrect password."
		login()
	else:
		if canplay == False:
			print "You are currently banned, or something has gone wrong with the database."
		if canplay == True:
			print "Last login on %s" %lastlogin
			print "Welcome, %s!" %realuser
			#os.environ['TT_PLAYCOOKIE'] = realuser
			if access >= 600:
				print "Welcome, Server Admin or owner!"
				admLoop(access)
			
def generate_file_sha1(rootdir, filename, blocksize=2**20):
    m = hashlib.md5()
    with open( os.path.join(rootdir, filename) , "rb" ) as f:
        while True:
            buf = f.read(blocksize)
            if not buf:
                break
            m.update( buf )
    return m.hexdigest()

#thinghash = 

def main():
	choice = raw_input("Do you want to register or login?: ")
	if choice.lower() == 'register':
		register()
	elif choice.lower() == 'login':
		login()
	else:
		print ""+ choice +" wasn't a choice."
		main()	
while True:
	main()

db.close()

