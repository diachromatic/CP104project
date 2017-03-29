import discord
import asyncio
import random
import re
import math
import os

client = discord.Client()


def save_to_file(path, text, position):
	if os.path.isfile(path) == False:
		f = open(path, "a")
		f.close()
	if position == "":
		f = open(path, "a")
		f.write(text + "\n")
		f.close()
	else:
		filetext = []
		with open(path, "r+") as f:
			for line in f:
				filetext.append(line)
		i = 0
		written = False
		for line in filetext:
			if "[" + position + "]" in line:
				f = open(path, "w")
				filetext.insert(i + 1, text + "\n")
				f.seek(0)
				f.truncate()
				
				for j in range(len(filetext)):
					f.write(filetext[j])
				written = True
				break
			i += 1
			
		if written == False:
			f = open(path, "a")
			f.write("[" + position + "]\n")
			f.write(text + "\n")
			
		f.close()
		
def save_data(path, array):
	f = open(path, "wb")
	f.write(bytearray(array))
	f.close()
	
def load_data(path, size = 256):
	array = [0] * size
	if os.path.isfile(path) == True:
		f = open(path, "rb")
		i = 0
		data = f.read()
		for byte in data:
			if i < len(array):
				array[i] = byte
			i += 1
		f.close()
	return array
	
def delete_from_file(path, text, position):
	if os.path.isfile(path) == True:
		filetext = []
		inserver = False
		with open(path, "r+") as f:
			for line in f:
					if inserver == False:
						filetext.append(line)
						if "[" + position + "]" in line:
							inserver = True
					else:
						if text not in line:
							filetext.append(line)
						if "[" in line:
							inserver = False
		with open(path, "w") as f:
			for j in range(len(filetext)):
				f.write(filetext[j] + "\n")
			
def delete_all(path, user, tags):
	if os.path.isfile(path) == True:
		filetext = []
		inuser = False
		with open(path, "r+") as f:
			for line in f:
				if inuser == False:
					filetext.append(line.split(' ')[-1].strip())
					if "[" + user + "]" in line:
						inuser = True
				else:
					if tags != "" and tags not in line:
						filetext.append(line.split(' ')[-1].strip())
					if "[" in line:
						inuser = False
							
def find_in_file(path, user, position):
	if position == "":
		inserver = True
	else:
		inserver = False
	with open(path, "r+") as f:
		for line in f:
			if inserver == True:
				if user in line:
					return line
				if position != "" and "[" in line:
					return ""
			if inserver == False:
				if "[" + position + "]" in line:
					inserver = True
			
	return ""

def find_from_id(path, id):
	i = 0
	with open(path, "r+") as f:
		for line in f:
			if i == id:
				return line
			i += 1
	return ""

def find_id_in_file(path, term, caps = False):
	i = 0
	with open(path, "r+") as f:
		for line in f:
			if caps == True:
				line = line.lower()
			if term in line:
				return i
			i += 1
	return 0
		
def fetch_from_file(path, user, tags, fetchall = False):
	filetext = []
	choices = []
	tagslist = []
	sections = []
	multiplesections = False
	tagpointer = 0
	if ";" in user:
		multiplesections = True
		sectionpointer = 1
		sectionnumber = 0
		sections.append(user[0])
		while sectionpointer < len(user):
			if user[sectionpointer] != ";":
				sections[sectionnumber] += user[sectionpointer]
			else:
				sectionnumber += 1
				sectionpointer += 2
				sections.append(user[sectionpointer])
			sectionpointer += 1
	if multiplesections == False:
		sections.append(user)
	
	if tags != "":
		while tagpointer < len(tags):
			tag = get_argument(tags, tagpointer, ' ')
			tagpointer += len(tag) + 1
			tagslist.append(tag)
	
	if user != "":
		userexists = False
		with open(path, "r+") as f:
			for line in f:
				if userexists == True:
					if "[" not in line:
						if tags == "":
							choices.append(line)
						else:
							hastags = True
							for member in tagslist:
								if member not in line:
									hastags = False
									break
							if hastags == True:
								choices.append(line)
					else:
						for section in sections:
							if "[" + section + "]" not in line:
								userexists = False
				for section in sections:
					if "[" + section + "]" in line:
						userexists = True
	else:
		with open(path, "r+") as f:
			for line in f:
				if "[" not in line:
					if tags == "":
						choices.append(line)
					else:
						hastags = True
						for member in tagslist:
							if member not in line:
								hastags = False
								break
						if hastags == True:
							choices.append(line)
	if choices != []:
		if fetchall == True:
			return choices
		else:
			return choices[random.randint(0, len(choices) - 1)]
	else:
		return ""

def fetch_from_database(path, argument0, argument1, argument2):
	filetext = []
	choices = []
	with open(path, "r+") as f:
		for line in f:
			if argument0 in line and argument1 in line and argument2 in line:
				choices.append(line)
	if choices != []:
		return choices[random.randint(0, len(choices) - 1)]
	else:
		return ""
		
def get_argument(string, pointer, separator):
	returnstring = ""
	while pointer < len(string):
		if string[pointer] != separator:
			returnstring += string[pointer]
			pointer += 1
		else:
			break
	return returnstring
	
def get_user(id, server):
	return discord.utils.find(lambda x: x.id == id, discord.utils.find(lambda x: x.id == server, client.servers).members)
	
def ascii_to_text(string):
	newstring = ""
	for character in string:
		newstring += chr(character)
	return newstring
	
def split_string(string, position, separator, type):
	string2 = string[position:]
	newstring = ""
	for character in string2:
		if character != separator:
			newstring += character
		else:
			break
	if type == "int":
		return int(newstring)
	else:
		return newstring

def find_string_separator(string, position, separator):
	string2 = string[position:]
	i = position
	for character in string2:
		if character != separator:
			i += 1
		else:
			break
	i += 1
	return i

def roll_dice(type):
	if type == "chance":
		return random.randint(1, 100)

def find_item_slot(array, item):
	i = 0
	while i < len(array):
		if array[i] == 0 or array[i] == item:
			return i
		i += 1
	return None
		
def get_formula(type, argument1 = 0, argument2 = 0, argument3 = 0, argument4 = 0):
	if type == "damage":
		return round(argument1 / 5 * (1 + random.randint(1,5)) + argument2 - argument3 / 5 * (1 + random.randint(1,5)) + argument4)
	if type == "critical":
		return round(argument1 * (1 + 0.01 * argument2))
		
def skill_database(index, shortname, returndata):
	skillname = ""
	skillshortname = ""
	skillclass = ""
	skilllevel = 0
	skilldescription = ""
	skillpassive = False
	skilltype = ""
	skillhealthcost = 0
	skillmanacost = 0
	skillsecondarymanacost = 0
	
	if shortname == "blackarrow":
		index = 1
	if shortname == "forcedsoul":
		index = 2
	if shortname == "darksigil":
		index = 3
	if shortname == "felinesacrifice":
		index = 4
	if shortname == "meow":
		index = 5
	if shortname == "cutepaws":
		index = 6
	if shortname == "gnaw":
		index = 7
	if shortname == "purify":
		index = 8
	
	if shortname == "innocentgaze":
		index = 9
	if shortname == "end":
		index = 10
	if shortname == "bunnyears":
		index = 11
	if shortname == "bunnybandage":
		index = 12
	if shortname == "hyperlove":
		index = 13
	if shortname == "toughfur":
		index = 14
	if shortname == "arcanerend":
		index = 15
	if shortname == "a":
		index = 16
	if shortname == "a":
		index = 17
	if shortname == "voidgaze":
		index = 18
	if shortname == "toxicblight":
		index = 19
	
	if index == 1:
		skillname = "Black Arrow"
		skillshortname = "blackarrow"
		skillclass = "cat"
		skilllevel = 4
		skilldescription = "Uh... That's a good question. Where does this arrow come from? What is it made of? How does it work? You aren't shooting it from a bow, certainly. So what *are* you shooting it from?\nDeals average magic damage."
		skillsecondarymanacost = 1
	if index == 2:
		skillname = "Forced Soul"
		skillshortname = "forcedsoul"
		skillclass = "cat"
		skilllevel = 8
		skilldescription = "Force departed souls into an enemy's body to poison them."
		skillsecondarymanacost = 2
	if index == 3:
		skillname = "Dark Sigil"
		skillshortname = "darksigil"
		skillclass = "cat"
		skilllevel = 12
		skilldescription = "Strike one opponent with magic, attaching a curse to them. After two turns, the curse detonates, dealing above average magic damage."
		skillsecondarymanacost = 4
	if index == 4:
		skillname = "Feline Sacrifice"
		skillshortname = "felinesacrifice"
		skillclass = "cat"
		skillpassive = True
		skilllevel = 15
		skilldescription = "Perform a dark ritual to bring yourself more in tune with the souls of the departed.\nIncreases SP gained from attacking and defeating enemies."
	if index == 5:
		skillname = "Meow"
		skillshortname = "meow"
		skillclass = "cat"
		skilllevel = 2
		skilldescription = "Make a high-pitched cry at the enemy.\nDeals low magic damage."
		skillmanacost = 20
	if index == 6:
		skillname = "Cute Paws"
		skillshortname = "cutepaws"
		skillclass = "cat"
		skilllevel = 6
		skilldescription = "Cutely swat at the enemy.\nDeals very low damage and confuses opponent at 50% rate."
		skillmanacost = 25
	if index == 7:
		skillname = "Gnaw"
		skillshortname = "gnaw"
		skillclass = "cat"
		skilllevel = 10
		skilldescription = "Bite down hard with magic-imbued fangs.\nDeals both physical and magical damage at an above-average rate."
		skillmanacost = 40
	if index == 8:
		skillname = "Purify"
		skillshortname = "purify"
		skillclass = "cat"
		skilllevel = 14
		skilldescription = "Meditate in order to cleanse the darkness within.\nSacrifices SP to restore Mana."
		skillsecondarymanacost = 2
		
	if index == 9:
		skillname = "Innocent Gaze"
		skillshortname = "innocentgaze"
		skillclass = "bun"
		skilllevel = 1
		skilldescription = "Gaze into an enemy, activating the goodwill in their heart and causing an excess of internal bloodflow.\nDeals low physical damage."
		skillmanacost = 30
		skillsecondarymanacost = 20
	if index == 10:
		skillname = "End"
		skillshortname = "end"
		skillclass = "bun"
		skilllevel = 2
		skilldescription = "Use this skill to end a specificed Guard or Curse. Does not take up a turn."
	if index == 11:
		skillname = "Bunny Ears"
		skillshortname = "bunnyears"
		skillclass = "bun"
		skilllevel = 2
		skilldescription = ""
		skillmanacost = 30
		skillsecondarymanacost = -10
		skilltype = "guard"
	if index == 12:
		skillname = "Bunny Bandage"
		skillshortname = "bunnybandage"
		skillclass = "bun"
		skilllevel = 6
		skilldescription = ""
		skillmanacost = 80
		skillsecondarymanacost = -30
		skilltype = "friendly"
	if index == 13:
		skillname = "Hyper Love"
		skillshortname = "hyperlove"
		skillclass = "bun"
		skilllevel = 10
		skilldescription = ""
		skillmanacost = 60
		skillsecondarymanacost = -20
		skilltype = "guard"
	if index == 14:
		skillname = "Tough Fur"
		skillshortname = "toughfur"
		skillclass = "bun"
		skilllevel = 14
		skilldescription = ""
		skillmanacost = 75
		skillsecondarymanacost = -20
		skilltype = "guard"
	if index == 15:
		skillname = "Arcane Rend"
		skillshortname = "arcanerend"
		skillclass = "bun"
		skilllevel = 1
		skilldescription = "Fabricate a mystical blade that strikes at the soul of an enemy.\nDeals average magical damage."
		skillmanacost = 60
		skillsecondarymanacost = -20
		
	if index == 18:
		skillname = "Void Gaze"
		skillshortname = "voidgaze"
		skillclass = "bun"
		skilllevel = 12
		skilldescription = ""
		skillmanacost = 60
		skillsecondarymanacost = -20
		skilltype = "curse"
	if index == 19:
		skillname = "Toxic Blight"
		skillshortname = "toxicblight"
		skillclass = "bun"
		skilllevel = 15
		skilldescription = ""
		skillmanacost = 90
		skillsecondarymanacost = -20
		skilltype = "curse"
	
	if returndata == "name":
		return skillname
	if returndata == "shortname":
		return skillshortname
	if returndata == "class":
		return skillclass
	if returndata == "level":
		return skilllevel
	if returndata == "index":
		return index
	if returndata == "healthcost":
		return skillhealthcost
	if returndata == "manacost":
		return skillmanacost
	if returndata == "secondarymanacost":
		return skillsecondarymanacost
	if returndata == "description":
		return skilldescription
	if returndata == "passive":
		return skillpassive
	if returndata == "type":
		return skilltype
	
def tcg_database(index, shortname, returndata):
	cardname = ""
	cardshortname = ""
	carddescription = ""
	cardtype = ""
	
	if shortname == "greenslime":
		index = 1
	
	if index == 1:
		cardname = "Green Slime"
		cardshortname = "greenslime"
		carddescription = "Wins the game."
		cardtype = "Monster"
	
	if returndata == "name":
		return cardname
	if returndata == "shortname":
		return cardshortname
	if returndata == "description":
		return carddescription
	if returndata == "type":
		return cardtype
	if returndata == "index":
		return index
	
@client.event
async def automated_message(channel, message):
	sentmessage = "What happened?"
	if message == "unauthorizedchannel":
		sentmessage = "This isn't the place for that."
	if message == "unauthorizeduser":
		sentmessage = "You are not authorized to use this command!"
	if message == "unknownuser":
		sentmessage = "User not found."
	if message == "wrongstate":
		sentmessage = "There's not enough time to do that right now!"
	await client.send_message(channel, sentmessage)
		
@client.event
async def on_ready():
	print("Let's Do Excellent!!")

@client.event
async def on_message(message):
	datadir = "data\\"
	chardir = "character\\"
	individualdir = "individual\\"
	enemiespath = datadir + "database\\bestiary\\enemies.txt"
	itemspath = datadir + "database\\items\\items.txt"
	recipespath = datadir + "database\\items\\recipes.txt"
	statspath = datadir + "database\\class\\stats.txt"
	eventpath = datadir + "database\\event\\event.txt"
	locationspath = datadir + "database\\event\\locations.txt"
	dungeonspath = datadir + "database\\event\\dungeons.txt"
	codexpath = datadir + "database\\codex\\codex.txt"

	alchemyinfopath = "alchemycooldown"

	chardatapath = "chardata"
	partydatapath = "partydata"
	flagdatapath = "flagdata"
	professiondatapath = "professiondata"
	tcgdatapath = "tcgdata"
	encounterdatapath = "encounterdata"
	recipedatapath = "recipedata"
	codexdatapath = "codexdata"
	tcgdatapath = "tcgdata"
	criticaldatapath = "criticaldata"
	individualdatapath = "individualdata"
	teamchannelspath = datadir + "teamchannels.txt"

	# Chardata
	charnamepos = 0
	charclasspos = 10
	charlevelpos = 15
	charexppos = 16
	charATKpos = 18
	charDEFpos = 19
	charMAGpos = 20
	charAGIpos = 21
	charLUKpos = 22
	charALCpos = 23
	charhealthpos = 26
	charmanapos = 28
	charsecondarymanapos = 30
	charstatuspoisonedpos = 32
	charstatusconfusedpos = 33
	charguardbunnyearspos = 34
	charguardhyperlovepos = 35
	charguardtoughfurpos = 36
	charpassiveskillspos = 40
	chardataarray = [0] * 256

	# Partydata
	partyvaliddatapos = 0
	partycollectvalidatorpos = 1
	partyresetvalidpos = 2
	partystatepos = 3
	partyindungeonpos = 4
	partydungeonXpos = 5
	partydungeonYpos = 6
	partyfundspos = 7
	partylocationpos = 9
	partydungeonpos = 10
	partyeventpos = 11
	partyitemspos = 12
	partyitemsquantitypos = 112
	partydataarray = [0] * 256
	partysize = 4
	
	# Flagdata
	flagdataarray = [0] * 256
	flagspos = 0

	# Professiondata
	professiondataarray = [0] * 256
	professionskillspos = 0
	professionexpdatabuffer = 50
	availableprofessions = 2

	# Tcgdata
	decksize = 50
	tcgdeckpos = 0
	tcgcardsownedpos = decksize + 1

	# Criticaldata
	criticaldataarray = [0] * 256
	criticalbonuspos = 0
	
	# Encounterdata
	encounteridpos = 0
	encounterquantitypos = 1
	encounterhealthpos = 2
	encounterexaminedpos = 4
	encounterdarksigilcountdownpos = 5
	encounterdarksigilcasterpos = 6
	encounterstatuspoisonedpos = 7
	encounterstatusconfusedpos = 8
	encountercursetoxicblightpos = 9
	encountercursevoidgazepos = 10
	encounteractionqueuepos = 160
	encounteritemqueuepos = 170
	encounteritemtargetpos = 180
	encounterskillqueuepos = 190
	encounteractiontargetpos = 200
	encounterdataarray = [0] * 256
	encountersize = 4

	# Recipedata
	recipedataarray = [0] * 256
	discoveredrecipepos = 0

	# Codexdata
	codexdataarray = [0] * 256
	discoveredcodexpos = 0

	# Individualdata
	individualnamepos = 0
	individualclasspos = 10
	individuallevelpos = 15
	individualexppos = 16
	individualATKpos = 18
	individualDEFpos = 19
	individualMAGpos = 20
	individualAGIpos = 21
	individualLUKpos = 22
	individualALCpos = 23
	individualhealthpos = 26
	individualmanapos = 28
	individualsecondarymanapos = 30
	individualvaliddatapos = 32
	individualcollecteddatapos = 33
	individualpassiveskillspos = 40
	individualfundspos = 80
	individualprofessionskillspos = 100
	individualdiscoveredcodexpos = 200
	individualdiscoveredrecipepos = 400
	individualdeckpos = 600
	individualcardsownedpos = individualdeckpos + decksize + 1
	individualdataarray = [0] * 1024
	
	
	databuffer = 50
	encounterdatabuffer = 20
	encounterlevelrange = 2

	commandsymbol = '&'
	
	privatemessage = message.channel.is_private
	
	if message.author.name == "The Adventurer":
		print(">>>>>>>>>>>" + str(message.author.name) + ": " + message.content)
	else:
		print(str(message.author.name) + ": " + message.content)
		
	botcommander = False
	if privatemessage == False:
		for role in message.author.roles:
			if role.name == "Bot Commander" or role.name == "Administrators":
				botcommander = True
	
	if message.author.name != "The Adventurer":
			
		lowermessage = message.content.lower()
		nopunctmessage = lowermessage.replace('\'', '')
		nopunctmessage = nopunctmessage.replace(',', '')
		nopunctmessage = nopunctmessage.replace('.', '')
		nopunctmessage = nopunctmessage.replace('!', '')
		nopunctmessage = nopunctmessage.replace('?', '')
		nopunctmessage = nopunctmessage.replace(';', '')
		pointer = 0
		if lowermessage[pointer] == commandsymbol:
			pointer += 1
			command = get_argument(lowermessage, pointer, ' ')
			pointer += len(command) + 1
			basepointer = pointer
			
			msgtime = str(message.timestamp)
			msgyear = int(msgtime[0:4])
			msgmonth = int(msgtime[5:7])
			msgday = int(msgtime[8:10])
			msghour = int(msgtime[11:13])
			msgminute = int(msgtime[14:16])
			msgsecond = int(msgtime[17:19])
			
			teamdata = find_in_file(teamchannelspath, str(message.channel) + " <", str(message.server))
			if teamdata != "":
				teampos = find_string_separator(teamdata, 0, '<')
				team = split_string(teamdata, teampos, '>', "string")
			else:
				team = ""
			if privatemessage == True:
				pathfolder = individualdir
				pathid = message.author.id
				professionskillspos = individualprofessionskillspos
				partysize = 1
				encountersize = 1
				team = "i"
			else:
				pathfolder = chardir
				pathid = str(message.server.id)

			chardatapath_full = datadir + pathfolder + pathid + "\\" + chardatapath + team + pathid + ".dat"
			partydatapath_full = datadir + pathfolder + pathid + "\\" + partydatapath + team + pathid + ".dat"
			flagdatapath_full = datadir + pathfolder + pathid + "\\" + flagdatapath + team + pathid + ".dat"
			professiondatapath_full = datadir + pathfolder + pathid + "\\" + professiondatapath + team + pathid + ".dat"
			tcgdatapath_full = datadir + pathfolder + pathid + "\\" + tcgdatapath + team + pathid + ".dat"
			encounterdatapath_full = datadir + pathfolder + pathid + "\\" + encounterdatapath + team + pathid + ".dat"
			recipedatapath_full = datadir + pathfolder + pathid + "\\" + recipedatapath + team + pathid + ".dat"
			codexdatapath_full = datadir + pathfolder + pathid + "\\" + codexdatapath + team + pathid + ".dat"
			criticaldatapath_full = datadir + pathfolder + pathid + "\\" + criticaldatapath + team + pathid + ".dat"
			individualdatapath_full = datadir + individualdir + message.author.id + "\\" + individualdatapath + "i" + message.author.id + ".dat"

			alchemycooldownpath_full = datadir + pathfolder + pathid + "\\" + alchemyinfopath + team + pathid + ".txt"
			
			if team != "":
				chardataarray = load_data(chardatapath_full)
				partydataarray = load_data(partydatapath_full)
				flagdataarray = load_data(flagdatapath_full)
				professiondataarray = load_data(professiondatapath_full)
				tcgdataarray = load_data(tcgdatapath_full, 512)
				encounterdataarray = load_data(encounterdatapath_full)
				recipedataarray = load_data(recipedatapath_full)
				codexdataarray = load_data(codexdatapath_full)
				criticaldataarray = load_data(criticaldatapath_full)
				individualdataarray = load_data(individualdatapath_full, 1024)
				
				alchemycooldownpath = alchemycooldownpath_full
			
			charname = [""] * partysize
			charclass = [""] * partysize
			charclassfull = [""] * partysize
			charlevel = [1] * partysize
			charATK = [0] * partysize
			charDEF = [0] * partysize
			charMAG = [0] * partysize
			charAGI = [0] * partysize
			charLUK = [0] * partysize
			charALC = [0] * partysize
			charATKmod = [0] * partysize
			charMAGmod = [0] * partysize
			charDEFmod = [0] * partysize
			charhealthmax = [0] * partysize
			charhealth = [0] * partysize
			charmanamax = [0] * partysize
			charmana = [0] * partysize
			charsecondarymanamax = [0] * partysize
			charsecondarymana = [0] * partysize
			charsecondarymananame = [0] * partysize
			charpassiveskills = [[0 for x in range(5)] for y in range(partysize)]
			charstatuspoisoned = [0] * partysize
			charstatusconfused = [0] * partysize
			charguardbunnyears = [0] * partysize
			charguardhyperlove = [0] * partysize
			charguardtoughfur = [0] * partysize
			spincrease = [0] * partysize
			charexpmax = [0] * partysize
			charexp = [0] * partysize
			actionqueue = [0] * partysize
			itemqueue = [0] * partysize
			itemtarget = [0] * partysize
			skillqueue = [0] * partysize
			actiontarget = [0] * partysize
			professionlevel = [1] * availableprofessions
			professionname = ["Scholar", "Duelist"]
			professionexp = [0] * availableprofessions
			professionexpmax = [1] * availableprofessions
			
			bunscaleleft = "Anarchy"
			bunscaleright = "Purity"
			guardbunnyearsmod = 3
			guardtoughfurmod = 6
			cursevoidgazemod = -3
			
			scholarpos = 0
			duelistpos = 1
			
			flags = [0] * 256
			tcgcardsowned = [0] * 256
			tcgdeck = [0] * decksize
			discoveredrecipes = [0] * 256
			discoveredcodex = [0] * 256
			criticalbonus = [0] * 256
			gamereset = False
			
			partyitems = [0] * 100
			partyitemsquantity = [0] * 100
			
			state = "choice"
			funds = 0
			
			partylocation = 1
			partydungeon = 1
			partyevent = 1
			partyindungeon = 0
			partydungeonX = 0
			partydungeonY = 0
			
			infotextdisplay = False
			runeventactions = False
			findencounter = False
			exploretype = "normal"
			
			encounterid = [0]
			encounterquantity = 0
			encounteraveragelevel = 0
			encounterhealth = [0]
			encounterhealthmax = [0]
			encounterexamined = [0]
			encounterstatuspoisoned = [0]
			encounterstatusconfused = [0]
			encountercursetoxicblight = [0]
			encountercursevoidgaze = [0]
			encounterdarksigilcountdown = [0]
			encounterdarksigilcaster = [0]
			
			resetvalid = 0
			validdata = partydataarray[partyvaliddatapos]
			validindividualdata = individualdataarray[individualvaliddatapos]
			collecteddata = individualdataarray[individualcollecteddatapos]
			collectvalidator = random.randint(0, 255)
			
			individualreadonly = True
			selectivereadonly = True
			collectingdata = False
			
			potentialdestination = ""
			
			if validdata == 1:
				partyevent = partydataarray[partyeventpos]
			eventdata = find_from_id(eventpath, partyevent)
			eventdatapos = 0
			eventallowflag = split_string(eventdata, eventdatapos, '|', "string")
			eventallowflag = eventallowflag[2:]
			eventdatapos = find_string_separator(eventdata, eventdatapos, '|')
			eventdisallowflag = split_string(eventdata, eventdatapos, '|', "string")
			eventdisallowflag = eventdisallowflag[2:]
			eventdatapos = find_string_separator(eventdata, eventdatapos, '|')
			eventlocation = split_string(eventdata, eventdatapos, '|', "string")
			eventlocation = eventlocation[2:]
			eventdatapos = find_string_separator(eventdata, eventdatapos, '|')
			eventactionstring = split_string(eventdata, eventdatapos, '|', "string")
			eventdatapos = find_string_separator(eventdata, eventdatapos, '|')
			eventcommandstring = split_string(eventdata, eventdatapos, '|', "string")
			eventdatapos = find_string_separator(eventdata, eventdatapos, '|')
			eventdescription = split_string(eventdata, eventdatapos, '|', "string")
			eventdescription = eventdescription.replace('\\n', '\n')
			eventdatapos = find_string_separator(eventdata, eventdatapos, '|')
			eventactions = [""] * 10
			eventactionarguments = [""] * 10
			eventcommands = [""] * 10
			eventcommandresults = [[""] * 10] * 10
			eventcommandflags = [[""] * 10] * 10
			
			i = 0
			k = 0
			while i < len(eventactionstring):
				if eventactionstring[i] != ";":
					if len(eventactions[k]) < 3:
						eventactions[k] += eventactionstring[i]
					else:
						eventactionarguments[k] += eventactionstring[i]
				else:
					if eventactionarguments[k] != "":
						eventactionarguments[k] = int(eventactionarguments[k])
					k += 1
				i += 1
				
			i = 0
			k = 0
			l = 0
			m = 0
			while i < len(eventcommandstring):
				if l == 0: # Check command text
					if eventcommandstring[i] != ";":
						if eventcommandstring[i] == "(":
							l = 1
						else:
							eventcommands[k] += eventcommandstring[i]
					else:
						if eventcommandresults[k][m] != "":
							eventcommandresults[k][m] = int(eventcommandresults[k][m])
						k += 1
				elif l == 1: # Check command destination
					if eventcommandstring[i] == ")":
						l = 0
					elif eventcommandstring[i] == "[":
						l = 2
					elif eventcommandstring[i] == "]":
						m += 1
					else:
						eventcommandresults[k][m] += eventcommandstring[i]
				elif l == 2:
					if eventcommandstring[i] == ":":
						l = 1
					else:
						eventcommandflags[k][m] += eventcommandstring[i]
					
				i += 1
			
			if validdata == 0:
				command = ""
				charname = ["Anne", "Vex", "Ears", "Red"]
				charclass = ["cat", "kit", "bun", "sqk"]
				
				runeventactions = True
				
				j = 0
				while j < partysize:
					statsstring = find_in_file(statspath, "| " + charclass[j] + " |", "")
					statsstringpos = 0
					statsstringpos = find_string_separator(statsstring, statsstringpos, '[')
					ATKincrease = split_string(statsstring, statsstringpos, ']', "string")
					ATKincrease = int(ATKincrease)
					statsstringpos = find_string_separator(statsstring, statsstringpos, '[')
					DEFincrease = split_string(statsstring, statsstringpos, ']', "string")
					DEFincrease = int(DEFincrease)
					statsstringpos = find_string_separator(statsstring, statsstringpos, '[')
					MAGincrease = split_string(statsstring, statsstringpos, ']', "string")
					MAGincrease = int(MAGincrease)
					statsstringpos = find_string_separator(statsstring, statsstringpos, '[')
					AGIincrease = split_string(statsstring, statsstringpos, ']', "string")
					AGIincrease = int(AGIincrease)
					statsstringpos = find_string_separator(statsstring, statsstringpos, '[')
					LUKincrease = split_string(statsstring, statsstringpos, ']', "string")
					LUKincrease = int(LUKincrease)
					statsstringpos = find_string_separator(statsstring, statsstringpos, '[')
					ALCincrease = split_string(statsstring, statsstringpos, ']', "string")
					ALCincrease = int(ALCincrease)
					
					charATK[j] = ATKincrease
					charMAG[j] = MAGincrease
					charDEF[j] = DEFincrease
					charAGI[j] = AGIincrease
					charLUK[j] = LUKincrease
					charALC[j] = ALCincrease
					
					charlevel[j] = 1
					charexp[j] = 0
					charexpmax[j] = 1
					charhealthmax[j] = round((100 + 20 * charlevel[j]) * (1 + 0.1 * charDEF[j]))
					charmanamax[j] = round((100 + 10 * charlevel[j]) * (1 + 0.3 * charMAG[j]))
					charhealth[j] = charhealthmax[j]
					charmana[j] = charmanamax[j]
					charsecondarymana[j] = 1
					
					if charclass[j] == "cat":
						charsecondarymananame[j] = "Soul Points"
						charsecondarymanamax[j] = 15 + (2 * charlevel[j])
						charsecondarymana[j] = charsecondarymanamax[j]
					elif charclass[j] == "sqk":
						charmanamax[j] = 0
						charmana[j] = 0
					elif charclass[j] == "bun":
						charsecondarymananame[j] = bunscaleright
						charsecondarymanamax[j] = 100
						charsecondarymana[j] = 51
					
					j += 1
			
			if validdata == 1:
				j = 0
				while j < partysize:
					
					if team != "":
						i = 0
						while i < 10:
							if chardataarray[charnamepos + i + j * databuffer] == 0: #and chardataarray[charnamepos + i + 1 + j * databuffer] == 0:
								break
							charname[j] += chr(chardataarray[charnamepos + i + j * databuffer])
							i += 1
						i = 0
						while i < 10:
							if chardataarray[charclasspos + i + j * databuffer] == 0: #and chardataarray[charclasspos + i + 1 + j * databuffer] == 0:
								break
							charclass[j] += chr(chardataarray[charclasspos + i + j * databuffer])
							i += 1
						
						i = 0
						while i < len(charpassiveskills[j]):
							charpassiveskills[j][i] = chardataarray[charpassiveskillspos + j * databuffer]
							i += 1
							
						if charpassiveskills[j][skill_database(0, "felinesacrifice", "index")] == 1:
							spincrease[j] = 2
						
						charlevel[j] = chardataarray[charlevelpos + j * databuffer]
						charATK[j] = chardataarray[charATKpos + j * databuffer]
						charDEF[j] = chardataarray[charDEFpos + j * databuffer]
						charMAG[j] = chardataarray[charMAGpos + j * databuffer]
						charAGI[j] = chardataarray[charAGIpos + j * databuffer]
						charLUK[j] = chardataarray[charLUKpos + j * databuffer]
						charALC[j] = chardataarray[charALCpos + j * databuffer]
						charhealthmax[j] = round((100 + 20 * charlevel[j]) * (1 + 0.1 * (charDEF[j] + charDEFmod[j])))
						charmanamax[j] = round((100 + 10 * charlevel[j]) * (1 + 0.3 * (charMAG[j] + charMAGmod[j])))
						charsecondarymanamax[j] = 0
						charsecondarymananame[j] = ""
						charexpmax[j] = 50 * (5**(charlevel[j] - 1))
						actionqueue[j] = encounterdataarray[encounteractionqueuepos + j]
						itemqueue[j] = encounterdataarray[encounteritemqueuepos + j]
						itemtarget[j] = encounterdataarray[encounteritemtargetpos + j]
						skillqueue[j] = encounterdataarray[encounterskillqueuepos + j]
						actiontarget[j] = encounterdataarray[encounteractiontargetpos + j]
						
						if charclass[j] == "cat":
							charclassfull[j] = "Black Cat"
							charsecondarymananame[j] = "Soul Points"
							charsecondarymanamax[j] = 15 + (2 * charlevel[j])
						elif charclass[j] == "kit":
							charclassfull[j] = "Kitsune"
						elif charclass[j] == "bun":
							charclassfull[j] = "Esper Bunny"
							charsecondarymananame[j] = bunscaleright
							charsecondarymanamax[j] = 100
						elif charclass[j] == "sqk":
							charclassfull[j] = "Squirrel Knight"
							charmanamax[j] = 0
							charmana[j] = 0
						else:
							charclassfull[j] = "Human"
						exparray = [chardataarray[charexppos + j * databuffer], chardataarray[charexppos + 1 + j * databuffer]]
						charexp[j] = int.from_bytes(exparray, "little")
						healtharray = [chardataarray[charhealthpos + j * databuffer], chardataarray[charhealthpos + 1 + j * databuffer]]
						charhealth[j] = int.from_bytes(healtharray, "little")
						manaarray = [chardataarray[charmanapos + j * databuffer], chardataarray[charmanapos + 1 + j * databuffer]]
						charmana[j] = int.from_bytes(manaarray, "little")
						secondarymanaarray = [chardataarray[charsecondarymanapos + j * databuffer], chardataarray[charsecondarymanapos + 1 + j * databuffer]]
						charsecondarymana[j] = int.from_bytes(secondarymanaarray, "little")
						
						charstatuspoisoned[j] = chardataarray[charstatuspoisonedpos + j * databuffer]
						charstatusconfused[j] = chardataarray[charstatusconfusedpos + j * databuffer]
						charguardbunnyears[j] = chardataarray[charguardbunnyearspos + j * databuffer]
						charguardhyperlove[j] = chardataarray[charguardhyperlovepos + j * databuffer]
						charguardtoughfur[j] = chardataarray[charguardtoughfurpos + j * databuffer]
						
						if charguardbunnyears[j] == 1:
							charATKmod[j] += guardbunnyearsmod
							charMAGmod[j] += guardbunnyearsmod
						
						if charhealth[j] > charhealthmax[j]:
							charhealth[j] = charhealthmax[j]
						if charmana[j] > charmanamax[j]:
							charmana[j] = charmanamax[j]
						if charsecondarymana[j] > charsecondarymanamax[j]:
							charsecondarymana[j] = charsecondarymanamax[j]
					j += 1
				
				averagepartylevel = 0
				j = 0
				while j < partysize:
					averagepartylevel += charlevel[j]
					j += 1
				averagepartylevel /= partysize
				
				encounterquantity = encounterdataarray[encounterquantitypos]
				encounterid = [0] * encounterquantity
				encounter = [""] * encounterquantity
				encounterhealth = [0] * encounterquantity
				encounterhealthmax = [0] * encounterquantity
				encounterexamined = [0] * encounterquantity
				encounterstatuspoisoned = [0] * encounterquantity
				encounterstatusconfused = [0] * encounterquantity
				encountercursetoxicblight = [0] * encounterquantity
				encountercursevoidgaze = [0] * encounterquantity
				encounterdarksigilcountdown = [0] * encounterquantity
				encounterdarksigilcaster = [0] * encounterquantity
				
				encountername = [""] * encounterquantity
				encounterlevel = [1] * encounterquantity
				encounterfamily = [""] * encounterquantity
				encounterspecies = [""] * encounterquantity
				encounterATK = [0] * encounterquantity
				encounterDEF = [0] * encounterquantity
				encounterRES = [0] * encounterquantity
				encounterAGI = [0] * encounterquantity
				encounterspecials = [""] * encounterquantity
				encountercardrarity = [0] * encounterquantity
				
				encounterAGImod = [0] * encounterquantity
				encounterDEFmod = [0] * encounterquantity
				
				j = 0
				while j < encounterquantity:
					encounterid[j] = encounterdataarray[encounteridpos + encounterdatabuffer * j]
					encounterexamined[j] = encounterdataarray[encounterexaminedpos + encounterdatabuffer * j]
					encounterhealth[j] = encounterdataarray[encounterhealthpos + encounterdatabuffer * j]
					encounterhealthmax[j] = 100
					j += 1

				state = ""
				
				collectvalidator = partydataarray[partycollectvalidatorpos]
				
				j = 0
				while j < len(flags):
					flags[j] = flagdataarray[j]
					j += 1
			
				if partydataarray[partystatepos] == 0:
					state = "normal"
				elif partydataarray[partystatepos] == 1:
					state = "choice"
				elif partydataarray[partystatepos] == 2:
					state = "battle"
				else:
					state = "dungeon"
				
				resetvalid = partydataarray[partyresetvalidpos]
				
				partyindungeon = partydataarray[partyindungeonpos]
				partydungeonX = partydataarray[partydungeonXpos]
				partydungeonY = partydataarray[partydungeonYpos]
				
				partylocation = partydataarray[partylocationpos]
				locationdata = find_from_id(locationspath, partylocation)
				locationdatapos = 0
				locationname = split_string(locationdata, locationdatapos, '|', "string")
				locationdatapos = find_string_separator(locationdata, locationdatapos, '|')
				locationshortname = split_string(locationdata, locationdatapos, '|', "string")
				locationdatapos = find_string_separator(locationdata, locationdatapos, '|')
				locationdescription = split_string(locationdata, locationdatapos, '|', "string")
				locationdatapos = find_string_separator(locationdata, locationdatapos, '|')
				locationmaxlevel = split_string(locationdata, locationdatapos, '|', "string")
				locationdatapos = find_string_separator(locationdata, locationdatapos, '|')
				locationnativespecies = split_string(locationdata, locationdatapos, '|', "string")
				locationdatapos = find_string_separator(locationdata, locationdatapos, '|')
				locationdestinations = split_string(locationdata, locationdatapos, '|', "string")
				locationdatapos = find_string_separator(locationdata, locationdatapos, '|')
				if locationmaxlevel != "":
					locationmaxlevel = int(locationmaxlevel)
				locationactions = [""] * 10
				i = 0
				while locationdatapos < len(locationdata):
					locationactions[i] = split_string(locationdata, locationdatapos, ';', "string").replace(' ', '')
					locationdatapos = find_string_separator(locationdata, locationdatapos, ';')
					i += 1
				
				locationnativespecieslist = []
				i = 1
				while i < len(locationnativespecies):
					newspecies = split_string(locationnativespecies, i, ';', "string")
					i = find_string_separator(locationnativespecies, i, ';')
					if newspecies.rstrip() != "":
						locationnativespecieslist.append(newspecies)
					else:
						break
				
				locationdestinationslist = []
				i = 1
				while i < len(locationdestinations):
					newdestination = split_string(locationdestinations, i, ';', "string")
					i = find_string_separator(locationdestinations, i, ';')
					if newdestination.rstrip() != "":
						locationdestinationslist.append(int(newdestination))
					else:
						break
				
				partydungeon = partydataarray[partydungeonpos]
				
				fundsarray = [partydataarray[partyfundspos], partydataarray[partyfundspos + 1]]
				funds = int.from_bytes(fundsarray, "little")
				
				i = 0
				while i < availableprofessions:
					professionlevel[i] = professiondataarray[i]
					professionexpmax[i] = round(50 * (5**(professionlevel[i] - 1)))
					professionexparray = [professiondataarray[(i * 2) + professionexpdatabuffer], professiondataarray[(i * 2) + professionexpdatabuffer + 1]]
					professionexp[i] = int.from_bytes(professionexparray, "little")
					i += 1
				
				i = 0
				while i < len(tcgdeck):
					tcgdeck[i] = tcgdataarray[tcgdeckpos + i]
					i += 1
				
				i = 0
				while i < len(tcgcardsowned):
					tcgcardsowned[i] = tcgdataarray[tcgcardsownedpos + i]
					i += 1
				
				i = 0
				while i < 100:
					partyitems[i] = partydataarray[partyitemspos + i]
					partyitemsquantity[i] = partydataarray[partyitemsquantitypos + i]
					i += 1
				
				i = 0
				while i < len(discoveredrecipes):
					discoveredrecipes[i] = recipedataarray[discoveredrecipepos + i]
					if privatemessage == True:
						recipedata = individualdataarray[individualdiscoveredrecipepos + i]
						if recipedata == 1:
							discoveredrecipes[i] = 1
					i += 1
				
				i = 0
				while i < len(discoveredcodex):
					discoveredcodex[i] = codexdataarray[discoveredcodexpos + i]
					if privatemessage == True:
						codexdata = individualdataarray[individualdiscoveredcodexpos + i]
						if codexdata == 1:
							discoveredcodex[i] = 1
					i += 1
				
				i = 0
				while i < len(criticalbonus):
					criticalbonus[i] = criticaldataarray[criticalbonuspos + i]
					i += 1
				
				if state == "battle":
					encounterspecialslist = [[] for y in range(encounterquantity)]
					j = 0
					while j < encounterquantity:
						encounter[j] = find_from_id(enemiespath, encounterid[j])
						
						encounterpos = 0
						encountername[j] = split_string(encounter[j], encounterpos, '|', "string")
						encounterpos = find_string_separator(encounter[j], encounterpos, '|')
						encounterlevel[j] = split_string(encounter[j], encounterpos, '|', "string")
						encounterpos = find_string_separator(encounter[j], encounterpos, '|')
						encounterfamily[j] = split_string(encounter[j], encounterpos, '|', "string")
						encounterpos = find_string_separator(encounter[j], encounterpos, '|')
						encounterspecies[j] = split_string(encounter[j], encounterpos, '|', "string")
						encounterpos = find_string_separator(encounter[j], encounterpos, '|')				
						encounterATK[j] = split_string(encounter[j], encounterpos, '|', "string")
						encounterpos = find_string_separator(encounter[j], encounterpos, '|')
						encounterDEF[j] = split_string(encounter[j], encounterpos, '|', "string")
						encounterpos = find_string_separator(encounter[j], encounterpos, '|')
						encounterRES[j] = split_string(encounter[j], encounterpos, '|', "string")
						encounterpos = find_string_separator(encounter[j], encounterpos, '|')
						encounterAGI[j] = split_string(encounter[j], encounterpos, '|', "string")
						encounterpos = find_string_separator(encounter[j], encounterpos, '|')
						encounterspecials[j] = split_string(encounter[j], encounterpos, '|', "string")
						encounterpos = find_string_separator(encounter[j], encounterpos, '|')
						encountercardrarity[j] = split_string(encounter[j], encounterpos, '|', "string")
						encounterpos = find_string_separator(encounter[j], encounterpos, '|')
						
						if encounterspecials[j] != "":
							encounterspecialspos = 0
							while encounterspecialspos < len(encounterspecials[j]):
								encounterspecialslist[j].append(split_string(encounterspecials[j], encounterspecialspos, ";"))
								encounterspecialspos = find_string_separator(encounterspecials[j], encounterspecialspos, ';')
						
						encounterATK[j] = int(encounterATK[j])
						encounterDEF[j] = int(encounterDEF[j])
						encounterRES[j] = int(encounterRES[j])
						encounterAGI[j] = int(encounterAGI[j])
						encounterlevel[j] = int(encounterlevel[j])
						encountercardrarity[j] = int(encountercardrarity[j])
						
						encounteraveragelevel += encounterlevel[j]
						
						encounterATK[j] = round((8 + (encounterlevel[j] - 1) * 3 + random.randint(-2, 2))) * (1 + (0.1 * encounterATK[j]))
						encounterDEF[j] = round((8 + (encounterlevel[j] - 1) * 3 + random.randint(-2, 2))) * (1 + (0.1 * encounterDEF[j]))
						encounterRES[j] = round((8 + (encounterlevel[j] - 1) * 3 + random.randint(-2, 2))) * (1 + (0.1 * encounterRES[j]))
						encounterAGI[j] = round((8 + (encounterlevel[j] - 1) * 3 + random.randint(-2, 2))) * (1 + (0.1 * encounterAGI[j]))
						
						encounterstatuspoisoned[j] = encounterdataarray[encounterstatuspoisonedpos + encounterdatabuffer * j]
						encounterstatusconfused[j] = encounterdataarray[encounterstatusconfusedpos + encounterdatabuffer * j]
						encountercursetoxicblight[j] = encounterdataarray[encountercursetoxicblightpos + encounterdatabuffer * j]
						encountercursevoidgaze[j] = encounterdataarray[encountercursevoidgazepos + encounterdatabuffer * j]
						encounterdarksigilcountdown[j] = encounterdataarray[encounterdarksigilcountdownpos + encounterdatabuffer * j]
						encounterdarksigilcaster[j] = encounterdataarray[encounterdarksigilcasterpos + encounterdatabuffer * j]
						
						if encountercursevoidgaze[j] == 1:
							encounterAGImod[j] = cursevoidgazemod
							encounterDEFmod[j] = cursevoidgazemod
							
						encounterhealthmax[j] = round((100 + 20 * encounterlevel[j]) * (1 + 0.1 * (encounterDEF[j] + encounterDEFmod[j])))
						
						encounterhealtharray = [encounterdataarray[encounterhealthpos + encounterdatabuffer * j], encounterdataarray[encounterhealthpos + 1 + encounterdatabuffer * j]]
						encounterhealth[j] = int.from_bytes(encounterhealtharray, "little")
						
						j += 1
					
					if encounterquantity > 0:
						encounteraveragelevel /= encounterquantity
					defending = [False] * partysize
			
			validdata = 1
			
			if privatemessage == True:
				if validindividualdata == 0:
					charclass[0] = "cat"
					charclassfull[0] = "Black Cat"
					charname[0] = "Anne"
					
					statsstring = find_in_file(statspath, "| " + charclass[0] + " |", "")
					statsstringpos = 0
					statsstringpos = find_string_separator(statsstring, statsstringpos, '[')
					ATKincrease = split_string(statsstring, statsstringpos, ']', "string")
					ATKincrease = int(ATKincrease)
					statsstringpos = find_string_separator(statsstring, statsstringpos, '[')
					DEFincrease = split_string(statsstring, statsstringpos, ']', "string")
					DEFincrease = int(DEFincrease)
					statsstringpos = find_string_separator(statsstring, statsstringpos, '[')
					MAGincrease = split_string(statsstring, statsstringpos, ']', "string")
					MAGincrease = int(MAGincrease)
					statsstringpos = find_string_separator(statsstring, statsstringpos, '[')
					AGIincrease = split_string(statsstring, statsstringpos, ']', "string")
					AGIincrease = int(AGIincrease)
					statsstringpos = find_string_separator(statsstring, statsstringpos, '[')
					LUKincrease = split_string(statsstring, statsstringpos, ']', "string")
					LUKincrease = int(LUKincrease)
					statsstringpos = find_string_separator(statsstring, statsstringpos, '[')
					ALCincrease = split_string(statsstring, statsstringpos, ']', "string")
					ALCincrease = int(ALCincrease)
					
					charATK[0] = ATKincrease
					charMAG[0] = MAGincrease
					charDEF[0] = DEFincrease
					charAGI[0] = AGIincrease
					charLUK[0] = LUKincrease
					charALC[0] = ALCincrease
					
					charlevel[0] = 1
					charexp[0] = 0
					charexpmax[0] = 1
					charhealthmax[0] = round((100 + 20 * charlevel[0]) * (1 + 0.1 * charDEF[0]))
					charmanamax[0] = round((100 + 10 * charlevel[0]) * (1 + 0.3 * charMAG[0]))
					charhealth[0] = charhealthmax[0]
					charmana[0] = charmanamax[0]
					charsecondarymana[0] = 1
					
					charsecondarymananame[0] = "Soul Points"
					charsecondarymanamax[0] = 15 + (2 * charlevel[0])
					charsecondarymana[0] = charsecondarymanamax[0]
					
					command = ""
					individualreadonly = False
					
					await client.send_message(message.channel, "Initializing personal data. Your class has been set to " + charclassfull[0] + ". Your name is " + charname[0] + ".\nYour class and name can be changed at any time, by using **" + commandsymbol + "class** and **" + commandsymbol + "name** respectively.")
				
			validindividualdata = 1
			
			
			# Commands
			# States: "normal" - regular commands can be used, "choice" - commands are mostly restricted to choices based on current event, "battle" - commands are mostly restricted to battle choices
			pointer = basepointer
			if state == "normal":
				if team != "":
					if command == "class":
						if privatemessage == True:
							argument1 = get_argument(lowermessage, pointer, ' ')
							pointer += len(argument1) + 1
							
							if argument1 == "cat" or argument1 == "bun" or argument1 == "kit" or argument1 == "sqk":
								charclass[0] = argument1
								
								statsstring = find_in_file(statspath, "| " + charclass[j] + " |", "")
								statsstringpos = 0
								statsstringpos = find_string_separator(statsstring, statsstringpos, '[')
								ATKincrease = split_string(statsstring, statsstringpos, ']', "string")
								ATKincrease = int(ATKincrease)
								statsstringpos = find_string_separator(statsstring, statsstringpos, '[')
								DEFincrease = split_string(statsstring, statsstringpos, ']', "string")
								DEFincrease = int(DEFincrease)
								statsstringpos = find_string_separator(statsstring, statsstringpos, '[')
								MAGincrease = split_string(statsstring, statsstringpos, ']', "string")
								MAGincrease = int(MAGincrease)
								statsstringpos = find_string_separator(statsstring, statsstringpos, '[')
								AGIincrease = split_string(statsstring, statsstringpos, ']', "string")
								AGIincrease = int(AGIincrease)
								statsstringpos = find_string_separator(statsstring, statsstringpos, '[')
								LUKincrease = split_string(statsstring, statsstringpos, ']', "string")
								LUKincrease = int(LUKincrease)
								statsstringpos = find_string_separator(statsstring, statsstringpos, '[')
								ALCincrease = split_string(statsstring, statsstringpos, ']', "string")
								ALCincrease = int(ALCincrease)
								
								charATK[0] = ATKincrease
								charDEF[0] = DEFincrease
								charMAG[0] = MAGincrease
								charAGI[0] = AGIincrease
								charLUK[0] = LUKincrease
								charALC[0] = ALCincrease
								
								statsstring = find_in_file(statspath, "| " + charclass[0] + " |", "")
								statsstringpos = 0
								statsstringpos = find_string_separator(statsstring, statsstringpos, '(')
								ATKincrease = split_string(statsstring, statsstringpos, ')', "string")
								ATKincrease = int(ATKincrease)
								statsstringpos = find_string_separator(statsstring, statsstringpos, '(')
								DEFincrease = split_string(statsstring, statsstringpos, ')', "string")
								DEFincrease = int(DEFincrease)
								statsstringpos = find_string_separator(statsstring, statsstringpos, '(')
								MAGincrease = split_string(statsstring, statsstringpos, ')', "string")
								MAGincrease = int(MAGincrease)
								statsstringpos = find_string_separator(statsstring, statsstringpos, '(')
								AGIincrease = split_string(statsstring, statsstringpos, ')', "string")
								AGIincrease = int(AGIincrease)
								statsstringpos = find_string_separator(statsstring, statsstringpos, '(')
								LUKincrease = split_string(statsstring, statsstringpos, ')', "string")
								LUKincrease = int(LUKincrease)
								statsstringpos = find_string_separator(statsstring, statsstringpos, '(')
								ALCincrease = split_string(statsstring, statsstringpos, ')', "string")
								ALCincrease = int(ALCincrease)
								
								charATK[0] += ATKincrease * (charlevel[0] - 1)
								charDEF[0] += DEFincrease * (charlevel[0] - 1)
								charMAG[0] += MAGincrease * (charlevel[0] - 1)
								charAGI[0] += AGIincrease * (charlevel[0] - 1)
								charLUK[0] += LUKincrease * (charlevel[0] - 1)
								charALC[0] += ALCincrease * (charlevel[0] - 1)
								
								selectivereadonly = False
								
								await client.send_message(message.channel, "Your class has been changed.")
							else:
								await client.send_message(message.channel, "If you would like to change your class, type \"cat\" for \"Black Cat\"; \"bun\" for \"Esper Bunny\"; \"kit\" for \"Kitsune\"; or \"sqk\" for \"Squirrel Knight\".")
							
					if command == "name":
						if privatemessage == True:
							argument1 = get_argument(message.content, pointer, ' ')
							pointer += len(argument1) + 1
							
							if argument1 != "":
								charname[0] = argument1
								selectivereadonly = False
								await client.send_message(message.channel, "Your name has been changed to " + charname[0] + ".")
							else:
								await client.send_message(message.channel, "Please provide a name.")
								
					if command == "collect":
						if privatemessage == False:
							if individualdataarray[individualcollecteddatapos] != collectvalidator:
								if individualdataarray[individualvaliddatapos] == 1:
									argument1 = get_argument(lowermessage, pointer, ' ')
									pointer += len(argument1) + 1
									
									if argument1 == "confirm":
										individualreadonly = False
										individualdataarray[individualcollecteddatapos] = collectvalidator
										collectingdata = True
										await client.send_message(message.channel, "Game data added to personal data!")
									else:
										await client.send_message(message.channel, "This command will add data from the current game to your personal data. You can only do this once per game. To confirm this, use \"**" + commandsymbol + "collect confirm**\".")
								else:
									await client.send_message(message.channel, "You don't have any personal data! Please use \"**" + commandsymbol + "**\" or any other command in a private message to create your personal data.")

								
								
					
					if command == "explore":
						findencounter = True
						exploretype = "normal"
						state = "battle"
					
					if command == "travel":
						argument1 = get_argument(message.content, pointer, ' ')
						pointer += len(argument1) + 1
						validlocation = False
						destination = find_id_in_file(locationspath, argument1)
						
						for member in locationdestinationslist:
							if destination == member:
								validlocation = True
								break
						
						if validlocation == True and destination != 0:
							if random.randint(1, 10) > 7:
								findencounter = True
								exploretype = "travel"
								potentialdestintion = destination
								state = "battle"
							else:
								partylocation = destination
								newlocationdata = find_from_id(locationspath, partylocation)
								newlocationname = split_string(newlocationdata, 0, "|", "string").rstrip()
								infotextdisplay = True
								await client.send_message(message.channel, "You travel to " + newlocationname + ".")
						else:
							await client.send_message(message.channel, "You cannot travel there!")
					
					if command == "sleep":
						innprice = 50
						if funds >= innprice:
							funds -= innprice
							i = 0
							while i < partysize:
								charhealth[i] = charhealthmax[i]
								charmana[i] = charmanamax[i]
								charsecondarymana[i] = charsecondarymanamax[i]
								if charclass[i] == "bun":
									charsecondarymana[i] = 51
								i += 1
							await client.send_message(message.channel, "You pay the innkeep " + str(innprice) + " Gold and sleep in your rooms. You wake up much later, feeling refreshed.")
						else:
							await client.send_message(message.channel, "You haven't got the cash! It costs " + str(innprice) + " Gold to stay at this inn.")
							
					if command == "cards":
						argument1 = get_argument(lowermessage, pointer, ' ')
						pointer += len(argument1) + 1
						
						if argument1 == "":
							cardsstring = "List of cards:\n"
							
							i = 0
							while i < len(tcgcardsowned):
								cardname = tcg_database(i + 1, "", "name")
								cardshortname = tcg_database(i + 1, "", "shortname")
								cardtype = tcg_database(i + 1, "", "type")
								
								if tcgcardsowned[i] == 0:
									newcardname = ""
									newcardshortname = ""
									newcardtype = ""
									l = 0
									while l < len(cardname) + 50:
										if l < len(cardname):
											if cardname[l] == ' ':
												newcardname += cardname[l]
											else:
												newcardname += '?'
										if l < len(cardshortname):
											if cardshortname[l] == ' ':
												newcardshortname += cardshortname[l]
											else:
												newcardshortname += '?'
										if l < len(cardtype):
											if cardtype[l] == ' ':
												newcardtype += cardtype[l]
											else:
												newcardtype += '?'
										l += 1
										
									cardname = newcardname
									cardshortname = newcardshortname
									cardtype = newcardtype
									
								if cardname != "":
									cardsstring += "\n" + cardname + " [" + cardshortname + "] | " + cardtype
									if tcgcardsowned[i] > 0:
										cardsstring += " | " + str(tcgcardsowned[i]) + " owned\n"
								i += 1
							
							await client.send_message(message.channel, cardsstring)
						
						else:
							cardname = tcg_database(0, argument1, "name")
							cardshortname = tcg_database(0, argument1, "shortname")
							carddescription = tcg_database(0, argument1, "description")
							cardindex = tcg_database(0, argument1, "index")
							cardtype = tcg_database(0, argument1, "type")
							
							if cardname != "" and tcgcardsowned[cardindex - 1] > 0:
								cardsstring = cardname + " [" + cardshortname + "] | " + cardtype + " | " + str(tcgcardsowned[cardindex - 1]) + " owned\n" + carddescription
								await client.send_message(message.channel, cardsstring)
							else:
								await client.send_message(message.channel, "You don't have that card!")
								
					if command == "deck":
						argument1 = get_argument(lowermessage, pointer, ' ')
						pointer += len(argument1) + 1
						argument2 = get_argument(lowermessage, pointer, ' ')
						pointer += len(argument2) + 1
						
						if argument1 == "":
							cardsstring = "Cards currently in deck:\n"
							i = 0
							while i < decksize:
								cardname = tcg_database(tcgdeck[i], "", "name")
								cardshortname = tcg_database(tcgdeck[i], "", "shortname")
								carddescription = tcg_database(tcgdeck[i], "", "description")
								cardindex = tcg_database(tcgdeck[i], "", "index")
								
								if tcgdeck[i] != 0:
									cardsstring += "\n" + cardname + " [" + cardshortname + "]"
								i += 1
						
						if argument1 == "add":
							cardindex = tcg_database(0, argument2, "index")
							cardname = tcg_database(cardindex, "", "name")
							
							if cardindex != 0 and tcgcardsowned[cardindex - 1] > 0:
								cardsindeck = 0
								i = 0
								while i < decksize:
									if tcgdeck[i] == cardindex:
										cardsindeck += 1
									if tcgdeck[i] == 0:
										if tcgcardsowned[cardindex - 1] > cardsindeck:
											if cardsindeck < 4:
												tcgdeck[i] = int(argument2)
												await client.send_message(message.channel, "Added " + cardname + " to deck!")
											else:
												await client.send_message(message.channel, "You already have too many of that card in your deck!")
										else:
											await client.send_message(message.channel, "You don't have any more of that card!")
										break
									i += 1
							else:
								await client.send_message(message.channel, "You don't have that card!")
						
						if argument1 == "remove" or argument1 == "removeall":
							cardindex = tcg_database(0, argument2, "index")
							cardname = tcg_database(cardindex, "", "name")
							
							if cardindex != 0:
								i = 0
								while i < decksize:
									if tcgdeck[i] == cardindex:
										tcgdeck[i] = 0
										if argument1 == "remove":
											await client.send_message(message.channel, "Removed " + cardname + " from deck!")
											break
									i += 1
								if argument1 == "removeall":
									await client.send_message(message.channel, "Removed all copies of " + cardname + " from deck!")
							else:
								await client.send_message(message.channel, "That card is not in your deck!")
								
						if argument1 == "getcode":
							deckstring = ""
							i = 0
							while i < decksize:
								cardstring = ""
								if tcgdeck[i] < 10:
									cardstring += "0"
								if tcgdeck[i] < 100:
									cardstring += "0"
								cardstring += str(tcgdeck[i])
								deckstring += cardstring
								i += 1
							await client.send_message(message.channel, "Copy this code to automatically load an old card deck:\n" + deckstring)
						
						if argument1 == "loadcode":
							if argument2 != "":
								deckcodeentries = [0] * decksize
								validcode = True
								i = 0
								while i < decksize:
									deckcodeentry = argument2[i * 3:i * 3 + 3]
									if deckcodeentry.isdigit() and len(deckcodeentry) == 3:
										deckcodeentries[i] = int(deckcodeentry)
									else:
										validcode = False
										break
									i += 1
								if len(deckcodeentries) == decksize:
									validcode = False
									
								if validcode == True:
									tcgdeck = deckcodeentries
								else:
									await client.send_message(message.channel, "Please input a valid code!")	
							else:
								await client.send_message(message.channel, "Please input a valid code!")
						
					j = 0
					while j < partysize:
						if command == charname[j].lower():
							argument1 = get_argument(lowermessage, pointer, ' ')
							pointer += len(argument1) + 1
							
							if argument1 == "mix" or argument1 == "recipe":
								args = [""] * 3
								recipeknown = True
								
								with open(alchemycooldownpath, "r+") as f:
									for line in f:
										time = ""
										name = ""
										stringpos = 0
										while stringpos < len(line) - 1:
											if line[stringpos + 1] != "~":
												time += line[stringpos]
												stringpos += 1
											else:
												break
										stringpos += 3
										while stringpos < len(line):
											name += line[stringpos]
											stringpos += 1
										name = name.replace('\n', '')
										if time != "":
											year = int(time[0:4])
											month = int(time[5:7])
											day = int(time[8:10])
											hour = int(time[11:13])
											minute = int(time[14:16])
											if msgyear > year or (msgyear == year and msgmonth > month) or (msgyear == year and msgmonth == month and msgday > day) or (msgyear == year and msgmonth == month and msgday == day and msghour > hour) or (msgyear == year and msgmonth == month and msgday == day and msghour == hour and msgminute > minute):
												delete_from_file(alchemycooldownpath, line, "")
								alchemycooldown = find_in_file(alchemycooldownpath, charname[j], "")
								
								remainingcooldown = 0
								if alchemycooldown != "":
									alchemycooldown = split_string(alchemycooldown, 0, "~", "string")
									year = int(alchemycooldown[0:4])
									month = int(alchemycooldown[5:7])
									day = int(alchemycooldown[8:10])
									hour = int(alchemycooldown[11:13])
									minute = int(alchemycooldown[14:16])
									second = int(alchemycooldown[17:19])
									
									msgfullminutes = msghour * 60 + msgminute
									fullminutes = hour * 60 + minute
									remainingcooldown = fullminutes - msgfullminutes
									
								if remainingcooldown <= 0:
									if argument1 == "mix":
										usingrecipe = False
										args[0] = get_argument(lowermessage, pointer, ' ')
										pointer += len(args[0]) + 1 # Material 1
										args[1] = get_argument(lowermessage, pointer, ' ')
										pointer += len(args[1]) + 1 # Material 2
										args[2] = get_argument(lowermessage, pointer, ' ')
										pointer += len(args[2]) + 1 # Material 3
									else:
										usingrecipe = True
										argument2 = get_argument(lowermessage, pointer, ' ')
										pointer += len(argument2) + 1 # Recipe
										recipedata = fetch_from_database(recipespath, "|" + argument2 + "|", "", "")
										recipedatapos = 0
										recipeid = split_string(recipedata, recipedatapos, '|', "string")
										recipeid = int(recipeid)
										recipedatapos = find_string_separator(recipedata, recipedatapos, '|')
										recipetier = split_string(recipedata, recipedatapos, '|', "string")
										recipedatapos = find_string_separator(recipedata, recipedatapos, '|')
										recipematerials = split_string(recipedata, recipedatapos, '|', "string")
										recipedatapos = 0
										if discoveredrecipes[recipeid - 2] == 0:
											recipeknown = False
											await client.send_message(message.channel, "You don't know the recipe for this item!")
										k = 0
										while k < len(args):
											args[k] = split_string(recipematerials, recipedatapos, ';', "string")
											recipedatapos = find_string_separator(recipematerials, recipedatapos, ';')
											k += 1
										
									itemsvalid = True
									
									if recipeknown == True:
										if args[0] != "" and args[1] != "":
											
											materialstring = args[0] + ";" + args[1]
											if args[2] != "":
												materialstring += ";" + args[2]
											
											for member in args:
												itemdata = find_id_in_file(itemspath, member)
												if itemdata != 0:
													itemname = split_string(find_from_id(itemspath, itemdata), 0, '|', "string")
													
													k = 0
													for partyitem in partyitems:
														if partyitem == itemdata:
															if partyitemsquantity[k] <= 0:
																itemsvalid = False
																break
														k += 1
														
												else:
													if member != "":
														await client.send_message(message.channel, "\"" + member + "\" not recognized as an item.")
														itemsvalid = False
														break
											
											if itemsvalid == True:
												for member in args:
													itemdata = find_id_in_file(itemspath, member)
													if itemdata != 0:
														itemname = split_string(find_from_id(itemspath, itemdata), 0, '|', "string")
														
														k = 0
														for partyitem in partyitems:
															if partyitem == itemdata:
																partyitemsquantity[k] -= 1
																if partyitemsquantity[k] <= 0:
																	partyitems[k] = 0
																break
															k += 1
												
												recipedata = fetch_from_database(recipespath, materialstring, "", "")
												recipeid = find_id_in_file(recipespath, recipedata)
												newmsgyear = msgyear
												newmsgmonth = msgmonth
												newmsgday = msgday
												newmsghour = msghour
												newmsgminute = msgminute + 10
												if newmsgminute >= 60:
													newmsgminute -= 60
													newmsghour += 1
													if newmsghour >= 24:
														newmsghour -= 24
														newmsgday += 1
												
												newmsgtime = str(newmsgyear) + "-" + str(newmsgmonth) + "-" + str(newmsgday) + " " + str(newmsghour) + ":" + str(newmsgminute) + ":" + str(msgsecond)
												save_to_file(alchemycooldownpath, newmsgtime + " ~ " + charname[j], "")
												if recipedata != "":
													itemadded = False
													itemid = split_string(recipedata, 0, '|', "string")
													itemid = int(itemid) - 1
													addeditemdata = find_from_id(itemspath, itemid)
													itemname = split_string(addeditemdata, 0, '|', "string")
													
													k = 0
													for partyitem in partyitems:
														if partyitem == itemid:
															partyitemsquantity[k] += 1
															itemadded = True
															break
														k += 1
													if itemadded == False:
														k = 0
														for partyitem in partyitems:
															if partyitem == 0:
																partyitems[k] = itemid - 1
																partyitemsquantity[k] = 1
																itemadded = True
																break
													
													mixsuccessstring = "You mix the materials...\n" + itemname + " was created!"
													if discoveredrecipes[recipeid - 1] == 0:
														discoveredrecipes[recipeid - 1] = 1
														mixsuccessstring += "\nNew recipe added to recipe list."
													await client.send_message(message.channel, mixsuccessstring)
													
												else:
													await client.send_message(message.channel, "You mix the materials...\n...But nothing is created.")
											else:
												await client.send_message(message.channel, "You don't have at least one of the selected components.")
											
										else:
											await client.send_message(message.channel, "Please select at least two materials to mix.")
								else:
									if remainingcooldown == 0:
										remainingcooldown = second - msgsecond
										remainingcooldownstring = str(remainingcooldown) + " second"
										if remainingcooldown != 1:
											remainingcooldownstring += "s"
									else:
										remainingcooldownstring = str(remainingcooldown) + " minute"
										if remainingcooldown != 1:
											remainingcooldownstring += "s"
									
									await client.send_message(message.channel, charname[j] + " is too tired to perform alchemy!\nCooldown will reset in " + remainingcooldownstring + ".")
						j += 1	
			
			pointer = basepointer
			if state == "choice":
				m = 0
				for member in eventcommands:
					if command == member and member != "":
						i = 0
						if len(eventcommandflags[m]):
							partyevent = eventcommandresults[m][i] - 1
						else:
							while i < len(eventcommandflags[m]):
								if eventcommandflags[m][i] == 1:
									partyevent = eventcommandresults[m][i] - 1
									break
								i += 1
						
						runeventactions = True
						eventdata = find_from_id(eventpath, partyevent)
						eventdatapos = 0
						eventallowflag = split_string(eventdata, eventdatapos, '|', "string")
						eventdatapos = find_string_separator(eventdata, eventdatapos, '|')
						eventdisallowflag = split_string(eventdata, eventdatapos, '|', "string")
						eventdatapos = find_string_separator(eventdata, eventdatapos, '|')
						eventlocation = split_string(eventdata, eventdatapos, '|', "string")
						eventdatapos = find_string_separator(eventdata, eventdatapos, '|')
						eventactionstring = split_string(eventdata, eventdatapos, '|', "string")
						eventdatapos = find_string_separator(eventdata, eventdatapos, '|')
						eventcommandstring = split_string(eventdata, eventdatapos, '|', "string")
						eventdatapos = find_string_separator(eventdata, eventdatapos, '|')
						eventdescription = split_string(eventdata, eventdatapos, '|', "string")
						eventdescription = eventdescription.replace('\\n', '\n')
						eventdatapos = find_string_separator(eventdata, eventdatapos, '|')
						eventactions = [""] * 10
						eventcommands = [""] * 10
						eventcommandresults = [""] * 10
						
						i = 0
						k = 0
						while i < len(eventactionstring):
							if eventactionstring[i] != ";":
								if len(eventactions[k]) < 3:
									eventactions[k] += eventactionstring[i]
								else:
									eventactionarguments[k] += eventactionstring[i]
							else:
								if eventactionarguments[k] != "":
									eventactionarguments[k] = int(eventactionarguments[k])
								k += 1
							i += 1
							
						i = 0
						k = 0
						l = 0
						while i < len(eventcommandstring):
							if l == 0: # Check command text
								if eventcommandstring[i] != ";":
									if eventcommandstring[i] == "(":
										l = 1
									else:
										eventcommands[k] += eventcommandstring[i]
								else:
									eventcommandresults[k] = int(eventcommandresults[k])
									k += 1
							elif l == 1: # Check command destination
								if eventcommandstring[i] == ")":
									l = 0
								else:
									eventcommandresults[k] += eventcommandstring[i]
							i += 1
						break
					m += 1
			
			pointer = basepointer			
			if state == "battle":
				if team != "":
					j = 0
					while j < partysize:
						if command == charname[j].lower():
							argument1 = get_argument(lowermessage, pointer, ' ')
							pointer += len(argument1) + 1
							
							if argument1 == "attack":
								argument2 = get_argument(lowermessage, pointer, ' ')
								pointer += len(argument2) + 1
								
								if argument2.isdigit():
									if int(argument2) <= encounterquantity and int(argument2) > 0:
										if encounterhealth[int(argument2) - 1] == 0:
											argument2 = "0"
								if argument2 == "" or argument2.isdigit() == False or int(argument2) > encounterquantity - 1 or int(argument2) <= 0:
									k = 0
									while k < encounterquantity:
										if encounterhealth[k] != 0:
											argument2 = k
											break
										k += 1
								else:
									argument2 = int(argument2) - 1
								argument2 = int(argument2)
									
								actiontarget[j] = argument2
								actionqueue[j] = 0
								await client.send_message(message.channel, charname[j] + " is set to attack " + encountername[actiontarget[j]] + " [" + str(actiontarget[j] + 1) + ") this turn.")
							
							if argument1 == "defend":
								actionqueue[j] = 1
								await client.send_message(message.channel, charname[j] + " is set to defend this turn.")
							
							if argument1 == "run":
								actionqueue[j] = 2
								await client.send_message(message.channel, charname[j] + " is set to run this turn.")
							
							if argument1 == "use":
								argument2 = get_argument(lowermessage, pointer, ' ')
								pointer += len(argument2) + 1 # item
								argument3 = get_argument(lowermessage, pointer, ' ')
								pointer += len(argument3) + 1 # target
								
								if argument2 != "" and argument3 != "":
									validtarget = False
									i = 0
									while i < partysize:
										if argument3 == charname[i].lower():
											itemtarget[j] = i
											validtarget = True
											break
										i += 1
									
									if validtarget == True:
										itemused = False
										
										item = find_in_file(itemspath, argument2, "")
										itempos = 0
										itemname = split_string(item, itempos, '|', "string")
										itempos = find_string_separator(item, itempos, '|')
										itemrefname = split_string(item, itempos, '|', "string")
										itempos = find_string_separator(item, itempos, '|')
										itemdesc = split_string(item, itempos, '|', "string")
										itempos = find_string_separator(item, itempos, '|')
										itembattle = split_string(item, itempos, '|', "string")
										effectstring = ""
										
										i = 0
										for member in partyitems:
											itemid = find_id_in_file(itemspath, "|" + itemrefname + "|")
											if itemid == member:
												if itembattle == "battle":
													itemqueue[j] = itemid
													actionqueue[j] = 3
													await client.send_message(message.channel, charname[j] + " is set to use " + itemname + " this turn.")
												else:
													await client.send_message(message.channel, itemname + " can't be used in battle!")
												itemused = True
												break
											i += 1
										if itemused == False:
											await client.send_message(message.channel, "You don't have any " + itemname + ".")
									else:
										await client.send_message(message.channel, "You can't use an item on that!")
								else:
									await client.send_message(message.channel, "Make sure to provide an item name and target for the item's effect.")
							
							if argument1 == "skill":
								argument2 = get_argument(lowermessage, pointer, ' ')
								pointer += len(argument2) + 1 # skill
								
								skillname = skill_database(0, argument2, "name")
								skillclass = skill_database(0, argument2, "class")
								skilllevel = skill_database(0, argument2, "level")
								skillindex = skill_database(0, argument2, "index")
								skillpassive = skill_database(0, argument2, "passive")
								skilltype = skill_database(0, argument2, "type")
								
								argument3 = get_argument(lowermessage, pointer, ' ')
								pointer += len(argument3) + 1
								
								if skilltype == "guard" or skilltype == "curse":
									if skillname != "":
										if charclass[j] == skillclass and charlevel[j] >= skilllevel and skillpassive == False:
											actionqueue[j] = 4
											skillqueue[j] = skillindex
											await client.send_message(message.channel, charname[j] + " is set to perform " + skillname + " this turn.")
										else:
											await client.send_message(message.channel, charname[j] + " can't use that skill!")
									else:
										await client.send_message(message.channel, "That's not a valid skill!")
										
								else:
									if argument2 != "end":
										if skilltype == "friendly":
											if argument3.isdigit():
												if int(argument3) > partysize or int(argument3) == 0:
													argument3 = 0
												else:
													argument3 = int(argument3) - 1
												actiontarget[j] = argument3
											else:
												i = 0
												while i < partysize:
													if argument3 == charname[i]:
														actiontarget[j] = i
													i += 1
												
										else:
											if argument3.isdigit():
												if int(argument3) <= encounterquantity and int(argument3) > 0:
													if encounterhealth[int(argument3) - 1] == 0:
														argument3 = "0"
											if argument3 == "" or argument3.isdigit() == False or int(argument3) > encounterquantity - 1 or int(argument3) <= 0:
												k = 0
												while k < encounterquantity:
													if encounterhealth[k] != 0:
														argument3 = k
														break
													k += 1
											else:
												argument3 = int(argument3) - 1
											argument3 = int(argument3)
												
											actiontarget[j] = argument3
									
									if skillname != "":
										if charclass[j] == skillclass and charlevel[j] >= skilllevel and skillpassive == False:
											if argument2 == "end":
												if argument3 == "bunnyears":
													if charguardbunnyears[0] == 1:
														i = 0
														while i < partysize:
															charguardbunnyears[i] = 0
															charATKmod[i] -= guardbunnyearsmod
															charMAGmod[i] -= guardbunnyearsmod
															i += 1
														buffname = skill_database(0, argument3, "name")
														await client.send_message(message.channel, "Ended " + buffname + ".")
													else:
														await client.send_message(message.channel, "That buff is not active!")
												elif argument3 == "hyperlove":
													if charguardhyperlove[0] == 1:
														i = 0
														while i < partysize:
															charguardhyperlove[i] = 0
															i += 1
														buffname = skill_database(0, argument3, "name")
														await client.send_message(message.channel, "Ended " + buffname + ".")
													else:
														await client.send_message(message.channel, "That buff is not active!")
												elif argument3 == "toughfur":
													if charguardtoughfur[0] == 1:
														i = 0
														while i < partysize:
															charguardtoughfur[i] = 0
															i += 1
														buffname = skill_database(0, argument3, "name")
														await client.send_message(message.channel, "Ended " + buffname + ".")
													else:
														await client.send_message(message.channel, "That buff is not active!")
												elif argument3 == "voidgaze":
													if encountercursevoidgaze[0] == 1:
														i = 0
														while i < encounterquantity:
															encountercursevoidgaze[i] = 0
															encounterDEFmod[i] -= cursevoidgazemod
															encounterAGImod[i] -= cursevoidgazemod
															i += 1
														buffname = skill_database(0, argument3, "name")
														await client.send_message(message.channel, "Ended " + buffname + ".")
													else:
														await client.send_message(message.channel, "That buff is not active!")
												elif argument3 == "toxicblight":
													if encountercursetoxicblight[0] == 1:
														i = 0
														while i < encounterquantity:
															encountercursetoxicblight[i] = 0
															i += 1
														buffname = skill_database(0, argument3, "name")
														await client.send_message(message.channel, "Ended " + buffname + ".")
													else:
														await client.send_message(message.channel, "That buff is not active!")
												else:
													await client.send_message(message.channel, "That is not a valid buff!")
											else:
												actionqueue[j] = 4
												skillqueue[j] = skillindex
												if skilltype == "friendly":
													await client.send_message(message.channel, charname[j] + " is set to perform " + skillname + " on " + charname[actiontarget[j]] + " this turn.")
												else:
													await client.send_message(message.channel, charname[j] + " is set to perform " + skillname + " on " + encountername[actiontarget[j]] + " [" + str(actiontarget[j] + 1) + "] this turn.")
										else:
											await client.send_message(message.channel, charname[j] + " can't use that skill!")
									else:
										await client.send_message(message.channel, "That's not a valid skill!")
							
							if argument1 == "examine":
								argument2 = get_argument(lowermessage, pointer, ' ')
								pointer += len(argument2) + 1
								
								if argument2.isdigit():
									if int(argument2) <= encounterquantity and int(argument2) > 0:
										if encounterhealth[int(argument2) - 1] == 0:
											argument2 = "0"
								if argument2 == "" or argument2.isdigit() == False or int(argument2) > encounterquantity - 1 or int(argument2) <= 0:
									k = 0
									while k < encounterquantity:
										if encounterhealth[k] != 0:
											argument2 = k
											break
										k += 1
								else:
									argument2 = int(argument2) - 1
								argument2 = int(argument2)
									
								actiontarget[j] = argument2
								actionqueue[j] = 5
								await client.send_message(message.channel, charname[j] + " is set to examine " + encountername[actiontarget[j]] + " [" + str(actiontarget[j] + 1) + "] this turn.")
								
						j += 1
					
					if command == "execute" or command == "autoattack":
						autoattackcontinue = True
						winstring = ""
						while autoattackcontinue == True:
							if command == "execute":
								autoattackcontinue = False
							infotextdisplay = True
							initiativequeue = [0] * (partysize + encounterquantity)
							AGIdata = [0] * (partysize + encounterquantity)
							highestinitiative = 0
							encounterdefeated = False
							combatstring = ""
							k = 0
							while k < len(AGIdata):
								if k < partysize:
									AGIdata[k] = charAGI[k]
								else:
									AGIdata[k] = encounterAGI[k - partysize] + encounterAGImod[k - partysize]
								k += 1
								
							k = 0
							while k < len(AGIdata):
								highestinitiative = max(AGIdata)
								j = 0
								while j < len(AGIdata):
									if AGIdata[j] == highestinitiative:
										AGIdata[j] = 0
										initiativequeue[k] = j
										break;
									j += 1
								k += 1
							
							# Initiative-irrelevant Actions
							j = 0
							while j < partysize:
								if charhealth [j] > 0:
									if actionqueue[j] == 1: # Defend
										defending[j] = True
										combatstring += charname[j] + " defends.\n"
									if charclass[j] == "bun":
										if actionqueue[j] == 0:
											actionqueue[j] = 1
											defending[j] = True
											combatstring += charname[j] + " goes to attack " + encountername[actiontarget[j]] + " [" + str(actiontarget[j] + 1) + "]! But gets scared and defends instead...\n"
										if actionqueue[j] == 1:
											if charsecondarymana[j] > 51:
												charsecondarymana[j] -= 10
												if charsecondarymana[j] > 41 and charsecondarymana[j] < 51:
													charsecondarymana[j] = 51
											elif charsecondarymana[j] < 51:
												charsecondarymana[j] += 10
												if charsecondarymana[j] < 60 and charsecondarymana[j] > 50:
													charsecondarymana[j] = 50
								j += 1
							
							# Initiative-relevant Actions
							j = 0
							while j < len(initiativequeue):
								# Player actions
								if encounterdefeated == False:
									if initiativequeue[j] < partysize:
										if charhealth[initiativequeue[j]] > 0:
											if charstatusconfused[initiativequeue[j]] == 1:
												combatstring += charname[initiativequeue[j]] + " is confused! "
												confuseresist = random.randint(0, 100)
												if confuseresist > 80:
													charstatusconfused[initiativequeue[j]] = 0
													confusesuccess = 0
													combatstring += charname[initiativequeue[j]] + " snaps out of their confusion! "
												else:
													confusesuccess = random.randint(0, 100)
													if confusesuccess > 50:
														confusehit = initiativequeue[j]
														while confusehit == initiativequeue[j]:
															confusehit = random.randint(0, partysize - 1)
														damage = get_formula(charlevel[initiativequeue[j]], charATK[initiativequeue[j]] + charATKmod[initiativequeue[j]], charlevel[confusehit], (charDEF[confusehit] + charDEFmod[confusehit]) * 3)
														charhealth[confusehit] -= damage
														combatstring += charname[initiativequeue[j]] + " attacks " + charname[confusehit] + " for " + str(damage) + " damage!\n"
											else:
												confusesuccess = 0
													
											if confusesuccess <= 50:
												if actionqueue[initiativequeue[j]] == 0: # Attack
													damage = get_formula("damage", charlevel[initiativequeue[j]], charATK[initiativequeue[j]] + charATKmod[initiativequeue[j]], encounterlevel[actiontarget[initiativequeue[j]]], encounterDEF[actiontarget[initiativequeue[j]]] + encounterDEFmod[actiontarget[initiativequeue[j]]])
													damage = get_formula("critical", damage, criticalbonus[encounterid[actiontarget[initiativequeue[j]]]])
													encounterhealth[actiontarget[initiativequeue[j]]] -= damage
													if charclass[initiativequeue[j]] == "cat":
														if damage > 0:
															charsecondarymana[initiativequeue[j]] += 1 + spincrease[initiativequeue[j]]
															charmana[initiativequeue[j]] += round(charmana[initiativequeue[j]] * 0.1)
													combatstring += charname[initiativequeue[j]] + " attacks " + encountername[actiontarget[initiativequeue[j]]] + " [" + str(actiontarget[initiativequeue[j]] + 1) + "] for " + str(damage) + " damage!\n"

												if actionqueue[initiativequeue[j]] == 2: # Run
													combatstring += charname[initiativequeue[j]] + " tries to run!"
													chanceroll = roll_dice("chance")
													if chanceroll <= 40:
														state = "normal"
														encounterquantity = 0
														infotextdisplay = True
														autoattackcontinue = False
														
														k = 0
														while k < partysize:
															charstatuspoisoned[k] = 0
															charstatusconfused[k] = 0
															charguardbunnyears[k] = 0
															charguardhyperlove[k] = 0
															charguardtoughfur[k] = 0
															charATKmod[k] = 0
															charMAGmod[k] = 0
															actiontarget[k] = 0
															
															k += 1
														combatstring += " Got away safely!\n"
													else:
														combatstring += " Couldn't get away!\n"
												
												if actionqueue[initiativequeue[j]] == 3: # Item
													item = find_from_id(itemspath, itemqueue[initiativequeue[j]])
													itempos = 0
													itemname = split_string(item, itempos, '|', "string")
													itempos = find_string_separator(item, itempos, '|')
													itemrefname = split_string(item, itempos, '|', "string")
													itempos = find_string_separator(item, itempos, '|')
													itemdesc = split_string(item, itempos, '|', "string")
													itempos = find_string_separator(item, itempos, '|')
													itembattle = split_string(item, itempos, '|', "string")
													itempos = find_string_separator(item, itempos, '|')
													itemeffect = split_string(item, itempos, '|', "string")
													itempos = find_string_separator(item, itempos, '|')
													itemvalue = split_string(item, itempos, '|', "string")
													itemvalue = int(itemvalue)
													itemvalue += round(itemvalue * (0.01 * charALC[initiativequeue[j]]))
													
													combatstring += charname[initiativequeue[j]] + " uses " + itemname + " on " + charname[itemtarget[initiativequeue[j]]] + "!"
													effectstring = ""
													
													itemsleft = 1
													i = 0
													for member in partyitems:
														if find_id_in_file(itemspath, "|" + itemrefname + "|") == member:
															effectstring = "But it doesn't seem to do anything..."
															if itemeffect == "hurtfixed":
																charhealth[itemtarget[initiativequeue[j]]] -= itemvalue
																effectstring = charname[itemtarget[initiativequeue[j]]] + " loses " + str(itemvalue) + " health."
															if itemeffect == "healfixed":
																actualgain = charhealthmax[itemtarget[initiativequeue[j]]] - charhealth[itemtarget[initiativequeue[j]]]
																if itemvalue < actualgain:
																	actualgain = itemvalue
																charhealth[itemtarget[initiativequeue[j]]] += actualgain
																effectstring = charname[itemtarget[initiativequeue[j]]] + " restores " + str(actualgain) + " health."
															itemused = True
															partyitemsquantity[i] -= 1
															itemsleft = partyitemsquantity[i]
															break
														i += 1
													if itemused == True:
														combatstring += " " + effectstring
													else:
														combatstring += " But you don't have any " + itemname + "..."
													
													if itemsleft == 0:
														actionqueue[initiativequeue[j]] = 0
												
												if actionqueue[initiativequeue[j]] == 4: # Skill
													skillname = skill_database(skillqueue[initiativequeue[j]], "", "name")
													skillshortname = skill_database(skillqueue[initiativequeue[j]], "", "shortname")
													skillhealthcost = skill_database(skillqueue[initiativequeue[j]], "", "healthcost")
													skillmanacost = skill_database(skillqueue[initiativequeue[j]], "", "manacost")
													skillsecondarymanacost = skill_database(skillqueue[initiativequeue[j]], "", "secondarymanacost")
													
													if charhealth[initiativequeue[j]] > skillhealthcost and charmana[initiativequeue[j]] >= skillmanacost and charsecondarymana[initiativequeue[j]] >= skillsecondarymanacost and (charclass[initiativequeue[j]] == "cat" and charsecondarymana[initiativequeue[j]] <= 10) == False:
														if skillshortname == "blackarrow":
															charhealth[initiativequeue[j]] -= skillhealthcost
															charmana[initiativequeue[j]] -= skillmanacost
															charsecondarymana[initiativequeue[j]] -= skillsecondarymanacost
															damage = get_formula("damage", charlevel[initiativequeue[j]], charMAG[initiativequeue[j]] + charMAGmod[initiativequeue[j]], encounterlevel[actiontarget[initiativequeue[j]]], encounterRES[actiontarget[initiativequeue[j]]])
															damage = get_formula("critical", damage, criticalbonus[encounterid[actiontarget[initiativequeue[j]]]])
															encounterhealth[actiontarget[initiativequeue[j]]] -= damage
															combatstring += charname[initiativequeue[j]] + " uses " + skillname + " on " + encountername[actiontarget[initiativequeue[j]]] + " [" + str(actiontarget[initiativequeue[j]] + 1) + "] for " + str(damage) + " damage!\n"
															
														if skillshortname == "forcedsoul":
															poisonsuccessrate = 70 + charMAG[initiativequeue[j]] + charMAGmod[initiativequeue[j]]
															charsecondarymana[initiativequeue[j]] -= skillsecondarymanacost
															combatstring += charname[initiativequeue[j]] + " uses " + skillname + " on " + encountername[actiontarget[initiativequeue[j]]] + " [" + str(actiontarget[initiativequeue[j]] + 1) + "]!"
															if random.randint(0, 100) <= poisonsuccessrate:
																if encounterstatuspoisoned[actiontarget[initiativequeue[j]]] == 0:
																	encounterstatuspoisoned[actiontarget[initiativequeue[j]]] = 1
																	combatstring += " " + encountername[actiontarget[initiativequeue[j]]] + " [" + str(actiontarget[initiativequeue[j]] + 1) + "] was poisoned!\n"
																else:
																	combatstring += " But the enemy was already poisoned...\n"
															else:
																combatstring += " But the enemy refused to be poisoned...\n"
																
														if skillshortname == "darksigil":
															encounterdarksigilcountdown[actiontarget[initiativequeue[j]]] = 3
															charsecondarymana[initiativequeue[j]] -= skillsecondarymanacost
															encounterdarksigilcaster[actiontarget[initiativequeue[j]]] = initiativequeue[j]
															combatstring += charname[initiativequeue[j]] + " uses " + skillname + "! A dark aura fills the air around " + encountername[actiontarget[initiativequeue[j]]] + " [" + str(actiontarget[initiativequeue[j]] + 1) + "]...\n"
															
														if skillshortname == "meow":
															charmana[initiativequeue[j]] -= skillmanacost
															combatstring += charname[initiativequeue[j]] + " uses " + skillname + "!"
															damage = get_formula("damage", charlevel[initiativequeue[j]], (charMAG[initiativequeue[j]] + charMAGmod[initiativequeue[j]]) * 0.8, encounterlevel[actiontarget[initiativequeue[j]]], encounterRES[actiontarget[initiativequeue[j]]])
															damage = get_formula("damage", criticalbonus[encounterid[actiontarget[initiativequeue[j]]]])
															encounterhealth[actiontarget[initiativequeue[j]]] -= damage
															combatstring += charname[initiativequeue[j]] + " deals " + str(damage) + " damage to " + encountername[actiontarget[initiativequeue[j]]] + " [" + str(actiontarget[initiativequeue[j]] + 1) + "]!\n"
															
														if skillshortname == "cutepaws":
															confusesuccessrate = 50
															charmana[initiativequeue[j]] -= skillmanacost
															combatstring += charname[initiativequeue[j]] + " uses " + skillname + "!"
															damage = get_formula("damage", charlevel[initiativequeue[j]], (charATK[initiativequeue[j]] + charATKmod[initiativequeue[j]]) * 0.65, encounterlevel[actiontarget[initiativequeue[j]]], encounterDEF[actiontarget[initiativequeue[j]]])
															damage = get_formula("critical", damage, criticalbonus[encounterid[actiontarget[initiativequeue[j]]]])
															encounterhealth[actiontarget[initiativequeue[j]]] -= damage
															combatstring += charname[initiativequeue[j]] + " deals " + str(damage) + " damage to " + encountername[actiontarget[initiativequeue[j]]] + " [" + str(actiontarget[initiativequeue[j]] + 1) + "]!\n"
															
															if random.randint(0, 100) <= confusesuccessrate:
																if encounterstatusconfused[actiontarget[initiativequeue[j]]] == 0:
																	encounterstatusconfused[actiontarget[initiativequeue[j]]] = 1
																	combatstring += " " + encountername[actiontarget[initiativequeue[j]]] + " [" + str(actiontarget[initiativequeue[j]] + 1) + "] was confused!\n"
																else:
																	combatstring += " But the enemy was already confused...\n"
															else:
																combatstring += " But the enemy refused to be confused...\n"
																
														if skillshortname == "gnaw":
															charmana[initiativequeue[j]] -= skillmanacost
															combatstring += charname[initiativequeue[j]] + " uses " + skillname + "!"
															damage = get_formula("damage", charlevel[initiativequeue[j]], ((charATK[initiativequeue[j]] + charATKmod[initiativequeue[j]]) * 1.2 + (charMAG[initiativequeue[j]] + charMAGmod[initiativequeue[j]]) * 1.2) / 2, encounterlevel[actiontarget[initiativequeue[j]]], (encounterDEF[actiontarget[initiativequeue[j]]] + encounterDEFmod[actiontarget[initiativequeue[j]]] + encounterRES[actiontarget[initiativequeue[j]]]) / 2)
															damage = get_formula("critical", damage, criticalbonus[encounterid[actiontarget[initiativequeue[j]]]])
															encounterhealth[actiontarget[initiativequeue[j]]] -= damage
															combatstring += charname[initiativequeue[j]] + " deals " + str(damage) + " damage to " + encountername[actiontarget[initiativequeue[j]]] + " [" + str(actiontarget[initiativequeue[j]] + 1) + "]!\n"
															
														if skillshortname == "innocentgaze":
															charhealth[initiativequeue[j]] -= skillhealthcost
															charmana[initiativequeue[j]] -= skillmanacost
															charsecondarymana[initiativequeue[j]] -= skillsecondarymanacost
															damage = get_formula("damage", charlevel[initiativequeue[j]], (charATK[initiativequeue[j]] + charATKmod[initiativequeue[j]]) * 0.8, encounterlevel[actiontarget[initiativequeue[j]]], encounterDEF[actiontarget[initiativequeue[j]]] + encounterDEFmod[actiontarget[initiativequeue[j]]])
															damage = get_formula("damage", criticalbonus[encounterid[actiontarget[initiativequeue[j]]]])
															encounterhealth[actiontarget[initiativequeue[j]]] -= damage
															combatstring += charname[initiativequeue[j]] + " uses " + skillname + " on " + encountername[actiontarget[initiativequeue[j]]] + " [" + str(actiontarget[initiativequeue[j]] + 1) + "] for " + str(damage) + " damage!\n"
														
														if skillshortname == "bunnyears":
															if charguardbunnyears[0] == 0:
																i = 0
																while i < partysize:
																	if charguardbunnyears[i] == 0:
																		charguardbunnyears[i] = 1
																		charATKmod[i] += guardbunnyearsmod
																		charMAGmod[i] += guardbunnyearsmod
																	i += 1
																combatstring += charname[initiativequeue[j]] + " uses " + skillname + " on the party!\n"													
															else:
																combatstring += charname[initiativequeue[j]] + " tried to use " + skillname + ", but it failed!\n"
																
														if skillshortname == "bunnybandage":
															charhealth[initiativequeue[j]] -= skillhealthcost
															charmana[initiativequeue[j]] -= skillmanacost
															charsecondarymana[initiativequeue[j]] -= skillsecondarymanacost
															if charhealth[actiontarget[initiativequeue[j]]] > 0:
																healthrestored = round(charhealthmax[actiontarget[initiativequeue[j]]] * 0.2 + (charMAG[initiativequeue[j]] + charMAGmod[initiativequeue[j]]) * 2)
																if healthrestored + charhealth[actiontarget[initiativequeue[j]]] > charhealthmax[actiontarget[initiativequeue[j]]]:
																	healthrestored = charhealthmax[actiontarget[initiativequeue[j]]] - charhealth[actiontarget[initiativequeue[j]]]
																charhealth[actiontarget[initiativequeue[j]]] += healthrestored
																combatstring += charname[initiativequeue[j]] + " uses " + skillname + " on " + charname[actiontarget[initiativequeue[j]]] + "! " + str(healthrestored) + " Health restored!\n"													
															else:
																combatstring += charname[initiativequeue[j]] + " tried to use " + skillname + ", but it failed!\n"
														
														if skillshortname == "hyperlove":
															if charguardhyperlove[0] == 0:
																i = 0
																while i < partysize:
																	if charguardhyperlove[i] == 0:
																		charguardhyperlove[i] = 1
																	i += 1
																combatstring += charname[initiativequeue[j]] + " uses " + skillname + " on the party!\n"													
															else:
																combatstring += charname[initiativequeue[j]] + " tried to use " + skillname + ", but it failed!\n"
																
														if skillshortname == "toughfur":
															if charguardtoughfur[0] == 0:
																i = 0
																while i < partysize:
																	if charguardtoughfur[i] == 0:
																		charguardtoughfur[i] = 1
																	i += 1
																combatstring += charname[initiativequeue[j]] + " uses " + skillname + " on the party!\n"													
															else:
																combatstring += charname[initiativequeue[j]] + " tried to use " + skillname + ", but it failed!\n"
														
														if skillshortname == "arcanerend":
															charhealth[initiativequeue[j]] -= skillhealthcost
															charmana[initiativequeue[j]] -= skillmanacost
															charsecondarymana[initiativequeue[j]] -= skillsecondarymanacost
															damage = get_formula("damage", charlevel[initiativequeue[j]], charMAG[initiativequeue[j]] + charMAGmod[initiativequeue[j]], encounterlevel[actiontarget[initiativequeue[j]]], encounterRES[actiontarget[initiativequeue[j]]])
															damage = get_formula("damage", criticalbonus[encounterid[actiontarget[initiativequeue[j]]]])
															encounterhealth[actiontarget[initiativequeue[j]]] -= damage
															combatstring += charname[initiativequeue[j]] + " uses " + skillname + " on " + encountername[actiontarget[initiativequeue[j]]] + " [" + str(actiontarget[initiativequeue[j]] + 1) + "] for " + str(damage) + " damage!\n"
														
														if skillshortname == "voidgaze":
															if encountercursevoidgaze[0] == 0:
																i = 0
																while i < encounterquantity:
																	if encountercursevoidgaze[i] == 0:
																		encountercursevoidgaze[i] = 1
																		encounterDEFmod[i] -= cursevoidgazemod
																		encounterAGImod[i] -= cursevoidgazemod
																	i += 1
																combatstring += charname[initiativequeue[j]] + " uses " + skillname + " on the enemy!\n"													
															else:
																combatstring += charname[initiativequeue[j]] + " tried to use " + skillname + ", but it failed!\n"
														
														if skillshortname == "toxicblight":
															if encountercursetoxicblight[0] == 0:
																i = 0
																while i < encounterquantity:
																	if encountercursetoxicblight[i] == 0:
																		encountercursetoxicblight[i] = 1
																	i += 1
																combatstring += charname[initiativequeue[j]] + " uses " + skillname + " on the enemy!\n"													
															else:
																combatstring += charname[initiativequeue[j]] + " tried to use " + skillname + ", but it failed!\n"
															
													
													else:
														combatstring += charname[initiativequeue[j]] + " tried to use " + skillname + ", but it failed!\n"
												
												if actionqueue[initiativequeue[j]] == 5: # Examine
													combatstring += charname[initiativequeue[j]] + " tried to examine " + encountername[actiontarget[initiativequeue[j]]] + " [" + str(actiontarget[initiativequeue[j]] + 1) + "]..."
													if encounterexamined == 0:
														combatstring += "Analyzed " + encountername[actiontarget[initiativequeue[j]]] + " [" + str(actiontarget[initiativequeue[j]] + 1) + "]'s weak points!"
														encounterexamined = 1
														criticalbonusincrease = round((30 + random.randint(professionlevel[scholarpos], 2 * professionlevel[scholarpos])) / (1 + (0.01 * criticalbonus[encounterid[actiontarget[initiativequeue[j]]]])))
														if criticalbonusincrease < 1:
															criticalbonusincrease = 1
														criticalbonus[encounterid[actiontarget[initiativequeue[j]]]] += criticalbonusincrease
														
														scholarexpincrease = criticalbonusincrease
														professionexp[scholarpos] += scholarexpincrease
														
														combatstring += "\n" + professionname[scholarpos] + " profession gained " + str(scholarexpincrease) + " EXP.\n"
													else:
														combatstring += "But " + encountername[actiontarget[initiativequeue[j]]] + " [" + str(actiontarget[initiativequeue[j]] + 1) + "] had already been examined!\n"
												
									# Enemy actions
									else:
										if encounterhealth[initiativequeue[j] - partysize] <= 0:
											encounterhealth[initiativequeue[j] - partysize] = 0
											i = 0
											while i < partysize:
												if actiontarget[i] == initiativequeue[j] - partysize:
													k = 0
													while k < encounterquantity:
														if encounterhealth[k] != 0:
															actiontarget[i] = k
															break
														k += 1
												i += 1
											
										else:
											confusesuccess = 0
											
											if encounterstatusconfused[initiativequeue[j] - partysize] == 1:
												combatstring += encountername[initiativequeue[j] - partysize] + " [" + str(initiativequeue[j] - partysize + 1) + "] is confused! "
												confuseresist = random.randint(0, 100)
												if confuseresist > 80:
													encounterstatusconfused[initiativequeue[j] - partysize] = 0
													combatstring += encountername[initiativequeue[j] - partysize] + " [" + str(initiativequeue[j] - partysize + 1) + "] snaps out of their confusion! "
												else:
													confusesuccess = random.randint(0, 100)
													if confusesuccess > 50:
														combatstring += encountername[initiativequeue[j] - partysize] + " [" + str(initiativequeue[j] - partysize + 1) + "] missed its attack!\n"
												
											if confusesuccess <= 50:
												encounteraction = "attack"
												
												i = 0
												while i < len(encounterspecialslist[initiativequeue[j] - partysize]):
													if encounterspecialslist[initiativequeue[j] - partysize][i] != "":
														encounterselector = random.randint(1, 10)
														if encounterselector > 7:
															encounteraction = encounterspecialslist[initiativequeue[j] - partysize][random.randint(0, len(encounterspecialslist))]
														break
													i += 1
														
												if encounteraction == "attack":
													playerselected = random.randint(0, partysize - 1)
													damage = get_formula("damage", encounterlevel[initiativequeue[j] - partysize], encounterATK[initiativequeue[j] - partysize], charlevel[playerselected], charDEF[playerselected] + charDEFmod[playerselected])
													if defending[playerselected] == True:
														damage = int(damage / 1.5)
													charhealth[playerselected] -= damage
													combatstring += encountername[initiativequeue[j] - partysize] + " [" + str(initiativequeue[j] - partysize + 1) + "] attacks " + charname[playerselected] + " for " + str(damage) + " damage!\n"
								
								# Status checks
								if j == len(initiativequeue) - 1:
									k = 0				
									while k < partysize:
										if charstatuspoisoned[k] == 1:
											healthloss = round(charhealthmax[k] * (0.05 + (random.randint(-1, 1) / 100)))
											charhealth[k] -= healthloss
											combatstring += charname[k] + " is poisoned! " + charname[k] + " loses " + str(healthloss) + " health!\n"
										if charclass[k] == "bun":
											if charguardbunnyears[0] == 1:
												skillmanacost = skill_database(0, "bunnyears", "manacost")
												skillsecondarymanacost = skill_database(0, "bunnyears", "secondarymanacost")
												
												if charmana[k] >= skillmanacost:
													charmana[k] -= skillmanacost
													charsecondarymana[k] -= skillsecondarymanacost
												else:
													i = 0
													while i < partysize:
														if charguardbunnyears[i] == 1:
															charguardbunnyears[i] = 0
															charATKmod[i] -= guardbunnyearsmod
															charMAGmod[i] -= guardbunnyearsmod
														i += 1
											if charguardhyperlove[0] == 1:
												skillmanacost = skill_database(0, "hyperlove", "manacost")
												skillsecondarymanacost = skill_database(0, "hyperlove", "secondarymanacost")
												
												if charmana[k] >= skillmanacost:
													charmana[k] -= skillmanacost
													charsecondarymana[k] -= skillsecondarymanacost
													i = 0
													while i < partysize:
														charhealth[i] += 30 + (charMAG[k] + charMAGmod[k]) * 2
														i += 1
												else:
													i = 0
													while i < partysize:
														if charguardhyperlove[i] == 1:
															charguardhyperlove[i] = 0
														i += 1
											if charguardtoughfur[0] == 1:
												skillmanacost = skill_database(0, "toughfur", "manacost")
												skillsecondarymanacost = skill_database(0, "toughfur", "secondarymanacost")
												
												if charmana[k] >= skillmanacost:
													charmana[k] -= skillmanacost
													charsecondarymana[k] -= skillsecondarymanacost
												else:
													i = 0
													while i < partysize:
														if charguardtoughfur[i] == 1:
															charguardtoughfur[i] = 0
															charDEFmod[i] -= guardtoughfurmod
														i += 1
											if encountercursevoidgaze[0] == 1:
												skillmanacost = skill_database(0, "toxicblight", "manacost")
												skillsecondarymanacost = skill_database(0, "toxicblight", "secondarymanacost")
												
												if charmana[k] >= skillmanacost:
													charmana[k] -= skillmanacost
													charsecondarymana[k] -= skillsecondarymanacost
												else:
													i = 0
													while i < encounterquantity:
														if encountercursevoidgaze[i] == 1:
															encountercursevoidgaze[i] = 0
															encounterDEFmod[i] -= cursevoidgazemod
															encounterAGImod[i] -= cursevoidgazemod
														i += 1
											if encountercursetoxicblight[0] == 1:
												skillmanacost = skill_database(0, "toxicblight", "manacost")
												skillsecondarymanacost = skill_database(0, "toxicblight", "secondarymanacost")
												
												if charmana[k] >= skillmanacost:
													charmana[k] -= skillmanacost
													charsecondarymana[k] -= skillsecondarymanacost
													i = 0
													while i < encounterquantity:
														healthloss = round(encounterhealthmax[k] * (0.2 + (random.randint(-1, 1) / 100)) / encounterquantity)
														encounterhealth[i] -= healthloss
														i += 1
												else:
													i = 0
													while i < encounterquantity:
														if encountercursetoxicblight[i] == 1:
															encountercursetoxicblight[i] = 0
															
														i += 1
														
											if charsecondarymana[k] < 80:
												charmana[k] += round(charmana[k] * 0.05)
											else:
												combatstring += bunscaleright + " level too high! " + charname[k] + "'s natural Mana restoration was cancelled!\n"
											if charsecondarymana[k] < 20:
												healthloss = round(charhealthmax[k] * 0.05)
												charhealth[k] -= healthloss
												combatstring += bunscaleleft + " level too high! " + charname[k] + " lost " + str(healthloss) + " health!\n"
										k += 1
									
									k = 0
									while k < encounterquantity:
										if encounterstatuspoisoned[k] == 1:
											healthloss = round(encounterhealthmax[k] * (0.05 + (random.randint(-1, 1) / 100)))
											encounterhealth[k] -= healthloss
											combatstring += encountername[k] + " [" + str(k + 1) + "] is poisoned! " + encountername[k] + " [" + str(k + 1) + "] loses " + str(healthloss) + " health!\n"
										
										if encounterdarksigilcountdown[k] == 1:
											healthloss = int(round(charMAG[encounterdarksigilcaster[k]] + charMAGmod[encounterdarksigilcaster[k]] * (0.5 + (0.1 * encounterhealthmax[k]))))
											healthloss = round(healthloss * (1 + 0.01 * criticalbonus[encounterid[k]]))
											encounterhealth[k] -= healthloss
											combatstring += "Dark sigil explodes! " + encountername[k] + " [" + str(k + 1) + "] takes " + str(healthloss) + " damage!\n"
										if encounterdarksigilcountdown[k] >= 1:
											encounterdarksigilcountdown[k] -= 1
										k += 1
								
								# Check health
								k = 0				
								while k < partysize:	
									if charhealth[k] < 0:
										charhealth[k] = 0
									k += 1
								
								youlost = True
								k = 0
								while k < partysize:
									if charhealth[k] > 0:
										youlost = False
										break
									k += 1
									
								if youlost == True:
									fundslost = round(funds * 0.1)
									funds -= fundslost
									k = 0
									while k < partysize:
										charhealth[k] = charhealthmax[k]
										k += 1
									state = "normal"
									combatstring += "The party was defeated...\n" + str(fundslost) + " Gold was lost. The party woke up hours later in an inn.\n"
									winstring += "The party was defeated...\n" + str(fundslost) + " Gold was lost. The party woke up hours later in an inn.\n"
								
									encounterquantity = 0
									infotextdisplay = True
									autoattackcontinue = False
									
									k = 0
									while k < partysize:
										charstatuspoisoned[k] = 0
										charstatusconfused[k] = 0
										charguardbunnyears[k] = 0
										charguardhyperlove[k] = 0
										charguardtoughfur[k] = 0
										charATKmod[k] = 0
										charMAGmod[k] = 0
										actiontarget[k] = 0
										
										k += 1
									
								j += 1
											
								# Check for win
								youdefeated = True
								i = 0
								while i < encounterquantity:
									if encounterhealth[i] <= 0:
										encounterhealth[i] = 0
									else:
										youdefeated = False
									i += 1
								
								if youdefeated == True and youlost == False:
									autoattackcontinue = False
									expincrease = 0
									fundsincrease = 0
									i = 0
									while i < encounterquantity:
										expincrease += int((15 + random.randint(0, 2)) ** ((encounterlevel[i] + 1) / 2))
										fundsincrease += int((10 + random.randint(0, 5)) ** ((encounterlevel[i] + 1) / 2))
										i += 1
									funds += fundsincrease
									
									k = 0
									while k < partysize:
										charstatuspoisoned[k] = 0
										charstatusconfused[k] = 0
										charguardbunnyears[k] = 0
										charguardhyperlove[k] = 0
										charguardtoughfur[k] = 0
										charATKmod[k] = 0
										charMAGmod[k] = 0
										actiontarget[k] = 0
										if charhealth[k] > 0:
											charexp[k] += expincrease
											
										if charclass[k] == "cat":
											charsecondarymana[k] += 2 + int(1.5 * spincrease[k])
										k += 1
									combatstring += "\nThe enemy was defeated!\nParty members gained " + str(expincrease) + " EXP and " + str(fundsincrease) + " Gold!\n"
									winstring += "The enemy was defeated!\nParty members gained " + str(expincrease) + " EXP and " + str(fundsincrease) + " Gold!\n"

									maxitems = random.randint(0, 2 * encounterquantity)
									itemstotal = fetch_from_file(itemspath, "", "", True)
									itemsselected = [] * maxitems
									itemsavailable = []
									
									j = 0
									while j < maxitems:
										i = 0
										while i < len(itemstotal):
											if "0:0" not in itemstotal[i]:
												itemdata = itemstotal[i]
												itemdatapos = find_string_separator(itemdata, 0, '<')
												minlevel = split_string(itemdata, itemdatapos, ':', "string")
												minlevel = int(minlevel)
												itemdatapos = find_string_separator(itemdata, itemdatapos, ':')
												maxlevel = split_string(itemdata, itemdatapos, '>', "string")
												maxlevel = int(maxlevel)
												if minlevel <= encounteraveragelevel and maxlevel >= encounteraveragelevel:
													itemsavailable.append(itemstotal[i])
											i += 1
										itemsselected.append(itemsavailable[random.randint(0, len(itemsavailable) - 1)])
										j += 1
									for itemdata in itemsselected:
										itemdatapos = 0
										itemname = split_string(itemdata, itemdatapos, '|', "string")
										itemdatapos = find_string_separator(itemdata, itemdatapos, '|')
										itemshortname = split_string(itemdata, itemdatapos, '|', "string")
										itemid = find_id_in_file(itemspath, "|" + itemshortname + "|")
										
										combatstring += "Found " + itemname + "!"
										winstring += "Found " + itemname + "!"
										
										itemslot = find_item_slot(partyitems, itemid)
										if itemslot != None:
											partyitems[itemslot] = itemid
											partyitemsquantity[itemslot] += 1
										else:
											combatstring += " But your inventory was full..."
											winstring += " But your inventory was full..."
										combatstring += "\n"
										winstring += "\n"
										
									j = 0
									while j < encounterquantity:
										if random.randint(1, 100) <= encountercardrarity[j]:
											encountershortname = encountername[j].lower()
											encountershortname = encountershortname.replace(' ', '')
											tcgname = tcg_database(0, encountershortname, "name")
											tcgindex = tcg_database(0, encountershortname, "index")
											if tcgname != "":
												tcgcardsowned[tcgindex - 1] += 1
												combatstring += encountername[j] + " dropped a card! \"" + tcgname + "\" card added to card list.\n"
												winstring += encountername[j] + " dropped a card! \"" + tcgname + "\" card added to card list.\n"
										j += 1
									
									encounterquantity = 0
										
									state = "normal"
									infotextdisplay = True
								
								if state != "battle":
									break;
									
							if command == "execute":
								await client.send_message(message.channel, combatstring)
							else:
								if winstring != "":
									await client.send_message(message.channel, winstring)

			
			pointer = basepointer
			
			if command == "info":
						infotextdisplay = True
			
			j = 0
			while j < partysize:
				if command == charname[j].lower():
					argument1 = get_argument(lowermessage, pointer, ' ')
					pointer += len(argument1) + 1
					argument2 = get_argument(lowermessage, pointer, ' ')
					pointer += len(argument2) + 1
					
					if argument1 == "skills":
						if argument2 == "":
							skillsstring = "Available skills for " + charname[j] + ":"
							skilllistindex = 1
							while skilllistindex < 500:
								skillname = skill_database(skilllistindex, "", "name")
								skillshortname = skill_database(skilllistindex, "", "shortname")
								skillclass = skill_database(skilllistindex, "", "class")
								skilllevel = skill_database(skilllistindex, "", "level")
								skillhealthcost = skill_database(skilllistindex, "", "healthcost")
								skillmanacost = skill_database(skilllistindex, "", "manacost")
								skillsecondarymanacost = skill_database(skilllistindex, "", "secondarymanacost")
								skillpassive = skill_database(skilllistindex, "", "passive")
								
								if skillname == "":
									break
								
								if charclass[j] == skillclass and charlevel[j] >= skilllevel:
									skillsstring += "\n" + skillname + " [" + skillshortname + "]"
									if skillpassive == True:
										skillsstring += " | Passive Skill"
									if skillhealthcost > 0:
										skillsstring += " | " + str(skillhealthcost) + " Health"
									if skillmanacost > 0:
										skillsstring += " | " + str(skillmanacost) + " Mana"
									if skillsecondarymanacost != 0:
										if charclass[j] == "bun":
											if skillsecondarymanacost > 0:
												charsecondarymananame[j] = bunscaleright
											else:
												charsecondarymananame[j] = bunscaleleft
										skillsstring += " | " + str(abs(skillsecondarymanacost)) + " " + charsecondarymananame[j]
								skilllistindex += 1
										
							await client.send_message(message.channel, skillsstring)
						else:
							skillname = skill_database(0, argument2, "name")
							skillshortname = skill_database(0, argument2, "shortname")
							skillclass = skill_database(0, argument2, "class")
							skilllevel = skill_database(0, argument2, "level")
							skilldescription = skill_database(0, argument2, "description")
							skillhealthcost = skill_database(0, argument2, "healthcost")
							skillmanacost = skill_database(0, argument2, "manacost")
							skillsecondarymanacost = skill_database(0, argument2, "secondarymanacost")
							skillpassive = skill_database(skilllistindex, "", "passive")
							
							if charclass[j] == skillclass and charlevel[j] >= skilllevel and skillname != "":
								skillsstring = "\n" + skillname + " [" + skillshortname + "]"
								if skillpassive == True:
									skillsstring += " | Passive Skill"
								if skillhealthcost > 0:
									skillsstring += " | " + str(skillhealthcost) + " Health"
								if skillmanacost > 0:
									skillsstring += " | " + str(skillmanacost) + "Mana"
								if skillsecondarymanacost > 0:
									skillsstring += " | " + str(skillsecondarymanacost) + " " + charsecondarymananame[j]
								skillsstring += "\n" + skilldescription
								await client.send_message(message.channel, skillsstring)
							else:
								await client.send_message(message.channel, charname[j] + " doesn't have that skill!")
							
				j += 1
							
			if command == "status":
				statusmessage = ""
				j = 0
				while j < partysize:
					manastring = ""
					secondarymanastring = ""
					if charmanamax[j] != 0:
						manastring = " | Mana: " + str(charmana[j]) + "/" + str(charmanamax[j])
					if charsecondarymanamax[j] != 0:
						secondarymanamodifier = 0
						secondarymanamaxmodifier = secondarymanamodifier
						if charclass[j] == "cat":
							secondarymanamodifier = -10
							secondarymanamaxmodifier = secondarymanamodifier
						if charclass[j] == "bun":
							secondarymanamaxmodifier = -50
							if charsecondarymana[j] > 50:
								charsecondarymananame[j] = bunscaleright
								secondarymanamodifier = -50
							else:
								charsecondarymananame[j] = bunscaleleft
								secondarymanamodifier = (50 - charsecondarymana[k]) * 2 + 1 - 50
								if secondarymanamodifier > 50:
									secondarymanamodifier = 50
						secondarymanastring = " | " + charsecondarymananame[j] + ": " + str(charsecondarymana[j] + secondarymanamodifier) + "/" + str(charsecondarymanamax[j] + secondarymanamaxmodifier)
					statusmessage += charname[j] + " | Level " + str(charlevel[j]) + " | " + charclassfull[j] + "\nHealth: " + str(charhealth[j]) + "/" + str(charhealthmax[j]) + manastring + secondarymanastring + " | EXP: " + str(charexp[j]) + "/" + str(charexpmax[j]) + "\nATK: " + str(charATK[j]) + " | DEF: " + str(charDEF[j]) + " | MAG: " + str(charMAG[j]) + " | AGI: " + str(charAGI[j]) + " | LUK: " + str(charLUK[j]) + " | ALC: " + str(charALC[j]) + "\n\n"
					j += 1
				
				statusmessage += "Profession levels:\n\n"
				
				j = 0
				while j < availableprofessions:
					statusmessage += professionname[j] + " | Level " + str(professionlevel[j]) + "\nEXP: " + str(professionexp[j]) + "/" + str(professionexpmax[j]) + "\n\n"
					j += 1
				await client.send_message(message.channel, statusmessage)

			if command == "recipelist":
				recipes = [""] * 256
				recipestring = ""
				k = 1
				while k < len(recipes):
					recipedata = find_from_id(recipespath, k)
					if recipedata == "":
						break
					recipedatapos = 0
					recipeid = split_string(recipedata, recipedatapos, '|', "string")
					recipeid = int(recipeid)
					recipedatapos = find_string_separator(recipedata, recipedatapos, '|')
					recipetier = split_string(recipedata, recipedatapos, '|', "string")
					recipedatapos = find_string_separator(recipedata, recipedatapos, '|')
					recipematerials = split_string(recipedata, recipedatapos, '|', "string")
					recipedatapos = find_string_separator(recipedata, recipedatapos, '|')
					recipeshortname = split_string(recipedata, recipedatapos, '|', "string")
					itemdata = fetch_from_database(itemspath, "|" + recipeshortname + "|", "", "")
					itemdatapos = 0
					itemname = split_string(itemdata, itemdatapos, '|', "string")
					itemdatapos = find_string_separator(itemdata, itemdatapos, '|')
					itemshortname = split_string(itemdata, itemdatapos, '|', "string")
					itemdatapos = find_string_separator(itemdata, itemdatapos, '|')
					itemdescription = split_string(itemdata, itemdatapos, '|', "string")
					itemdatapos = find_string_separator(itemdata, itemdatapos, '|')
					if discoveredrecipes[recipeid - 2] == 0:
						newitemname = ""
						newitemshortname = ""
						newitemdescription = ""
						newrecipematerials = ""
						l = 0
						while l < len(itemdescription) + 50:
							if l < len(itemname):
								if itemname[l] == ' ':
									newitemname += itemname[l]
								else:
									newitemname += '?'
							if l < len(itemshortname):
								if itemshortname[l] == ' ':
									newitemshortname += itemshortname[l]
								else:
									newitemshortname += '?'
							if l < len(itemdescription):
								if itemdescription[l] == ' ':
									newitemdescription += itemdescription[l]
								else:
									newitemdescription += '?'
							if l < len(recipematerials):
								if recipematerials[l] == ' ' or recipematerials[l] == ';':
									newrecipematerials += recipematerials[l]
								else:
									newrecipematerials += '?'
							l += 1
						
						itemname = newitemname
						itemshortname = newitemshortname
						itemdescription = newitemdescription
						recipematerials = newrecipematerials
						
					
					stringaddition = "Tier " + recipetier + " | " + itemname + " [" + itemshortname + "] | " + itemdescription + "\nMaterials: "
					
					args = [""] * 3
					args2 = [""] * 3
					recipedatapos = 0
					l = 0
					while l < len(args):
						args[l] = split_string(recipematerials, recipedatapos, ';', "string")
						recipedatapos = find_string_separator(recipematerials, recipedatapos, ';')
						itemdata = fetch_from_database(itemspath, "|" + args[l] + "|", "", "")
						args2[l] = split_string(itemdata, 0, '|', "string")
						if args[l] != "":
							if l != 0:
								stringaddition += ", "
							stringaddition += args2[l] + " (" + args[l] + ")"
						l += 1
						
					recipestring += stringaddition + "\n\n"
					k += 1
				
				await client.send_message(message.channel, recipestring)
			
			if command == "codex":
				argument1 = get_argument(lowermessage, pointer, ' ')
				pointer += len(argument1) + 1 # category
				argument2 = lowermessage[pointer:] # entry
				
				readentry = False
				
				if argument1 == "":
					await client.send_message(message.channel, "Codex categories:\n\nPeople\nFamily")
				else:
					if argument2 == "":
						codexlist = ""
						k = 0
						while k < len(discoveredcodex):
							newcodex = find_from_id(codexpath, k + 1)
							if newcodex != "":
								newcodexpos = 0
								newcodexname = split_string(newcodex, newcodexpos, "|", "string")
								newcodexpos = find_string_separator(newcodex, newcodexpos, '|')
								newcodexcategory = split_string(newcodex, newcodexpos, "|", "string")
								newcodexpos = find_string_separator(newcodex, newcodexpos, '|')
								newcodexdescription = split_string(newcodex, newcodexpos, "|", "string")
								
								if newcodexcategory.lower() == argument1:
									if discoveredcodex[k] == 0:
										newnewcodexname = ""
										l = 0
										while l < len(newcodexname):
											if newcodexname[l] == ' ':
												newnewcodexname += newcodexname[l]
											else:
												newnewcodexname += '?'
											l += 1
										newcodexname = newnewcodexname
									
									codexlist += newcodexname + "\n"
							k += 1
								
						if codexlist != "":
							await client.send_message(message.channel, "Entries for selected category:\n" + codexlist)
						else:
							readentry = True
							argument2 = argument1
							argument1 = ""
							#await client.send_message(message.channel, "Invalid category!")
					else:
						readentry = True
						
					if readentry == True:
						if argument2 == "":
							selectedcodex = find_id_in_file(codexpath, "|" + argument1, True)
						else:
							selectedcodex = find_id_in_file(codexpath, argument2 + "|" + argument1, True)
						if selectedcodex != 0:
							selectedcodex = find_from_id(codexpath, selectedcodex)
							selectedcodexpos = 0
							selectedcodexname = split_string(selectedcodex, selectedcodexpos, "|", "string")
							selectedcodexpos = find_string_separator(selectedcodex, selectedcodexpos, '|')
							selectedcodexcategory = split_string(selectedcodex, selectedcodexpos, "|", "string")
							selectedcodexpos = find_string_separator(selectedcodex, selectedcodexpos, '|')
							selectedcodexdescription = split_string(selectedcodex, selectedcodexpos, "|", "string")
							selectedcodexpos = find_string_separator(selectedcodex, selectedcodexpos, '|')
							selectedcodeximage = split_string(selectedcodex, selectedcodexpos, "|", "string")
							
							await client.send_message(message.channel, selectedcodexname + "\n" + selectedcodexdescription + "\n" + selectedcodeximage)
						else:
							await client.send_message(message.channel, "You don't know that entry!")
			
			if command == "use":
				argument1 = get_argument(lowermessage, pointer, ' ')
				pointer += len(argument1) + 1 # item
				argument2 = get_argument(lowermessage, pointer, ' ')
				pointer += len(argument2) + 1 # target
				argument3 = get_argument(lowermessage, pointer, ' ')
				pointer += len(argument3) + 1 # quantity
				
				if argument3 == "":
					argument3 = 1
				argument3 = int(argument3)
				itemused = False
				itemuser = 0
				i = 0
				while i < partysize:
					if argument2 == charname[i].lower():
						itemuser = i
						break
					i += 1
				
				if argument1 != "" and argument2 != "":
					item = find_in_file(itemspath, argument1, "")
					if item != "":
						itempos = 0
						itemname = split_string(item, itempos, '|', "string")
						itempos = find_string_separator(item, itempos, '|')
						itemrefname = split_string(item, itempos, '|', "string")
						itempos = find_string_separator(item, itempos, '|')
						itemdesc = split_string(item, itempos, '|', "string")
						itempos = find_string_separator(item, itempos, '|')
						itembattle = split_string(item, itempos, '|', "string")
						itempos = find_string_separator(item, itempos, '|')
						itemeffect = split_string(item, itempos, '|', "string")
						itempos = find_string_separator(item, itempos, '|')
						itemvalue = split_string(item, itempos, '|', "string")
						itemvalue = int(itemvalue)
					else:
						itemrefname = " "
					
					effectstring = ""
					
					i = 0
					for member in partyitems:
						if find_id_in_file(itemspath, "|" + itemrefname + "|") == member:
							if state == "normal":
								itemquantity = partyitemsquantity[i]
								
								if itemquantity >= argument3:
									effectstring = "But it doesn't seem to do anything..."
									if itemeffect == "hurtfixed":
										charhealth[itemuser] -= itemvalue * argument3
										effectstring = charname[itemuser] + " loses " + str(itemvalue * argument3) + " health."
									if itemeffect == "healfixed":
										actualgain = charhealthmax[itemuser] - charhealth[itemuser]
										if itemvalue < actualgain:
											actualgain = itemvalue
										charhealth[itemuser] += actualgain
										effectstring = charname[itemuser] + " restores " + str(actualgain) + " health."
									itemused = True
									partyitemsquantity[i] -= 1
									await client.send_message(message.channel, "You use " + str(argument3) + " " + itemname + " on " + charname[itemuser] + ". " + effectstring)
								else:
									itemused = True
									await client.send_message(message.channel, "You don't have enough " + itemname + ", you only have " + str(itemquantity) + ".")
							break
						i += 1
					if itemused == False:
						await client.send_message(message.channel, "You don't have any " + itemname + ".")
			
			if command == "discard":
				argument1 = get_argument(lowermessage, pointer, ' ')
				pointer += len(argument1) + 1
				argument2 = get_argument(lowermessage, pointer, ' ')
				pointer += len(argument2) + 1
				if argument2 == "":
					argument2 = 1
				argument2 = int(argument2)
				itemdiscarded = False
				
				if argument1 != "":
					item = find_in_file(itemspath, argument1, "")
					itempos = 0
					itemname = split_string(item, itempos, '|', "string")
					itempos = find_string_separator(item, itempos, '|')
					itemrefname = split_string(item, itempos, '|', "string")
					
					i = 0
					for member in partyitems:
						if find_id_in_file(itemspath, "|" + itemrefname + "|") == member:
							if state == "normal":
								itemquantity = partyitemsquantity[i]
								if itemquantity >= argument2:
									partyitemsquantity[i] -= argument2
									itemdiscarded = True
									await client.send_message(message.channel, "Discarded " + argument2 + " " + itemname + ".")
								else:
									itemdiscarded = True
									await client.send_message(message.channel, "You don't have enough " + itemname + ", you only have " + str(itemquantity) + ".")
							else:
								itemdiscarded = True
								await automated_message(message.channel, "wrongstate")
							break
					if itemdiscarded == False:
						await client.send_message(message.channel, "You don't have any " + itemname + ".")
			
			if command == "partystatus":
				itemsstring = ""
				i = 0
				for member in partyitems:
					if member != 0:
						item = find_from_id(itemspath, member)
						itemquantity = partyitemsquantity[i]
						itempos = 0
						itemname = split_string(item, itempos, '|', "string")
						itempos = find_string_separator(item, itempos, '|')
						itemrefname = split_string(item, itempos, '|', "string")
						itempos = find_string_separator(item, itempos, '|')
						itemdesc = split_string(item, itempos, '|', "string")
						itemsstring += str(itemquantity) + " " + itemname + " [" + itemrefname + "] - " + itemdesc + "\n"
						i += 1
				if itemsstring == "":
					itemsstring = "Nothing!"
				await client.send_message(message.channel, "Gold: " + str(funds) + "\nItems:\n" + itemsstring + "\nTo use an item, type **" + commandsymbol + "use <short name> <quantity\*>.** To discard an item, type **" + commandsymbol + "discard <short name> <quantity\*>.** An item's short name is the name that is displayed inside square brackets. Type **" + commandsymbol + "help** for more detailed instructions.")
			
			if command == "personalstatus":
				namedata = ""
				classdata = ""
				
				personalmessage = ""
				
				i = 0
				while i < 10:
					if individualdataarray[individualnamepos + i] == 0: #and individualdataarray[charnamepos + i + 1 + j * databuffer] == 0:
						break
					namedata += chr(individualdataarray[individualnamepos + i])
					i += 1
				i = 0
				while i < 10:
					if individualdataarray[individualclasspos + i] == 0: #and individualdataarray[charclasspos + i + 1 + j * databuffer] == 0:
						break
					classdata += chr(individualdataarray[individualclasspos + i])
					i += 1
					
				if classdata == "cat":
					classfulldata = "Black Cat"
				elif classdata == "kit":
					classfulldata = "Kitsune"
				elif classdata == "bun":
					classfulldata = "Esper Bunny"
				elif classdata == "sqk":
					classfulldata = "Squirrel Knight"
				else:
					classfulldata = "Human"
					
				exparray = [individualdataarray[individualexppos], individualdataarray[individualexppos + 1]]
				expdata = int.from_bytes(exparray, "little")
				leveldata = individualdataarray[individuallevelpos]
				ATKdata = individualdataarray[individualATKpos]
				DEFdata = individualdataarray[individualDEFpos]
				MAGdata = individualdataarray[individualMAGpos]
				AGIdata = individualdataarray[individualAGIpos]
				LUKdata = individualdataarray[individualLUKpos]
				ALCdata = individualdataarray[individualALCpos]
				expmaxdata = round(50 * (5**(leveldata - 1)))
				
				professionleveldata = [0] * availableprofessions
				professionexpdata = [0] * availableprofessions
				professionexpmaxdata = [0] * availableprofessions
				
				i = 0
				while i < availableprofessions:
					professionleveldata[i] = individualdataarray[individualprofessionskillspos + i]
					professionexpmaxdata[i] = round(50 * (5**(professionleveldata[i] - 1)))
					professionexparray = [individualdataarray[(i * 2) + individualprofessionskillspos + professionexpdatabuffer], professiondataarray[(i * 2) + individualprofessionskillspos + professionexpdatabuffer + 1]]
					professionexpdata[i] = int.from_bytes(professionexparray, "little")
					i += 1
				
				fundsarray = [individualdataarray[individualfundspos], individualdataarray[individualfundspos + 1]]
				fundsdata = int.from_bytes(fundsarray, "little")
				
				personalmessage += namedata + " | Level " + str(leveldata) + " | " + classfulldata + "\nEXP: " + str(expdata) + "/" + str(expmaxdata) + "\nATK: " + str(ATKdata) + " | DEF: " + str(DEFdata) + " | MAG: " + str(MAGdata) + " | AGI: " + str(AGIdata) + " | LUK: " + str(LUKdata) + " | ALC: " + str(ALCdata) + "\n\n"
					
				personalmessage += "Gold: " + str(fundsdata)
				
				personalmessage += "\n\nProfession levels:\n\n"
				
				j = 0
				while j < availableprofessions:
					personalmessage += professionname[j] + " | Level " + str(professionlevel[j]) + "\nEXP: " + str(professionexp[j]) + "/" + str(professionexpmax[j]) + "\n\n"
					j += 1
				
				await client.send_message(message.channel, personalmessage)
			
			
			if command == "reset":
				if resetvalid == 1 or botcommander == True or privatemessage == True:
					argument1 = get_argument(lowermessage, pointer, ' ')
					pointer += len(argument1) + 1
					
					if argument1 == "confirm":
						os.remove(chardatapath_full)
						os.remove(partydatapath_full)
						os.remove(flagdatapath_full)
						os.remove(professiondatapath_full)
						os.remove(encounterdatapath_full)
						os.remove(recipedatapath_full)
						os.remove(codexdatapath_full)
						os.remove(tcgdatapath_full)
						os.remove(criticaldatapath_full)
						
						os.remove(alchemycooldownpath)
						
						gamereset = True
						
						resetstring = "Game has been reset! Type **\"" + commandsymbol + "\"** to start a new game."
						
						if privatemessage == True:
							individualreadonly = False
							resetstring += "\nCharacter stats applied to individual data!"
						
						await client.send_message(message.channel, resetstring)
					else:
						await client.send_message(message.channel, "This will reset all game data and restart the game. To confirm this, use **" + commandsymbol + "reset confirm**.")
				else:
					await client.send_message(message.channel, "Cannot reset game! Please finish the current game or ask a bot commander to **" + commandsymbol + "reset**.")
			
			# Admin commands	
			if botcommander == True:
				if command == "setteam":
					argument1 = message.content[pointer:]
					
					currentteam = find_in_file(teamchannelspath, str(message.channel), str(message.server))
					if currentteam == "":
						save_to_file(teamchannelspath, str(message.channel) + " <" + argument1 + ">", str(message.server))
						await client.send_message(message.channel, "This channel is now under Team " + argument + ".")
					else:
						team = ""
						await client.send_message(message.channel, "This channel is already part of a team! Use **" + commandsymbol + "clearteam** to clear any team affiliations with the current channel.")
				
				if command == "clearteam":
					delete_from_file(teamchannelspath, str(message.channel), str(message.server))
					team = ""
					await client.send_message(message.channel, "Cleared team affiliations for this channel.")
				
				if command == "teststart":
					charname = ["Anne", "Vex", "Ears", "Red"]
					charclass = ["cat", "kit", "bun", "sqk"]
					j = 0
					while j < partysize:
						statsstring = find_in_file(statspath, "| " + charclass[j] + " |", "")
						statsstringpos = 0
						statsstringpos = find_string_separator(statsstring, statsstringpos, '[')
						ATKincrease = split_string(statsstring, statsstringpos, ']', "string")
						ATKincrease = int(ATKincrease)
						statsstringpos = find_string_separator(statsstring, statsstringpos, '[')
						DEFincrease = split_string(statsstring, statsstringpos, ']', "string")
						DEFincrease = int(DEFincrease)
						statsstringpos = find_string_separator(statsstring, statsstringpos, '[')
						MAGincrease = split_string(statsstring, statsstringpos, ']', "string")
						MAGincrease = int(MAGincrease)
						statsstringpos = find_string_separator(statsstring, statsstringpos, '[')
						AGIincrease = split_string(statsstring, statsstringpos, ']', "string")
						AGIincrease = int(AGIincrease)
						statsstringpos = find_string_separator(statsstring, statsstringpos, '[')
						LUKincrease = split_string(statsstring, statsstringpos, ']', "string")
						LUKincrease = int(LUKincrease)
						statsstringpos = find_string_separator(statsstring, statsstringpos, '[')
						ALCincrease = split_string(statsstring, statsstringpos, ']', "string")
						ALCincrease = int(ALCincrease)
						
						charATK[j] = ATKincrease
						charMAG[j] = MAGincrease
						charDEF[j] = DEFincrease
						charAGI[j] = AGIincrease
						charLUK[j] = LUKincrease
						charALC[j] = ALCincrease
						
						charlevel[j] = 1
						charexp[j] = 0
						charexpmax[j] = 50 * (5**(charlevel[j] - 1))
						charhealth[j] = 999
						charmana[j] = 999
						charsecondarymana[j] = 999
							
						j += 1
					
					state = "normal"
					funds = 0
					
					partyitems[0] = 1
					partyitemsquantity[0] = 100
					partyitems[1] = 2
					partyitemsquantity[1] = 100
					partylocation = 1
					partyevent = 0
					
					k = 0
					while k < len(discoveredcodex):
						codexentry = find_from_id(codexpath, k + 1)
						if codexentry != "":
							codexentrypos = 0
							codexentryname = split_string(codexentry, codexentrypos, "|", "string")
							codexentrypos = find_string_separator(codexentry, codexentrypos, '|')
							codexentrycategory = split_string(codexentry, codexentrypos, "|", "string")
							codexentrypos = find_string_separator(codexentry, codexentrypos, '|')
							codexentrydescription = split_string(codexentry, codexentrypos, "|", "string")
							codexentrypos = find_string_separator(codexentry, codexentrypos, '|')
							codexentryimage = split_string(codexentry, codexentrypos, "|", "string")
							codexentrypos = find_string_separator(codexentry, codexentrypos, '|')
							codexentrydefault = split_string(codexentry, codexentrypos, "|", "string")
							codexentrydefault = int(codexentrydefault)
							
							discoveredcodex[k] = codexentrydefault
						else:
							discoveredcodex[k] = 0
						k += 1
					
					await client.send_message(message.channel, "Game has been test-started!")
				
			# Help
			if command == "help":
				argument1 = get_argument(lowermessage, pointer, ' ')
				pointer += len(argument1) + 1
				helpmessage = ""
				
				if argument1 == "":
					helpmessage = "<Placeholder text>\n\nTopics:\nBasics, Combat, Commands, Events"
					
				else:
					if argument1[0] == commandsymbol:
						if argument1[1:] == "help":
							helpmessage = "quack"
						
					else:
						if argument1 == "basics":
							helpmessage = ""
						if argument1 == "commands":
							helpmessage = "Available commands:\n<Placeholder text>\n\nAdmin commands:\n<Placeholder text>\n\nType **help <command>** (including the **" + commandsymbol + "**) for information on a specific command."
										
				await client.send_message(message.channel, helpmessage)
			
			# After-action Events
			if gamereset == False:
			
				j = 0
				while j < partysize:
					if charhealth[j] > charhealthmax[j]:
						charhealth[j] = charhealthmax[j]
					if charmana[j] > charmanamax[j]:
						charmana[j] = charmanamax[j]
					if charsecondarymana[j] > charsecondarymanamax[j]:
						charsecondarymana[j] = charsecondarymanamax[j]
					j += 1
						
				if team != "":
				
					levelupstring = ""	
					j = 0				
					while j < partysize:
						if charexp[j] >= charexpmax[j]:
							charexp[j] -= charexpmax[j]
							charlevel[j] += 1
							
							levelupstring += charname[j] + " leveled up! " + charname[j] + " is now level " + str(charlevel[j]) + ".\n"
							
							i = 0
							while i < 50:
								skillleveldata = skill_database(i, "", "level")
								skillnamedata = skill_database(i, "", "name")
								skillshortnamedata = skill_database(i, "", "shortname")
								skillclassdata = skill_database(i, "", "class")
								if charclass[j] == skillclassdata and charlevel[j] == skillleveldata:
									levelupstring += "Learned " + skillnamedata + " [" + skillshortnamedata + "].\n"
								i += 1
							
							levelupstring += "\n"
							
							statsstring = find_in_file(statspath, "| " + charclass[j] + " |", "")
							statsstringpos = 0
							statsstringpos = find_string_separator(statsstring, statsstringpos, '(')
							ATKincrease = split_string(statsstring, statsstringpos, ')', "string")
							ATKincrease = int(ATKincrease)
							statsstringpos = find_string_separator(statsstring, statsstringpos, '(')
							DEFincrease = split_string(statsstring, statsstringpos, ')', "string")
							DEFincrease = int(DEFincrease)
							statsstringpos = find_string_separator(statsstring, statsstringpos, '(')
							MAGincrease = split_string(statsstring, statsstringpos, ')', "string")
							MAGincrease = int(MAGincrease)
							statsstringpos = find_string_separator(statsstring, statsstringpos, '(')
							AGIincrease = split_string(statsstring, statsstringpos, ')', "string")
							AGIincrease = int(AGIincrease)
							statsstringpos = find_string_separator(statsstring, statsstringpos, '(')
							LUKincrease = split_string(statsstring, statsstringpos, ')', "string")
							LUKincrease = int(LUKincrease)
							statsstringpos = find_string_separator(statsstring, statsstringpos, '(')
							ALCincrease = split_string(statsstring, statsstringpos, ')', "string")
							ALCincrease = int(ALCincrease)
							
							charATK[j] += ATKincrease
							charDEF[j] += DEFincrease
							charMAG[j] += MAGincrease
							charAGI[j] += AGIincrease
							charLUK[j] += LUKincrease
							charALC[j] += ALCincrease
						j += 1
					
					if levelupstring != "":
						await client.send_message(message.channel, levelupstring)
						
						
					if state == "choice":
						eventdescstring = eventdescription
						
						i = 0
						for action in eventactions:
							if runeventactions == True:
								if action == "RH-":
									playerselected = round(random.randint(1, partysize - 1))
									charhealth[playerselected] -= eventactionarguments[i]
									eventdescstring += "\n" + charname[playerselected] + " loses " + str(eventactionarguments[i]) + " Health."
								if action == "FL+":
									if eventactionarguments[i] < len(flags):
										flags[eventactionarguments[i]] = 1
								if action == "FL-":
									if eventactionarguments[i] < len(flags):
										flags[eventactionarguments[i]] = 0
								
							if action == "RESET":
								resetvalid = 1
							if action == "END":
								state = "normal"
								partyevent = 0
								infotextdisplay = True
							i += 1
						
						if infotextdisplay == True:
							await client.send_message(message.channel, eventdescstring)
					
					if state == "normal":
						if infotextdisplay == True:
							locationdata = find_from_id(locationspath, partylocation)
							locationdatapos = 0
							locationname = split_string(locationdata, locationdatapos, '|', "string")
							locationdatapos = find_string_separator(locationdata, locationdatapos, '|')
							locationshortname = split_string(locationdata, locationdatapos, '|', "string")
							locationdatapos = find_string_separator(locationdata, locationdatapos, '|')
							locationdescription = split_string(locationdata, locationdatapos, '|', "string")
							locationdatapos = find_string_separator(locationdata, locationdatapos, '|')
							locationmaxlevel = split_string(locationdata, locationdatapos, '|', "string")
							locationdatapos = find_string_separator(locationdata, locationdatapos, '|')
							if locationmaxlevel!= "":
								locationmaxlevel = int(locationmaxlevel)
							locationnativespecies = split_string(locationdata, locationdatapos, '|', "string")
							locationdatapos = find_string_separator(locationdata, locationdatapos, '|')
							locationdestinations = split_string(locationdata, locationdatapos, '|', "string")
							locationdatapos = find_string_separator(locationdata, locationdatapos, '|')
							
							locationactions = [""] * 10
							i = 0
							while locationdatapos < len(locationdata):
								locationactions[i] = split_string(locationdata, locationdatapos, ';', "string").replace(' ', '')
								locationdatapos = find_string_separator(locationdata, locationdatapos, ';')
								i += 1
							
							locationnativespecieslist = []
							i = 1
							while i < len(locationnativespecies):
								newspecies = split_string(locationnativespecies, i, ';', "string")
								i = find_string_separator(locationnativespecies, i, ';')
								if newspecies.rstrip() != "":
									locationnativespecieslist.append(newspecies)
								else:
									break
							
							locationdestinationslist = []
							i = 1
							while i < len(locationdestinations):
								newdestination = split_string(locationdestinations, i, ';', "string")
								i = find_string_separator(locationdestinations, i, ';')
								if newdestination.rstrip() != "":
									locationdestinationslist.append(int(newdestination))
								else:
									break
							
							availableactions = ""
							for action in locationactions:
								if action == commandsymbol + "explore":
									availableactions += "**" + commandsymbol + "explore** to look for things to fight or people to help.\n"
								if action == commandsymbol + "sleep":
									availableactions += "**" + commandsymbol + "sleep** at an inn. Inns cost 50 Gold here.\n"
								if action == commandsymbol + "travel":
									firstdestination = True
									destinationsstring = ""
									i = 0
									while i < len(locationdestinationslist):
										if firstdestination == False:
											destinationsstring += ","
										if i == len(locationdestinationslist) - 1 and firstdestination == False:
											destinationsstring += " or"
										firstdestination = False
										
										destinationdata = find_from_id(locationspath, locationdestinationslist[i])
										destinationdatapos = 0
										destinationname = split_string(destinationdata, destinationdatapos, '|', "string")
										destinationname = destinationname.rstrip()
										destinationname = destinationname.lstrip()
										destinationdatapos = find_string_separator(destinationdata, destinationdatapos, '|')
										destinationshortname = split_string(destinationdata, destinationdatapos, '|', "string")
										destinationshortname = destinationshortname.rstrip()
										destinationshortname = destinationshortname.lstrip()
										
										if destinationname != "":
											destinationsstring += " " + destinationname + " [" + destinationshortname + "]"
										i += 1
										
									if len(locationdestinationslist) != 0:
										availableactions += "**" + commandsymbol + "travel <location>** to a different place.\nYou can travel to" + destinationsstring + "."
							await client.send_message(message.channel, locationdescription + "\nThings to do:\n" + availableactions)
					if state == "battle":
						if findencounter == True:
							if random.randint(1, 10) > 2 or exploretype == "travel": # Enemy encounter
								maxencounters = random.randint(1, encountersize)
								encounter = []
								availableencounters = []
								
								j = 0
								while j < 256:
									e = find_from_id(enemiespath, j)
									if e != "":
										encounterpos = 0						
										ename = split_string(e, encounterpos, '|', "string")
										encounterpos = find_string_separator(e, encounterpos, '|')
										elevel = split_string(e, encounterpos, '|', "string")
										encounterpos = find_string_separator(e, encounterpos, '|')
										efamily = split_string(e, encounterpos, '|', "string")
										encounterpos = find_string_separator(e, encounterpos, '|')
										especies = split_string(e, encounterpos, '|', "string")
										encounterpos = find_string_separator(e, encounterpos, '|')
										if (int(elevel) > averagepartylevel - encounterlevelrange and int(elevel) < averagepartylevel + encounterlevelrange and int(elevel) <= locationmaxlevel) or (int(elevel) < averagepartylevel - encounterlevelrange and int(elevel) == locationmaxlevel):
											if len(locationnativespecieslist) > 0:
												for member in locationnativespecieslist:
													if especies == member:
														availableencounters.append(e)
														break
											else:
												availableencounters.append(e)
									else:
										break
									j += 1
								if len(availableencounters) > 0:
									j = 0
									while j < maxencounters:
										encounter.append(availableencounters[random.randint(0, len(availableencounters) - 1)])
										j += 1
								
								encounterquantity = len(encounter)
								
								if encounterquantity > 0:
									i = 0
									while i < encounterquantity:
										encounterid.append(find_id_in_file(enemiespath, encounter[i]))
										encounterpos = 0
										encountername.append(split_string(encounter[i], encounterpos, '|', "string"))
										encounterpos = find_string_separator(encounter[i], encounterpos, '|')
										encounterlevel.append(split_string(encounter[i], encounterpos, '|', "string"))
										encounterpos = find_string_separator(encounter[i], encounterpos, '|')
										encounterfamily.append(split_string(encounter[i], encounterpos, '|', "string"))
										encounterpos = find_string_separator(encounter[i], encounterpos, '|')
										encounterspecies.append(split_string(encounter[i], encounterpos, '|', "string"))
										encounterpos = find_string_separator(encounter[i], encounterpos, '|')
										encounterATK.append(split_string(encounter[i], encounterpos, '|', "string"))
										encounterpos = find_string_separator(encounter[i], encounterpos, '|')
										encounterDEF.append(split_string(encounter[i], encounterpos, '|', "string"))
										encounterpos = find_string_separator(encounter[i], encounterpos, '|')
										encounterRES.append(split_string(encounter[i], encounterpos, '|', "string"))
										encounterpos = find_string_separator(encounter[i], encounterpos, '|')
										encounterAGI.append(split_string(encounter[i], encounterpos, '|', "string"))
										encounterpos = find_string_separator(encounter[i], encounterpos, '|')
										encounterspecials.append(split_string(encounter[i], encounterpos, '|', "string"))
										encounterpos = find_string_separator(encounter[i], encounterpos, '|')
										encountercardrarity.append(split_string(encounter[i], encounterpos, '|', "string"))
										
										encounterhealthmax.append(round((100 + 20 * int(encounterlevel[i])) * (1 + 0.1 * int(encounterDEF[i]))))
										encounterhealth.append(encounterhealthmax[i])
										i += 1
									encounterstatuspoisoned = [0] * encounterquantity
									encounterstatusconfused = [0] * encounterquantity
									encountercursetoxicblight = [0] * encounterquantity
									encountercursevoidgaze = [0] * encounterquantity
									encounterdarksigilcaster = [0] * encounterquantity
									encounterdarksigilcountdown = [0] * encounterquantity
									
									state = "battle"
									infotextdisplay = True
									defending = [False] * partysize
									
									i = 0
									while i < encounterquantity:
										validcodex = find_in_file(codexpath, encounterfamily[i] + "|", "")
										if validcodex != "":
											codexid = find_id_in_file(codexpath, validcodex)
											discoveredcodex[codexid - 1] = 1
										validcodex = find_in_file(codexpath, encounterspecies[i] + "|", "")
										if validcodex != "":
											codexid = find_id_in_file(codexpath, validcodex)
											discoveredcodex[codexid - 1] = 1
										i += 1
									
									if encounterquantity == 1:
										if exploretype == "travel":
											await client.send_message(message.channel, "You tried to travel, but were interrupted by " + encountername[0] + "!")
										else:
											await client.send_message(message.channel, encountername[0] + " was encountered!")
									else:
										if exploretype == "travel":
											await client.send_message(message.channel, "You tried to travel, but were interrupted by " + encountername[0] + " and company!")
										else:
											await client.send_message(message.channel, encountername[0] + " and company were encountered!")
								else:
									if exploretype == "travel":
										partylocation = destination
										newlocationdata = find_from_id(locationspath, partylocation)
										newlocationname = split_string(newlocationdata, 0, "|", "string").rstrip()
										infotextdisplay = True
										await client.send_message(message.channel, "You travel to " + newlocationname + ".")
									else:
										await client.send_message(message.channel, "You take a leisurely stroll. What a functionally useless yet pleasant activity!")
							else: # Event
								eventdata = fetch_from_database(eventpath, "|l:" + str(partylocation) + "|", "", "")
								if eventdata == "":
									await client.send_message(message.channel, "You take a leisurely stroll. What a functionally useless yet pleasant activity!")
								else:
									state = "choice"
									partyevent = find_id_in_file(eventpath, eventdata)
									eventdatapos = 0
									eventallowflag = split_string(eventdata, eventdatapos, '|', "string")
									eventallowflag = eventallowflag[2:]
									eventdatapos = find_string_separator(eventdata, eventdatapos, '|')
									eventdisallowflag = split_string(eventdata, eventdatapos, '|', "string")
									eventdisallowflag = eventdisallowflag[2:]
									eventdatapos = find_string_separator(eventdata, eventdatapos, '|')
									eventlocation = split_string(eventdata, eventdatapos, '|', "string")
									eventlocation = eventlocation[2:]
									eventdatapos = find_string_separator(eventdata, eventdatapos, '|')
									eventactionstring = split_string(eventdata, eventdatapos, '|', "string")
									eventdatapos = find_string_separator(eventdata, eventdatapos, '|')
									eventcommandstring = split_string(eventdata, eventdatapos, '|', "string")
									eventdatapos = find_string_separator(eventdata, eventdatapos, '|')
									eventdescription = split_string(eventdata, eventdatapos, '|', "string")
									eventdescription = eventdescription.replace('\\n', '\n')
									eventdatapos = find_string_separator(eventdata, eventdatapos, '|')
									eventactions = [""] * 10
									eventactionarguments = [""] * 10
									eventcommands = [""] * 10
									eventcommandresults = [[""] * 10] * 10
									eventcommandflags = [[""] * 10] * 10
									
									i = 0
									k = 0
									while i < len(eventactionstring):
										if eventactionstring[i] != ";":
											if len(eventactions[k]) < 3:
												eventactions[k] += eventactionstring[i]
											else:
												eventactionarguments[k] += eventactionstring[i]
										else:
											if eventactionarguments[k] != "":
												eventactionarguments[k] = int(eventactionarguments[k])
											k += 1
										i += 1
										
									i = 0
									k = 0
									l = 0
									m = 0
									while i < len(eventcommandstring):
										if l == 0: # Check command text
											if eventcommandstring[i] != ";":
												if eventcommandstring[i] == "(":
													l = 1
												else:
													eventcommands[k] += eventcommandstring[i]
											else:
												eventcommandresults[k][m] = int(eventcommandresults[k][m])
												k += 1
										elif l == 1: # Check command destination
											if eventcommandstring[i] == ")":
												l = 0
											elif eventcommandstring[i] == "[":
												l = 2
											elif eventcommandstring[i] == "]":
												m += 1
											else:
												eventcommandresults[k][m] += eventcommandstring[i]
										elif l == 2:
											if eventcommandstring[i] == ":":
												l = 1
											else:
												eventcommandflags[k][m] += eventcommandstring[i]
											
										i += 1
					
						idlemessage = "You are currently fighting:\n"
						
						i = 0
						while i < encounterquantity:
							if encounterhealth[i] != 0:
								firststatus = True
								idlemessage += encountername[i] + " [" + str(i + 1) + "] | Level " + str(encounterlevel[i]) + "\nHealth: " + str(encounterhealth[i]) + "/" + str(encounterhealthmax[i]) + "\n"
								statusmessage = ""
								if encounterstatusconfused[i] == 1:
									if firststatus == False:
										statusmessage += " | "
									statusmessage += "Confused"
									firststatus = False
								if encounterstatuspoisoned[i] == 1:
									if firststatus == False:
										statusmessage += " | "
									statusmessage += "Poisoned"
									firststatus = False
								if encountercursevoidgaze[i] == 1:
									if firststatus == False:
										statusmessage += " | "
									statusmessage += "Void Gaze"
									firststatus = False
								if encountercursetoxicblight[i] == 1:
									if firststatus == False:
										statusmessage += " | "
									statusmessage += "Toxic Blight"
									firststatus = False
								if statusmessage != "":
									idlemessage += "Effects: " + statusmessage
								idlemessage += "\n"
							i += 1
						k = 0
						while k < partysize:
							if actionqueue[k] == 0:
								battleaction = "Attack -> " + encountername[actiontarget[k]] + " [" + str(actiontarget[k] + 1) + "]"
							elif actionqueue[k] == 1:
								battleaction = "Defend"
							elif actionqueue[k] == 2:
								battleaction = "Run"
							elif actionqueue[k] == 3:
								item = find_from_id(itemspath, itemqueue[k])
								itemname = split_string(item, 0, '|', "string")
								battleaction = itemname + " -> " + charname[itemtarget[k]]
							elif actionqueue[k] == 4:
								skillname = skill_database(skillqueue[k], "", "name")
								skilltype = skill_database(skillqueue[k], "", "type")
								
								battleaction = skillname
								if skilltype != "guard" and skilltype != "curse":
									battleaction += " -> " + encountername[actiontarget[k]] + " [" + str(actiontarget[k] + 1) + "]"
							elif actionqueue[k] == 5:
								battleaction = "Examine -> " + encountername[actiontarget[k]] + " [" + str(actiontarget[k] + 1) + "]"
							else:
								battleaction = "Unknown"
								
							manastring = ""
							secondarymanastring = ""
							if charmanamax[k] != 0:
								manastring = " | Mana: " + str(charmana[k]) + "/" + str(charmanamax[k])
							if charsecondarymanamax[k] != 0:
								secondarymanamodifier = 0
								secondarymanamaxmodifier = secondarymanamodifier
								if charclass[k] == "cat":
									secondarymanamodifier = -10
									secondarymanamaxmodifier = secondarymanamodifier
								if charclass[k] == "bun":
									secondarymanamaxmodifier = -50
									if charsecondarymana[k] > 50:
										charsecondarymananame[k] = bunscaleright
										secondarymanamodifier = -50
									else:
										charsecondarymananame[k] = bunscaleleft
										secondarymanamodifier = (50 - charsecondarymana[k]) * 2 + 1 - 50
										if secondarymanamodifier > 50:
											secondarymanamodifier = 50
								secondarymanastring = " | " + charsecondarymananame[k] + ": " + str(charsecondarymana[k] + secondarymanamodifier) + "/" + str(charsecondarymanamax[k] + secondarymanamaxmodifier)
							idlemessage += "\n" + charname[k] + " | Level " + str(charlevel[k]) + " | " + charclassfull[k] + "\nHealth: " + str(charhealth[k]) + "/" + str(charhealthmax[k]) + manastring + secondarymanastring
							
							firststatus = True
							statusmessage = ""
							if charstatusconfused[k] == 1:
								if firststatus == False:
									statusmessage += " | "
								statusmessage += "Confused"
								firststatus = False
							if charstatuspoisoned[k] == 1:
								if firststatus == False:
									statusmessage += " | "
								statusmessage += "Poisoned"
								firststatus = False
							if charguardbunnyears[k] == 1:
								if firststatus == False:
									statusmessage += " | "
								statusmessage += "Bunny Ears"
								firststatus = False
							if charguardhyperlove[k] == 1:
								if firststatus == False:
									statusmessage += " | "
								statusmessage += "Hyper Love"
								firststatus = False
							if charguardtoughfur[k] == 1:
								if firststatus == False:
									statusmessage += " | "
								statusmessage += "Tough Fur"
								firststatus = False
							if statusmessage != "":
								idlemessage += "\nEffects: " + statusmessage
							idlemessage += "\n- " + str(battleaction) + "\n"
							k += 1
							
						if infotextdisplay == True:
							await client.send_message(message.channel, idlemessage)
							
					if state == "dungeon":
						print("how the fuck")
					
					# Check stats
					j = 0				
					while j < partysize:	
						if charhealth[j] < 0:
							charhealth[j] = 0
						if charmana[j] < 0:
							charmana[j] = 0
						if charsecondarymana[j] < 0:
							charsecondarymana[j] = 0
							
						if charhealth[j] > charhealthmax[j]:
							charhealth[j] = charhealthmax[j]
						if charmana[j] > charmanamax[j]:
							charmana[j] = charmanamax[j]
						if charsecondarymana[j] > charsecondarymanamax[j]:
							charsecondarymana[j] = charsecondarymanamax[j]
						j += 1							
					
					
					j = 0
					while j < partysize:
						# Saving Data
						chardataarray[charlevelpos + j * databuffer] = charlevel[j]
						chardataarray[charATKpos + j * databuffer] = charATK[j]
						chardataarray[charDEFpos + j * databuffer] = charDEF[j]
						chardataarray[charMAGpos + j * databuffer] = charMAG[j]
						chardataarray[charAGIpos + j * databuffer] = charAGI[j]
						chardataarray[charLUKpos + j * databuffer] = charLUK[j]
						chardataarray[charALCpos + j * databuffer] = charALC[j]
						chardataarray[charstatuspoisonedpos + j * databuffer] = charstatuspoisoned[j]
						chardataarray[charstatusconfusedpos + j * databuffer] = charstatusconfused[j]
						chardataarray[charguardbunnyearspos + j * databuffer] = charguardbunnyears[j]
						chardataarray[charguardhyperlovepos + j * databuffer] = charguardhyperlove[j]
						chardataarray[charguardtoughfurpos + j * databuffer] = charguardtoughfur[j]
						encounterdataarray[encounteractionqueuepos + j] = actionqueue[j]
						encounterdataarray[encounteritemqueuepos + j] = itemqueue[j]
						encounterdataarray[encounteritemtargetpos + j] = itemtarget[j]
						encounterdataarray[encounterskillqueuepos + j] = skillqueue[j]
						encounterdataarray[encounteractiontargetpos + j] = actiontarget[j]
						
						i = 0
						while i < 10:
							if i < len(charname[j]):
								chardataarray[charnamepos + i + j * databuffer] = ord(charname[j][i])
							else:
								chardataarray[charnamepos + i + j * databuffer] = 0
							i += 1
						i = 0
						while i < 5:
							if i < len(charclass[j]):
								chardataarray[charclasspos + i + j * databuffer] = ord(charclass[j][i])
							else:
								chardataarray[charclasspos + i + j * databuffer] = 0
							i += 1
						
						i = 0
						while i < len(charpassiveskills[j]):
							skilllevel = skill_database(i, "", "level")
							skillclass = skill_database(i, "", "class")
							skillpassive = skill_database(i, "", "passive")
							if charlevel[j] >= skilllevel and charclass[j] == skillclass and skillpassive == True:
								charpassiveskills[j][i] = 1
							chardataarray[charpassiveskillspos + j * databuffer] = charpassiveskills[j][i]
							i += 1
						
						expbytes = charexp[j].to_bytes(2, "little")
						i = 0
						for byte in expbytes:
							chardataarray[charexppos + i + j * databuffer] = expbytes[i]
							i += 1
						
						healthbytes = charhealth[j].to_bytes(2, "little")
						i = 0
						for byte in healthbytes:
							chardataarray[charhealthpos + i + j * databuffer] = healthbytes[i]
							i += 1
						manabytes = charmana[j].to_bytes(2, "little")
						i = 0
						for byte in manabytes:
							chardataarray[charmanapos + i + j * databuffer] = manabytes[i]
							i += 1
						secondarymanabytes = charsecondarymana[j].to_bytes(2, "little")
						i = 0
						for byte in secondarymanabytes:
							chardataarray[charsecondarymanapos + i + j * databuffer] = secondarymanabytes[i]
							i += 1
						
						j += 1
					
					i = 0
					while i < encounterquantity:
						encounterdataarray[encounteridpos + i * encounterdatabuffer] = encounterid[i]
						encounterdataarray[encounterstatuspoisonedpos + i * encounterdatabuffer] = encounterstatuspoisoned[i]
						encounterdataarray[encounterstatusconfusedpos + i * encounterdatabuffer] = encounterstatusconfused[i]
						encounterdataarray[encounterdarksigilcountdownpos + i * encounterdatabuffer] = encounterdarksigilcountdown[i]
						encounterdataarray[encounterdarksigilcasterpos + i * encounterdatabuffer] = encounterdarksigilcaster[i]
						encounterdataarray[encountercursetoxicblightpos + i * encounterdatabuffer] = encountercursetoxicblight[i]
						
						i += 1
					
					encounterdataarray[encounterquantitypos] = encounterquantity
						
					if state == "normal":
						partydataarray[partystatepos] = 0
					elif state == "choice":
						partydataarray[partystatepos] = 1
					elif state == "battle":
						partydataarray[partystatepos] = 2
					else:
						partydataarray[partystatepos] = 3
					
					partydataarray[partyindungeonpos] = partyindungeon
					partydataarray[partydungeonXpos] = partydungeonX
					partydataarray[partydungeonYpos] = partydungeonY
					
					partydataarray[partycollectvalidatorpos] = collectvalidator
					
					partydataarray[partylocationpos] = partylocation
					partydataarray[partydungeonpos] = partydungeon
					partydataarray[partyeventpos] = partyevent
					
					fundsbytes = funds.to_bytes(2, "little")
					i = 0
					for byte in fundsbytes:
						partydataarray[partyfundspos + i] = fundsbytes[i]
						i += 1
					
					j = 0
					while j < len(flags):
						flagdataarray[j] = flags[j]
						j += 1
					
					k = 0
					while k < encounterquantity:
						encounterhealthbytes = encounterhealth[k].to_bytes(2, "little")
						i = 0
						for byte in encounterhealthbytes:
							encounterdataarray[encounterhealthpos + i + k * encounterdatabuffer] = encounterhealthbytes[i]
							i += 1
						k += 1
					
					i = 0
					while i < availableprofessions:
						if professionexp[i] >= professionexpmax[i]:
							professionexp[i] -= professionexpmax[i]
							professionlevel[i] += 1
							await client.send_message(message.channel, professionname[i] + " profession leveled up! " + professionname[i] + " profession is now level " + str(professionlevel[i]) + ".")
						
						professiondataarray[i] = professionlevel[i]
						professionexpbytes = professionexp[i].to_bytes(2, "little")
						k = 0
						for byte in professionexpbytes:
							professiondataarray[(i * 2) + professionexpdatabuffer + k] = professionexpbytes[k]
							k += 1
						i += 1
					
					i = 0
					while i < len(tcgdeck):
						tcgdataarray[tcgdeckpos + i] = tcgdeck[i]
						i += 1
					
					i = 0
					while i < len(tcgcardsowned):
						tcgdataarray[tcgcardsownedpos + i] = tcgcardsowned[i]
						i += 1
					
					i = 0
					while i < 100:
						if partyitemsquantity[i] <= 0:
							partyitemsquantity[i] = 0
							partyitems[i] = 0
						partydataarray[partyitemspos + i] = partyitems[i]
						partydataarray[partyitemsquantitypos + i] = partyitemsquantity[i]
						i += 1
					
					i = 0
					while i < len(discoveredrecipes):
						recipedataarray[discoveredrecipepos + i] = discoveredrecipes[i]
						i += 1

					i = 0
					while i < len(discoveredcodex):
						codexdataarray[discoveredcodexpos + i] = discoveredcodex[i]
						i += 1
					
					partydataarray[partyresetvalidpos] = resetvalid
					partydataarray[partyvaliddatapos] = validdata
					
					individualdataarray[individualvaliddatapos] = validindividualdata
					
					if team != "":
						if not os.path.exists(datadir + pathfolder + pathid):
							os.makedirs(datadir + pathfolder + pathid)
						save_data(chardatapath_full, chardataarray)
						save_data(partydatapath_full, partydataarray)
						save_data(flagdatapath_full, flagdataarray)
						save_data(professiondatapath_full, professiondataarray)
						save_data(tcgdatapath_full, tcgdataarray)
						save_data(encounterdatapath_full, encounterdataarray)
						save_data(recipedatapath_full, recipedataarray)
						save_data(codexdatapath_full, codexdataarray)
						save_data(criticaldatapath_full, criticaldataarray)
						
					if os.path.isfile(alchemycooldownpath) == False:
						save_to_file(alchemycooldownpath, "", "")
			
			#if privatemessage == True:
			if individualreadonly == True and selectivereadonly == False:
				i = 0
				while i < 10:
					if i < len(charname[0]):
						individualdataarray[individualnamepos + i] = ord(charname[0][i])
					else:
						individualdataarray[individualnamepos + i] = 0
					i += 1
				i = 0
				while i < 5:
					if i < len(charclass[0]):
						individualdataarray[individualclasspos + i] = ord(charclass[0][i])
					else:
						individualdataarray[individualclasspos + i] = 0
					i += 1
					
				individualdataarray[individualATKpos] = charATK[0]
				individualdataarray[individualDEFpos] = charDEF[0]
				individualdataarray[individualMAGpos] = charMAG[0]
				individualdataarray[individualAGIpos] = charAGI[0]
				individualdataarray[individualLUKpos] = charLUK[0]
				individualdataarray[individualALCpos] = charALC[0]
				
				save_data(individualdatapath_full, individualdataarray)
					
			if individualreadonly == False:
				if collectingdata == False:
					i = 0
					while i < 10:
						if i < len(charname[0]):
							individualdataarray[individualnamepos + i] = ord(charname[0][i])
						else:
							individualdataarray[individualnamepos + i] = 0
						i += 1
					i = 0
					while i < 5:
						if i < len(charclass[0]):
							individualdataarray[individualclasspos + i] = ord(charclass[0][i])
						else:
							individualdataarray[individualclasspos + i] = 0
						i += 1
				
				i = 0
				while i < len(charpassiveskills[0]):
					skilllevel = skill_database(i, "", "level")
					skillclass = skill_database(i, "", "class")
					skillpassive = skill_database(i, "", "passive")
					if charlevel[0] >= skilllevel and charclass[0] == skillclass and skillpassive == True:
						charpassiveskills[0][i] = 1
					individualdataarray[individualpassiveskillspos] = charpassiveskills[0][i]
					i += 1
				
				expmaxdata = round(50 * (5**(charlevel[0] - 1)))
				
				exparray = [individualdataarray[individualexppos], individualdataarray[individualexppos + 1]]
				charexp[0] += int.from_bytes(exparray, "little")
				expmaxdata = round(50 * (5**(charlevel[0] - 1)))
				j = charlevel[0] - 1
				while j > 0:
					expincrease = round(50 * (5**(j - 1)))
					charexp[0] += expincrease
					j -= 1
					
				charlevel[0] = individualdataarray[individuallevelpos]
				if charlevel[0] == 0:
					charlevel[0] = 1
				while charexp[0] >= charexpmax[0]:
					charexp[0] -= charexpmax[0]
					charlevel[0] += 1
					charexpmax[0] = round(50 * (5**(charlevel[0] - 1)))
					
					statsstring = find_in_file(statspath, "| " + charclass[0] + " |", "")
					statsstringpos = 0
					statsstringpos = find_string_separator(statsstring, statsstringpos, '(')
					ATKincrease = split_string(statsstring, statsstringpos, ')', "string")
					ATKincrease = int(ATKincrease)
					statsstringpos = find_string_separator(statsstring, statsstringpos, '(')
					DEFincrease = split_string(statsstring, statsstringpos, ')', "string")
					DEFincrease = int(DEFincrease)
					statsstringpos = find_string_separator(statsstring, statsstringpos, '(')
					MAGincrease = split_string(statsstring, statsstringpos, ')', "string")
					MAGincrease = int(MAGincrease)
					statsstringpos = find_string_separator(statsstring, statsstringpos, '(')
					AGIincrease = split_string(statsstring, statsstringpos, ')', "string")
					AGIincrease = int(AGIincrease)
					statsstringpos = find_string_separator(statsstring, statsstringpos, '(')
					LUKincrease = split_string(statsstring, statsstringpos, ')', "string")
					LUKincrease = int(LUKincrease)
					statsstringpos = find_string_separator(statsstring, statsstringpos, '(')
					ALCincrease = split_string(statsstring, statsstringpos, ')', "string")
					ALCincrease = int(ALCincrease)
					
					charATK[0] += ATKincrease
					charDEF[0] += DEFincrease
					charMAG[0] += MAGincrease
					charAGI[0] += AGIincrease
					charLUK[0] += LUKincrease
					charALC[0] += ALCincrease
					
				individualdataarray[individuallevelpos] = charlevel[0]
				
				individualdataarray[individualATKpos] = charATK[0]
				individualdataarray[individualDEFpos] = charDEF[0]
				individualdataarray[individualMAGpos] = charMAG[0]
				individualdataarray[individualAGIpos] = charAGI[0]
				individualdataarray[individualLUKpos] = charLUK[0]
				individualdataarray[individualALCpos] = charALC[0]
				
				i = 0
				expbytes = charexp[0].to_bytes(2, "little")
				for byte in expbytes:
					individualdataarray[individualexppos + i] = expbytes[i]
					i += 1
				
				charhealth[0] = charhealthmax[0]
				charmana[0] = charmanamax[0]
				charsecondarymana[0] = charsecondarymanamax[0]
				healthbytes = charhealth[0].to_bytes(2, "little")
				i = 0
				for byte in healthbytes:
					individualdataarray[individualhealthpos + i] = healthbytes[i]
					i += 1
				manabytes = charmana[0].to_bytes(2, "little")
				i = 0
				for byte in manabytes:
					individualdataarray[individualmanapos + i] = manabytes[i]
					i += 1
				secondarymanabytes = charsecondarymana[0].to_bytes(2, "little")
				i = 0
				for byte in secondarymanabytes:
					individualdataarray[individualsecondarymanapos + i] = secondarymanabytes[i]
					i += 1
			
				fundsarray = [individualdataarray[individualfundspos], individualdataarray[individualfundspos + 1]]
				funds += int.from_bytes(fundsarray, "little")
				fundsbytes = funds.to_bytes(2, "little")
				i = 0
				for byte in fundsbytes:
					individualdataarray[individualfundspos + i] = fundsbytes[i]
					i += 1
					
				i = 0
				while i < availableprofessions:
					professionexpmax[i] = round(50 * (5**(professionlevel[i] - 1)))
					professionexparray = [individualdataarray[(i * 2) + individualprofessionskillspos + professionexpdatabuffer], professiondataarray[(i * 2) + individualprofessionskillspos + professionexpdatabuffer + 1]]
					professionexp[i] = int.from_bytes(professionexparray, "little")
					j = professionlevel[i] - 1
					while j > 0:
						expincrease = round(50 * (5**(j - 1)))
						professionexp[i] += expincrease
						j -= 1
					professionlevel[i] = individualdataarray[individualprofessionskillspos + i]
					i += 1
				i = 0
				while i < availableprofessions:
					while professionexp[i] >= professionexpmax[i]:
						professionexp[i] -= professionexpmax[i]
						professionlevel[i] += 1
						professionexpmax[i] = round(50 * (5**(professionlevel[i] - 1)))
					
					individualdataarray[(i * 2) + individualprofessionskillspos + i] = professionlevel[i]
					professionexpbytes = professionexp[i].to_bytes(2, "little")
					k = 0
					for byte in professionexpbytes:
						individualdataarray[(i * 2) + individualprofessionskillspos + professionexpdatabuffer + k] = professionexpbytes[k]
						k += 1
					i += 1
				
				i = 0
				while i < len(tcgdeck):
					individualdataarray[individualdeckpos + i] = tcgdeck[i]
					i += 1
				
				i = 0
				while i < len(tcgcardsowned):
					tcgcardsowned[i] += individualdataarray[individualcardsownedpos + i]
					individualdataarray[individualcardsownedpos + i] = tcgcardsowned[i]
					i += 1
				
				i = 0
				while i < len(discoveredrecipes):
					recipedata = individualdataarray[individualdiscoveredrecipepos + i]
					if recipedata == 1:
						discoveredrecipes[i] = 1
					individualdataarray[individualdiscoveredrecipepos + i] = discoveredrecipes[i]
					i += 1

				i = 0
				while i < len(discoveredcodex):
					codexdata = individualdataarray[individualdiscoveredcodexpos + i]
					if codexdata == 1:
						discoveredcodex[i] = 1
					individualdataarray[individualdiscoveredcodexpos + i] = discoveredcodex[i]
					i += 1
				
				save_data(individualdatapath_full, individualdataarray)
			
		# Extra / hidden	
		if nopunctmessage == "hey adventurer" or nopunctmessage == "hi adventurer" or nopunctmessage == "sup adventurer" or nopunctmessage == "hows it going adventurer" or nopunctmessage == "whats up adventurer":
			greetingsmessages = []
			greetingsmessages.append("Hey.")
			greetingsmessages.append("Hi.")
			greetingsmessages.append("How's it going.")
			greetingsmessages.append("Sup.")
			greetingsmessages.append("Bye.")
			await client.send_message(message.channel, greetingsmessages[random.randint(0, len(greetingsmessages) - 1)])
		
client.run("MjEyNjIyMTQ3MDM2Nzc0NDAy.CoujeA.FBV5Poj8KOMCZWu1Hr8zDgPRqXk")