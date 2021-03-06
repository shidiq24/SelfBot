# -*- coding: utf-8 -*-

from LineAPI.linepy import *
from gtts import gTTS
from bs4 import BeautifulSoup
from datetime import datetime
from googletrans import Translator
import ast, codecs, json, os, pytz, re, random, requests, sys, time, urllib.parse

listApp = ["CHROMEOS", "DESKTOPWIN", "DESKTOPMAC", "IOSIPAD", "WIN10"]
try:
	for app in listApp:
		try:
			try:
				with open("authToken.txt", "r") as token:
					authToken = token.read()
					if not authToken:
						client = LINE("")   #PH-13
						with open("authToken.txt","w") as token:
							token.write(client.authToken)
						continue
					client = LINE(authToken, speedThrift=False, appName="{}\t2.1.5\tPH-13\t1".format(app))
				break
			except Exception as error:
				print(error)
				if error == "REVOKE":
					exit()
				elif "auth" in error:
					continue
				else:
					exit()
		except Exception as error:
			print(error)
except Exception as error:
	print(error)
with open("authToken.txt", "w") as token:
    token.write(str(client.authToken))
clientMid = client.profile.mid
clientStart = time.time()
clientPoll = OEPoll(client)

languageOpen = codecs.open("language.json","r","utf-8")
tagmeOpen = codecs.open("tag.json","r","utf-8")
setting2Open = codecs.open("setting2.json","r","utf-8")
readOpen = codecs.open("read.json","r","utf-8")
settingsOpen = codecs.open("setting.json","r","utf-8")
unsendOpen = codecs.open("unsend.json","r","utf-8")

language = json.load(languageOpen)
tagme = json.load(tagmeOpen)
setting2 = json.load(setting2Open)
read = json.load(readOpen)
settings = json.load(settingsOpen)
unsend = json.load(unsendOpen)

def restartBot():
	print ("[ INFO ] BOT RESETTED")
	python = sys.executable
	os.execl(python, python, *sys.argv)

def logError(text):
    client.log("[ ERROR ] {}".format(str(text)))
    tz = pytz.timezone("Asia/Jakarta")
    timeNow = datetime.now(tz=tz)
    timeHours = datetime.strftime(timeNow,"(%H:%M)")
    day = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday","Friday", "Saturday"]
    hari = ["Minggu", "Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"]
    bulan = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
    inihari = datetime.now(tz=tz)
    hr = inihari.strftime('%A')
    bln = inihari.strftime('%m')
    for i in range(len(day)):
        if hr == day[i]: hasil = hari[i]
    for k in range(0, len(bulan)):
        if bln == str(k): bln = bulan[k-1]
    time = "{}, {} - {} - {} | {}".format(str(hasil), str(inihari.strftime('%d')), str(bln), str(inihari.strftime('%Y')), str(inihari.strftime('%H:%M:%S')))
    with open("errorLog.txt","a") as error:
        error.write("\n[{}] {}".format(str(time), text))

def timeChange(secs):
	mins, secs = divmod(secs,60)
	hours, mins = divmod(mins,60)
	days, hours = divmod(hours,24)
	weeks, days = divmod(days,7)
	months, weeks = divmod(weeks,4)
	text = ""
	if months != 0: text += "%02d Months" % (months)
	if weeks != 0: text += " %02d Weeks" % (weeks)
	if days != 0: text += " %02d Days" % (days)
	if hours !=  0: text +=  " %02d hours" % (hours)
	if mins != 0: text += " %02d mins" % (mins)
	if secs != 0: text += " %02d secs" % (secs)
	if text[0] == " ":
		text = text[1:]
	return text

def command(text):
	pesan = text.lower()
	if settings["setKey"] == True:
		if pesan.startswith(settings["keyCommand"]):
			cmd = pesan.replace(settings["keyCommand"],"")
		else:
			cmd = "Undefined command"
	else:
		cmd = text.lower()
	return cmd

def backupData():
	try:
		backup = read
		f = codecs.open('read.json','w','utf-8')
		json.dump(backup, f, sort_keys=True, indent=4, ensure_ascii=False)
		backup = tagme
		f = codecs.open('tag.json','w','utf-8')
		json.dump(backup, f, sort_keys=True, indent=4, ensure_ascii=False)
		backup = settings
		f = codecs.open('setting.json','w','utf-8')
		json.dump(backup, f, sort_keys=True, indent=4, ensure_ascii=False)
		backup = unsend
		f = codecs.open('unsend.json','w','utf-8')
		json.dump(backup, f, sort_keys=True, indent=4, ensure_ascii=False)
		return True
	except Exception as error:
		logError(error)
		return False

def menuHelp():
	if settings['setKey'] == True:
		key = settings['keyCommand']
	else:
		key = ''
	menuHelp =	"╔════➢ Help Message " + "\n" + \
				"╠ " + key + "Help" + "\n" + \
				"╠════➢ Status Command " + "\n" + \
				"╠ MyKey" + "\n" + \
				"╠ " + key + "Logout" + "\n" + \
				"╠ " + key + "Restart" + "\n" + \
				"╠ " + key + "Runtime" + "\n" + \
				"╠ " + key + "Speed" + "\n" + \
				"╠ " + key + "Status" + "\n" + \
				"╠════➢ Settings Command " + "\n" + \
				"╠ SetKey 「On/Off」" + "\n" + \
				"╠ " + key + "AutAdd 「On/Off」" + "\n" + \
				"╠ " + key + "AutJoin 「On/Off」" + "\n" + \
				"╠ " + key + "AutJoinTicket 「On/Off」" + "\n" + \
				"╠ " + key + "AutRead 「On/Off」" + "\n" + \
				"╠ " + key + "AutRespon 「On/Off」" + "\n" + \
				"╠ " + key + "Contact 「On/Off」" + "\n" + \
				"╠ " + key + "Post 「On/Off」" + "\n" + \
				"╠ " + key + "Sticker 「On/Off」" + "\n" + \
				"╠ " + key + "Unsend 「On/Off」" + "\n" + \
				"╠ " + key + "SetKey: 「text」" + "\n" + \
				"╠ " + key + "SetAdd: 「text」" + "\n" + \
				"╠ " + key + "SetRespon: 「text」" + "\n" + \
				"╠ " + key + "SetJoin: 「Text」" + "\n" + \
				"╠════➢ Self Command " + "\n" + \
				"╠ " + key + "ChangeName: 「Text」" + "\n" + \
				"╠ " + key + "ChangeBio: 「Text」" + "\n" + \
				"╠ " + key + "Me" + "\n" + \
				"╠ " + key + "MyMid" + "\n" + \
				"╠ " + key + "MyName" + "\n" + \
				"╠ " + key + "MyBio" + "\n" + \
				"╠ " + key + "MyPict" + "\n" + \
				"╠ " + key + "MyVid" + "\n" + \
				"╠ " + key + "MyCover" + "\n" + \
				"╠ " + key + "MyProfile" + "\n" + \
				"╠ " + key + "Mid @Mention" + "\n" + \
				"╠ " + key + "Name @Mention" + "\n" + \
				"╠ " + key + "Bio @Mention" + "\n" + \
				"╠ " + key + "Pict @Mention" + "\n" + \
				"╠ " + key + "Vid @Mention" + "\n" + \
				"╠ " + key + "Cover @Mention" + "\n" + \
				"╠ " + key + "Clone @Mention" + "\n" + \
				"╠ " + key + "Restore" + "\n" + \
				"╠ " + key + "Backup" + "\n" + \
				"╠ " + key + "FriendList" + "\n" + \
				"╠ " + key + "FriendInfo 「Number」" + "\n" + \
				"╠ " + key + "BList" + "\n" + \
				"╠ " + key + "FriendBc" + "\n" + \
				"╠ " + key + "ChangePict" + "\n" + \
				"╠════➢ Group Command " + "\n" + \
				"╠ " + key + "ChangeGName: 「Text」" + "\n" + \
				"╠ " + key + "GCreator" + "\n" + \
				"╠ " + key + "GID" + "\n" + \
				"╠ " + key + "GName" + "\n" + \
				"╠ " + key + "GPict" + "\n" + \
				"╠ " + key + "OpenQR" + "\n" + \
				"╠ " + key + "CloseQR" + "\n" + \
				"╠ " + key + "GList" + "\n" + \
				"╠ " + key + "MemList" + "\n" + \
				"╠ " + key + "PendingList" + "\n" + \
				"╠ " + key + "GInfo" + "\n" + \
				"╠ " + key + "Unsend 「*」" + "\n" + \
				"╠ " + key + "GroupBc: 「Text」" + "\n" + \
				"╠ " + key + "ChangeGPict" + "\n" + \
				"╠════➢ Special Command " + "\n" + \
				"╠ " + key + "Mimic 「On/Off」" + "\n" + \
				"╠ " + key + "MicList" + "\n" + \
				"╠ " + key + "MicAdd @Mention" + "\n" + \
				"╠ " + key + "MicDel @Mention" + "\n" + \
				"╠ " + key + "Delmentionme" + "\n" + \
				"╠ " + key + "Mentionme" + "\n" + \
				"╠ " + key + "Mentionall" + "\n" + \
				"╠ " + key + "Lurk 「On/Off」" + "\n" + \
				"╠ " + key + "Lurking" + "\n" + \
				"╠════➢ Media Command " + "\n" + \
				"╠ " + key + "InstaInfo 「Username」" + "\n" + \
				"╠ " + key + "InstaStory 「Username」" + "\n" + \
				"╠ " + key + "Quotes" + "\n" + \
				"╠ " + key + "Image 「Search」" + "\n" + \
				"╠ " + key + "Music 「Search」" + "\n" + \
				"╠ " + key + "Lyric 「Search」" + "\n" + \
				"╠ " + key + "Youtube 「Search」" + "\n" + \
				"╚════➢ Copyright @Python-3 "
	return menuHelp

def clientBot(op):
	try:
		if op.type == 0:
			print ("[ 0 ] END OF OPERATION")
			return

		if op.type == 5:
			print ("[ 5 ] NOTIFIED ADD CONTACT")
			if settings["autoAdd"] == True:
				client.findAndAddContactsByMid(op.param1)
			client.sendMention(op.param1, settings["autoAddMessage"], [op.param1])

		if op.type == 13:
			print ("[ 13 ] NOTIFIED INVITE INTO GROUP")
			if settings["autoJoin"] and clientMid in op.param3:
				client.acceptGroupInvitation(op.param1)
				client.sendMention(op.param1, settings["autoJoinMessage"], [op.param2])

		if op.type == 25:
			try:
				print("[ 26 ] SEND MESSAGE")
				msg = op.message
				text = str(msg.text)
				msg_id = msg.id
				receiver = msg.to
				sender = msg._from
				cmd = command(text)
				setKey = settings["keyCommand"].title()
				if settings["setKey"] == False:
					setKey = ''
				if msg.toType == 0 or msg.toType == 1 or msg.toType == 2:
					if msg.toType == 0:
						if sender != client.profile.mid:
							to = sender
						else:
							to = receiver
					elif msg.toType == 1:
						to = receiver
					elif msg.toType == 2:
						to = receiver
					if msg.contentType == 0:
						if cmd == "logout":
							client.sendMessage(to, "The Devil has killed")
							sys.exit("[ INFO ] BOT SHUTDOWN")
							return
						elif cmd == "restart":
							client.sendMessage(to, "Bot is RESETTED, the evil has been respawn")
							restartBot()
						elif cmd == "speed":
							start = time.time()
							client.sendMessage(to, "Speed ...")
							elapsed_time = time.time() - start
							client.sendMessage(to, "The Speed is {} detik".format(str(elapsed_time)))
						elif cmd == "runtime":
							timeNow = time.time()
							runtime = timeNow - clientStart
							runtime = timeChange(runtime)
							client.sendMessage(to, "Selfbot active for {}".format(str(runtime)))
						elif cmd.startswith("setkey: "):
							sep = text.split(" ")
							key = text.replace(sep[0] + " ","")
							if " " in key:
								client.sendMessage(to, "Key tidak bisa menggunakan spasi")
							else:
								settings["keyCommand"] = str(key).lower()
								client.sendMessage(to, "Berhasil mengubah set key command menjadi : 「{}」".format(str(key).lower()))
						elif cmd == "help":
							helpMessage = menuHelp()
							contact = client.getContact(sender)
							icon = "http://dl.profile.line-cdn.net/{}".format(contact.pictureStatus)
							name = contact.displayName
							link = "https://pa1.narvii.com/6547/d29a5e4bb3405d83fc15cf50ec057f41640618a8_hq.gif"
							client.sendFooter(to, helpMessage, icon, name, link)
						elif cmd == "tts":
							helpTextToSpeech = menuTextToSpeech()
							contact = client.getContact(sender)
							icon = "http://dl.profile.line-cdn.net/{}".format(contact.pictureStatus)
							name = contact.displayName
							link = "https://pa1.narvii.com/6547/d29a5e4bb3405d83fc15cf50ec057f41640618a8_hq.gif"
							client.sendFooter(to, helpTextToSpeech, icon, name, link)
						elif cmd == "translate":
							helpTranslate = menuTranslate()
							contact = client.getContact(sender)
							icon = "http://dl.profile.line-cdn.net/{}".format(contact.pictureStatus)
							name = contact.displayName
							link = "https://pa1.narvii.com/6547/d29a5e4bb3405d83fc15cf50ec057f41640618a8_hq.gif"
							client.sendFooter(to, helpTranslate, icon, name, link)


						elif cmd == "status":
							try:
								ret_ = "╔════➢ Status "
								if settings["autoAdd"] == True: ret_ += "\n╠ Auto Add : ON"
								else: ret_ += "\n╠ Auto Add : OFF"
								if settings["autoJoin"] == True: ret_ += "\n╠ Auto Join : ON"
								else: ret_ += "\n╠ Auto Join : OFF"
								if settings["autoJoin"] == True: ret_ += "\n╠ Auto Join Ticket : ON"
								else: ret_ += "\n╠ Auto Join Ticket : OFF"
								if settings["autoRead"] == True: ret_ += "\n╠ Auto Read : ON"
								else: ret_ += "\n╠ Auto Read : OFF"
								if settings["autoRespon"] == True: ret_ += "\n╠ Auto Respon : ON"
								else: ret_ += "\n╠ Auto Respon : OFF"
								if settings["checkContact"] == True: ret_ += "\n╠ Check Contact : ON"
								else: ret_ += "\n╠ Check Contact : OFF"
								if settings["checkPost"] == True: ret_ += "\n╠ Check Post : ON"
								else: ret_ += "\n╠ Check Post : OFF"
								if settings["checkSticker"] == True: ret_ += "\n╠ Check Sticker : ON"
								else: ret_ += "\n╠ Check Sticker : OFF"
								if settings["detectUnsend"] == True: ret_ += "\n╠ Detect Unsend : ON"
								else: ret_ += "\n╠ Detect Unsend : OFF"
								if settings["setKey"] == True: ret_ += "\n╠ Set Key : ON"
								else: ret_ += "\n╠ Set Key : OFF"
								ret_ +="\n╠ Auto Add Message : {}".format(settings["autoAddMessage"])
								ret_ +="\n╠ Auto Join Message : {}".format(settings["autoJoinMessage"])
								ret_ +="\n╠ Auto Respon Message : {}".format(settings["autoResponMessage"])
								ret_ += "\n╚════➢ Status "
								client.sendMessage(to, str(ret_))
							except Exception as error:
								logError(error)
						elif cmd == "autadd on":
							if settings["autoAdd"] == True:
								client.sendMessage(to, "Auto add is activated")
							else:
								settings["autoAdd"] = True
								client.sendMessage(to, "Berhasil mengaktifkan auto add")
						elif cmd == "autadd off":
							if settings["autoAdd"] == False:
								client.sendMessage(to, "Auto add telah nonaktif")
							else:
								settings["autoAdd"] = False
								client.sendMessage(to, "Berhasil menonaktifkan auto add")
						elif cmd == "autjoin on":
							if settings["autoJoin"] == True:
								client.sendMessage(to, "Auto join is on")
							else:
								settings["autoJoin"] = True
								client.sendMessage(to, "Auto Join is activated")
						elif cmd == "autjoin off":
							if settings["autoJoin"] == False:
								client.sendMessage(to, "Auto join telah nonaktif")
							else:
								settings["autoJoin"] = False
								client.sendMessage(to, "Berhasil menonaktifkan auto join")
						elif cmd == "autjointicket on":
							if settings["autoJoinTicket"] == True:
								client.sendMessage(to, "Auto join ticket telah aktif")
							else:
								settings["autoJoinTicket"] = True
								client.sendMessage(to, "Berhasil mengaktifkan auto join ticket")
						elif cmd == "autjointicket off":
							if settings["autoJoinTicket"] == False:
								client.sendMessage(to, "Auto join ticket telah nonaktif")
							else:
								settings["autoJoinTicket"] = False
								client.sendMessage(to, "Berhasil menonaktifkan auto join ticket")
						elif cmd == "autread on":
							if settings["autoRead"] == True:
								client.sendMessage(to, "Auto read telah aktif")
							else:
								settings["autoRead"] = True
								client.sendMessage(to, "Berhasil mengaktifkan auto read")
						elif cmd == "autread off":
							if settings["autoRead"] == False:
								client.sendMessage(to, "Auto read telah nonaktif")
							else:
								settings["autoRead"] = False
								client.sendMessage(to, "Berhasil menonaktifkan auto read")
						elif cmd == "autrespon on":
							if settings["autoRespon"] == True:
								client.sendMessage(to, "Auto respon telah aktif")
							else:
								settings["autoRespon"] = True
								client.sendMessage(to, "Berhasil mengaktifkan auto respon")
						elif cmd == "autrespon off":
							if settings["autoRespon"] == False:
								client.sendMessage(to, "Auto respon telah nonaktif")
							else:
								settings["autoRespon"] = False
								client.sendMessage(to, "Berhasil menonaktifkan auto respon")
						elif cmd == "contact on":
							if settings["checkContact"] == True:
								client.sendMessage(to, "Check details contact telah aktif")
							else:
								settings["checkContact"] = True
								client.sendMessage(to, "Berhasil mengaktifkan check details contact")
						elif cmd == "contact off":
							if settings["checkContact"] == False:
								client.sendMessage(to, "Check details contact telah nonaktif")
							else:
								settings["checkContact"] = False
								client.sendMessage(to, "Berhasil menonaktifkan Check details contact")
						elif cmd == "post on":
							if settings["checkPost"] == True:
								client.sendMessage(to, "Check details post telah aktif")
							else:
								settings["checkPost"] = True
								client.sendMessage(to, "Berhasil mengaktifkan check details post")
						elif cmd == "post off":
							if settings["checkPost"] == False:
								client.sendMessage(to, "Check details post telah nonaktif")
							else:
								settings["checkPost"] = False
								client.sendMessage(to, "Berhasil menonaktifkan check details post")
						elif cmd == "sticker on":
							if settings["checkSticker"] == True:
								client.sendMessage(to, "Check details sticker telah aktif")
							else:
								settings["checkSticker"] = True
								client.sendMessage(to, "Berhasil mengaktifkan check details sticker")
						elif cmd == "sticker off":
							if settings["checkSticker"] == False:
								client.sendMessage(to, "Check details sticker telah nonaktif")
							else:
								settings["checkSticker"] = False
								client.sendMessage(to, "Berhasil menonaktifkan check details sticker")
						elif cmd == "unsend on":
							if settings["detectUnsend"] == True:
								client.sendMessage(to, "Detect unsend is already on u bish")
							else:
								settings["detectUnsend"] = True
								client.sendMessage(to, "detect unsend is on, time to be snake")
						elif cmd == "unsend off":
							if settings["detectUnsend"] == False:
								client.sendMessage(to, "Detect unsend is already dead, stop trying")
							else:
								settings["detectUnsend"] = False
								client.sendMessage(to, "detect unsend is off, the snake has lost")
						elif cmd.startswith("setadd: "):
							sep = text.split(" ")
							txt = text.replace(sep[0] + " ","")
							try:
								settings["autoAddMessage"] = txt
								client.sendMessage(to, "Berhasil mengubah pesan auto add menjadi : 「{}」".format(txt))
							except:
								client.sendMessage(to, "Gagal mengubah pesan auto add")
						elif cmd.startswith("setrespon: "):
							sep = text.split(" ")
							txt = text.replace(sep[0] + " ","")
							try:
								settings["autoResponMessage"] = txt
								client.sendMessage(to, "Berhasil mengubah pesan auto respon menjadi : 「{}」".format(txt))
							except:
								client.sendMessage(to, "Gagal mengubah pesan auto respon")
						elif cmd.startswith("setjoin: "):
							sep = text.split(" ")
							txt = text.replace(sep[0] + " ","")
							try:
								settings["autoJoinMessage"] = txt
								client.sendMessage(to, "Berhasil mengubah pesan auto join menjadi : 「{}」".format(txt))
							except:
								client.sendMessage(to, "Gagal mengubah pesan auto join")
						elif cmd.startswith("changename: "):
							sep = text.split(" ")
							name = text.replace(sep[0] + " ","")
							if len(name) <= 20:
								profile = client.getProfile()
								profile.displayName = name
								client.updateProfile(profile)
								client.sendMessage(to, "Berhasil mengubah nama menjadi : {}".format(name))
						elif cmd.startswith("changebio: "):
							sep = text.split(" ")
							bio = text.replace(sep[0] + " ","")
							if len(bio) <= 500:
								profile = client.getProfile()
								profile.displayName = bio
								client.updateProfile(profile)
								client.sendMessage(to, "Berhasil mengubah bio menjadi : {}".format(bio))
						elif cmd == "me":
							client.sendMention(to, "@!", [sender])
							client.sendContact(to, sender)
						elif cmd == "myprofile":
							contact = client.getContact(sender)
							cover = client.getProfileCoverURL(sender)
							result = "╔════➢ Details Profile "
							result += "\n╠ Display Name : @!"
							result += "\n╠ Mid : {}".format(contact.mid)
							result += "\n╠ Status Message : {}".format(contact.statusMessage)
							result += "\n╠ Picture Profile : http://dl.profile.line-cdn.net/{}".format(contact.pictureStatus)
							result += "\n╠ Cover : {}".format(str(cover))
							result += "\n╚════➢ Finish ]"
							client.sendImageWithURL(to, "http://dl.profile.line-cdn.net/{}".format(contact.pictureStatus))
							client.sendMention(to, result, [sender])
						elif cmd == "mymid":
							contact = client.getContact(sender)
							client.sendMention(to, "@!: {}".format(contact.mid), [sender])
						elif cmd == "myname":
							contact = client.getContact(sender)
							client.sendMention(to, "@!: {}".format(contact.displayName), [sender])
						elif cmd == "mybio":
							contact = client.getContact(sender)
							client.sendMention(to, "@!: {}".format(contact.statusMessage), [sender])
						elif cmd == "mypict":
							contact = client.getContact(sender)
							client.sendImageWithURL(to, "http://dl.profile.line-cdn.net/{}".format(contact.pictureStatus))
						elif cmd == "myvid":
							contact = client.getContact(sender)
							if contact.videoProfile == None:
								return client.sendMessage(to, "Anda tidak memiliki video profile")
							client.sendVideoWithURL(to, "http://dl.profile.line-cdn.net/{}/vp".format(contact.pictureStatus))
						elif cmd == "mycover":
							cover = client.getProfileCoverURL(sender)
							client.sendImageWithURL(to, str(cover))
						elif cmd.startswith("mid "):
							if 'MENTION' in msg.contentMetadata.keys()!= None:
								names = re.findall(r'@(\w+)', text)
								mention = ast.literal_eval(msg.contentMetadata['MENTION'])
								mentionees = mention['MENTIONEES']
								lists = []
								for mention in mentionees:
									if mention["M"] not in lists:
										lists.append(mention["M"])
								for ls in lists:
									client.sendMention(to, "@!: {}".format(ls), [ls])
						elif cmd.startswith("name "):
							if 'MENTION' in msg.contentMetadata.keys()!= None:
								names = re.findall(r'@(\w+)', text)
								mention = ast.literal_eval(msg.contentMetadata['MENTION'])
								mentionees = mention['MENTIONEES']
								lists = []
								for mention in mentionees:
									if mention["M"] not in lists:
										lists.append(mention["M"])
								for ls in lists:
									contact = client.getContact(ls)
									client.sendMention(to, "@!: {}".format(contact.displayName), [ls])
						elif cmd.startswith("bio "):
							if 'MENTION' in msg.contentMetadata.keys()!= None:
								names = re.findall(r'@(\w+)', text)
								mention = ast.literal_eval(msg.contentMetadata['MENTION'])
								mentionees = mention['MENTIONEES']
								lists = []
								for mention in mentionees:
									if mention["M"] not in lists:
										lists.append(mention["M"])
								for ls in lists:
									contact = client.getContact(ls)
									client.sendMention(to, "@!: {}".format(contact.statusMessage), [ls])
						elif cmd.startswith("pict "):
							if 'MENTION' in msg.contentMetadata.keys()!= None:
								names = re.findall(r'@(\w+)', text)
								mention = ast.literal_eval(msg.contentMetadata['MENTION'])
								mentionees = mention['MENTIONEES']
								lists = []
								for mention in mentionees:
									if mention["M"] not in lists:
										lists.append(mention["M"])
								for ls in lists:
									contact = client.getContact(ls)
									client.sendImageWithURL(to, "http://dl.profile.line-cdn.net/{}".format(contact.pictureStatus))
						elif cmd.startswith("vid "):
							if 'MENTION' in msg.contentMetadata.keys()!= None:
								names = re.findall(r'@(\w+)', text)
								mention = ast.literal_eval(msg.contentMetadata['MENTION'])
								mentionees = mention['MENTIONEES']
								lists = []
								for mention in mentionees:
									if mention["M"] not in lists:
										lists.append(mention["M"])
								for ls in lists:
									contact = client.getContact(ls)
									if contact.videoProfile == None:
										return client.sendMention(to, "@!tidak memiliki video profile", [ls])
									client.sendVideoWithURL(to, "http://dl.profile.line-cdn.net/{}/vp".format(contact.pictureStatus))
						elif cmd.startswith("cover "):
							if 'MENTION' in msg.contentMetadata.keys()!= None:
								names = re.findall(r'@(\w+)', text)
								mention = ast.literal_eval(msg.contentMetadata['MENTION'])
								mentionees = mention['MENTIONEES']
								lists = []
								for mention in mentionees:
									if mention["M"] not in lists:
										lists.append(mention["M"])
								for ls in lists:
									cover = client.getProfileCoverURL(ls)
									client.sendImageWithURL(to, str(cover))
						elif cmd.startswith("clone "):
							if 'MENTION' in msg.contentMetadata.keys()!= None:
								names = re.findall(r'@(\w+)', text)
								mention = ast.literal_eval(msg.contentMetadata['MENTION'])
								mentionees = mention['MENTIONEES']
								lists = []
								for mention in mentionees:
									if mention["M"] not in lists:
										lists.append(mention["M"])
								for ls in lists:
									client.cloneContactProfile(ls)
									client.sendContact(to, sender)
									client.sendMessage(to, "Berhasil clone profile")
						elif cmd == "restore":
							try:
								clientProfile = client.getProfile()
								clientProfile.displayName = str(settings["myProfile"]["displayName"])
								clientProfile.statusMessage = str(settings["myProfile"]["statusMessage"])
								clientPictureStatus = client.downloadFileURL("http://dl.profile.line-cdn.net/{}".format(str(settings["myProfile"]["pictureStatus"])), saveAs="LineAPI/tmp/backupPicture.bin")
								coverId = str(settings["myProfile"]["coverId"])
								client.updateProfile(clientProfile)
								client.updateProfileCoverById(coverId)
								client.updateProfilePicture(clientPictureStatus)
								client.sendMessage(to, "Berhasil restore profile")
								client.sendContact(to, sender)
								client.deleteFile(clientPictureStatus)
							except Exception as error:
								logError(error)
								client.sendMessage(to, "Gagal restore profile")
						elif cmd == "backup":
							try:
								clientProfile = client.getProfile()
								settings["myProfile"]["displayName"] = str(clientProfile.displayName)
								settings["myProfile"]["statusMessage"] = str(clientProfile.statusMessage)
								settings["myProfile"]["pictureStatus"] = str(clientProfile.pictureStatus)
								coverId = client.getProfileDetail()["result"]["objectId"]
								settings["myProfile"]["coverId"] = str(coverId)
								client.sendMessage(to, "Berhasil backup profile")
							except Exception as error:
								logError(error)
								client.sendMessage(to, "Gagal backup profile")
						elif cmd == "friendlist":
							contacts = client.getAllContactIds()
							num = 0
							result = "╔════➢ Friend List "
							for listContact in contacts:
								contact = client.getContact(listContact)
								num += 1
								result += "\n╠ {}. {}".format(num, contact.displayName)
							result += "\n╚════➢ Total {} Friend ".format(len(contacts))
							client.sendMessage(to, result)
						elif cmd.startswith("friendinfo "):
							sep = text.split(" ")
							query = text.replace(sep[0] + " ","")
							contacts = client.getAllContactIds()
							try:
								listContact = contacts[int(query)-1]
								contact = client.getContact(listContact)
								cover = client.getProfileCoverURL(listContact)
								result = "╔════➢ Details Profile "
								result += "\n╠ Display Name : @!"
								result += "\n╠ Mid : {}".format(contact.mid)
								result += "\n╠ Status Message : {}".format(contact.statusMessage)
								result += "\n╠ Picture Profile : http://dl.profile.line-cdn.net/{}".format(contact.pictureStatus)
								result += "\n╠ Cover : {}".format(str(cover))
								result += "\n╚════➢ Finish "
								client.sendImageWithURL(to, "http://dl.profile.line-cdn.net/{}".format(contact.pictureStatus))
								client.sendMention(to, result, [contact.mid])
							except Exception as error:
								logError(error)
						elif cmd == "bklist":
							blockeds = client.getBlockedContactIds()
							num = 0
							result = "╔════➢ List Blocked "
							for listBlocked in blockeds:
								contact = client.getContact(listBlocked)
								num += 1
								result += "\n╠ {}. {}".format(num, contact.displayName)
							result += "\n╚════➢ Total {} Blocked ".format(len(blockeds))
							client.sendMessage(to, result)
						elif cmd.startswith("friendbc: "):
							sep = text.split(" ")
							txt = text.replace(sep[0] + " ","")
							contacts = client.getAllContactIds()
							for contact in contacts:
								client.sendMessage(contact, "[ Broadcast ]\n{}".format(str(txt)))
							client.sendMessage(to, "Berhasil broadcast ke {} teman".format(str(len(contacts))))


						elif cmd.startswith("changegname: "):
							if msg.toType == 2:
								sep = text.split(" ")
								groupname = text.replace(sep[0] + " ","")
								if len(groupname) <= 20:
									group = client.getGroup(to)
									group.name = groupname
									client.updateGroup(group)
									client.sendMessage(to, "Berhasil mengubah nama group menjadi : {}".format(groupname))
						elif cmd == "openqr":
							if msg.toType == 2:
								group = client.getGroup(to)
								group.preventedJoinByTicket = False
								client.updateGroup(group)
								groupUrl = client.reissueGroupTicket(to)
								client.sendMessage(to, "Berhasil membuka QR Group\n\nGroupURL : line://ti/g/{}".format(groupUrl))
						elif cmd == "closeqr":
							if msg.toType == 2:
								group = client.getGroup(to)
								group.preventedJoinByTicket = True
								client.updateGroup(group)
								client.sendMessage(to, "Berhasil menutup QR Group")
						elif cmd == "gpict":
							if msg.toType == 2:
								group = client.getGroup(to)
								groupPicture = "http://dl.profile.line-cdn.net/{}".format(group.pictureStatus)
								client.sendImageWithURL(to, groupPicture)
						elif cmd == "gname":
							if msg.toType == 2:
								group = client.getGroup(to)
								client.sendMessage(to, "Nama Group : {}".format(group.name))
						elif cmd == "gid":
							if msg.toType == 2:
								group = client.getGroup(to)
								client.sendMessage(to, "Group ID : {}".format(group.id))
						elif cmd == "glist":
							groups = client.getGroupIdsJoined()
							ret_ = "╔════➢ Group List "
							no = 0
							for gid in groups:
								group = client.getGroup(gid)
								no += 1
								ret_ += "\n╠ {}. {} | {}".format(str(no), str(group.name), str(len(group.members)))
							ret_ += "\n╚════➢ Total {} Groups ".format(str(len(groups)))
							client.sendMessage(to, str(ret_))
						elif cmd == "memlist":
							if msg.toType == 2:
								group = client.getGroup(to)
								num = 0
								ret_ = "╔════➢ List Member "
								for contact in group.members:
									num += 1
									ret_ += "\n╠ {}. {}".format(num, contact.displayName)
								ret_ += "\n╚════➢ Total {} Members".format(len(group.members))
								client.sendMessage(to, ret_)
						elif cmd == "pendinglist":
							if msg.toType == 2:
								group = client.getGroup(to)
								ret_ = "╔════➢ Pending List "
								no = 0
								if group.invitee is None or group.invitee == []:
									return client.sendMessage(to, "Tidak ada pendingan")
								else:
									for pending in group.invitee:
										no += 1
										ret_ += "\n╠ {}. {}".format(str(no), str(pending.displayName))
									ret_ += "\n╚════➢ Total {} Pending".format(str(len(group.invitee)))
									client.sendMessage(to, str(ret_))
						elif cmd == "ginfo":
							group = client.getGroup(to)
							try:
								try:
									groupCreator = group.creator.mid
								except:
									groupCreator = "Tidak ditemukan"
								if group.invitee is None:
									groupPending = "0"
								else:
									groupPending = str(len(group.invitee))
								if group.preventedJoinByTicket == True:
									groupQr = "Tertutup"
									groupTicket = "Tidak ada"
								else:
									groupQr = "Terbuka"
									groupTicket = "https://line.me/R/ti/g/{}".format(str(client.reissueGroupTicket(group.id)))
								ret_ = "╔════➢ Group Information "
								ret_ += "\n╠ Nama Group : {}".format(group.name)
								ret_ += "\n╠ ID Group : {}".format(group.id)
								ret_ += "\n╠ Pembuat : @!"
								ret_ += "\n╠ Jumlah Member : {}".format(str(len(group.members)))
								ret_ += "\n╠ Jumlah Pending : {}".format(groupPending)
								ret_ += "\n╠ Group Qr : {}".format(groupQr)
								ret_ += "\n╠ Group Ticket : {}".format(groupTicket)
								ret_ += "\n╚════➢ Success "
								client.sendImageWithURL(to, "http://dl.profile.line-cdn.net/{}".format(group.pictureStatus))
								client.sendMention(to, str(ret_), [groupCreator])
							except:
								ret_ = "╔════➢ Group Information "
								ret_ += "\n╠ Nama Group : {}".format(group.name)
								ret_ += "\n╠ ID Group : {}".format(group.id)
								ret_ += "\n╠ Pembuat : {}".format(groupCreator)
								ret_ += "\n╠ Jumlah Member : {}".format(str(len(group.members)))
								ret_ += "\n╠ Jumlah Pending : {}".format(groupPending)
								ret_ += "\n╠ Group Qr : {}".format(groupQr)
								ret_ += "\n╠ Group Ticket : {}".format(groupTicket)
								ret_ += "\n╚════➢ Success "
								client.sendImageWithURL(to, "http://dl.profile.line-cdn.net/{}".format(group.pictureStatus))
								client.sendMessage(to, str(ret_))
						elif cmd.startswith("groupbc: "):
							sep = text.split(" ")
							txt = text.replace(sep[0] + " ","")
							groups = client.getGroupIdsJoined()
							for group in groups:
								client.sendMessage(group, "[ Broadcast ]\n{}".format(str(txt)))
							client.sendMessage(to, "Berhasil broadcast ke {} group".format(str(len(groups))))

						elif cmd.startswith("unsend "):
							sep = text.split(" ")
							args = text.replace(sep[0] + " ","")
							mes = int(sep[1])
							#try:
								#mes = int(args[1])
							#except:
								#mes = 1
							M = client.getRecentMessagesV2(to, 1001)
							MId = []
							for ind,i in enumerate(M):
								if ind == 0:
									pass
								else:
									if i._from == client.profile.mid:
										MId.append(i.id)
										if len(MId) == mes:
											break
							def unsMes(id):
								client.unsendMessage(id)
							for i in MId:
								thread1 = threading.Thread(target=unsMes, args=(i,))
								thread1.daemon = True
								thread1.start()
								thread1.join()
							client.sendMessage(to, "「UNSEND」\nSuccess unsend {} message.".format(len(MId)))
						elif cmd == "delmentionme":
								del tagme['ROM'][to]
								client.sendMessage(to, "「DEL MENTIONME」\nBerhasil menghapus data Mention di group \n{}".format(client.getGroup(to).name))
						elif cmd == "mentionme":
								if to in tagme['ROM']:
									moneys = {}
									msgas = ''
									for a in tagme['ROM'][to].items():
										moneys[a[0]] = [a[1]['msg.id'],a[1]['waktu']] if a[1] is not None else idnya
									sort = sorted(moneys)
									sort.reverse()
									sort = sort[0:]
									msgas = '[Mention Me]'
									h = []
									no = 0
									for m in sort:
										has = ''
										nol = -1
										for kucing in moneys[m][0]:
											nol+=1
											has+= '\nline://nv/chatMsg?chatId={}&messageId={} \n{}'.format(to,kucing,humanize.naturaltime(datetime.fromtimestamp(moneys[m][1][nol]/1000)))
										h.append(m)
										no+=1
										if m == sort[0]:
											msgas+= '\n{}. @!{}x{}'.format(no,len(moneys[m][0]),has)
										else:
											msgas+= '\n\n{}. @!{}x{}'.format(no,len(moneys[m][0]),has)
									client.sendMention(to, msgas, h)
								else:
									msgas = 'Sorry @!In {} nothink get a mention'.format(client.getGroup(to).name)
									client.sendMention(to, msgas, [sender])
						elif cmd == 'mentionall':
							group = client.getGroup(to)
							midMembers = [contact.mid for contact in group.members]
							midSelect = len(midMembers)//20
							for mentionMembers in range(midSelect+1):
								no = 0
								ret_ = "╔════➢ Mention Members"
								dataMid = []
								for dataMention in group.members[mentionMembers*20 : (mentionMembers+1)*20]:
									dataMid.append(dataMention.mid)
									no += 1
									ret_ += "\n╠ {}. @!".format(str(no))
								ret_ += "\n╚════➢ Target {} ᴀʜʟɪ ᴋᴜʙᴜʀ".format(str(len(dataMid)))
								client.sendMention(to, ret_, dataMid)
								client.sendMessage(to, "Total {} ᴄᴀʟᴏɴ ᴀʟᴍᴀʀʜᴜᴍ".format(str(len(midMembers))))
						elif cmd == "lurk on":
							tz = pytz.timezone("Asia/Jakarta")
							timeNow = datetime.now(tz=tz)
							day = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday","Friday", "Saturday"]
							hari = ["Minggu", "Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"]
							bulan = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
							hr = timeNow.strftime("%A")
							bln = timeNow.strftime("%m")
							for i in range(len(day)):
								if hr == day[i]: hasil = hari[i]
							for k in range(0, len(bulan)):
								if bln == str(k): bln = bulan[k-1]
							readTime = hasil + ", " + timeNow.strftime('%d') + " - " + bln + " - " + timeNow.strftime('%Y') + "\nJam : [ " + timeNow.strftime('%H:%M:%S') + " ]"
							if to in read['readPoint']:
								try:
									del read['readPoint'][to]
									del read['readMember'][to]
								except:
									pass
								read['readPoint'][to] = msg_id
								read['readMember'][to] = []
								client.sendMessage(to, "Lurking telah diaktifkan")
							else:
								try:
									del read['readPoint'][to]
									del read['readMember'][to]
								except:
									pass
								read['readPoint'][to] = msg_id
								read['readMember'][to] = []
								client.sendMessage(to, "Set reading point : \n{}".format(readTime))
						elif cmd == "lurk off":
							tz = pytz.timezone("Asia/Jakarta")
							timeNow = datetime.now(tz=tz)
							day = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday","Friday", "Saturday"]
							hari = ["Minggu", "Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"]
							bulan = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
							hr = timeNow.strftime("%A")
							bln = timeNow.strftime("%m")
							for i in range(len(day)):
								if hr == day[i]: hasil = hari[i]
							for k in range(0, len(bulan)):
								if bln == str(k): bln = bulan[k-1]
							readTime = hasil + ", " + timeNow.strftime('%d') + " - " + bln + " - " + timeNow.strftime('%Y') + "\nJam : [ " + timeNow.strftime('%H:%M:%S') + " ]"
							if to not in read['readPoint']:
								client.sendMessage(to,"Lurking telah dinonaktifkan")
							else:
								try:
									del read['readPoint'][to]
									del read['readMember'][to]
								except:
									pass
								client.sendMessage(to, "Delete reading point : \n{}".format(readTime))
						elif cmd == "lurking":
							if to in read['readPoint']:
								if read["readMember"][to] == []:
									return client.sendMessage(to, "Tidak Ada Sider")
								else:
									no = 0
									result = "╔════➢ Reader "
									for dataRead in read["readMember"][to]:
										no += 1
										result += "\n╠ {}. @!".format(str(no))
									result += "\n╚════➢ Total {} Sider ".format(str(len(read["readMember"][to])))
									client.sendMention(to, result, read["readMember"][to])
									read['readMember'][to] = []
						elif cmd == "changepict":
							settings["changePictureProfile"] = True
							client.sendMessage(to, "Silahkan kirim gambarnya")
						elif cmd == "changegpict":
							if msg.toType == 2:
								if to not in settings["changeGroupPicture"]:
									settings["changeGroupPicture"].append(to)
								client.sendMessage(to, "Silahkan kirim gambarnya")
						elif cmd == "mimic on":
							if settings["mimic"]["status"] == True:
								client.sendMessage(to, "Reply message telah aktif")
							else:
								settings["mimic"]["status"] = True
								client.sendMessage(to, "Berhasil mengaktifkan reply message")
						elif cmd == "mimic off":
							if settings["mimic"]["status"] == False:
								client.sendMessage(to, "Reply message telah nonaktif")
							else:
								settings["mimic"]["status"] = False
								client.sendMessage(to, "Berhasil menonaktifkan reply message")
						elif cmd == "miclist":
							if settings["mimic"]["target"] == {}:
								client.sendMessage(to, "Tidak Ada Target")
							else:
								no = 0
								result = "╔════➢ Mimic List "
								target = []
								for mid in settings["mimic"]["target"]:
									target.append(mid)
									no += 1
									result += "\n╠ {}. @!".format(no)
								result += "\n╚════➢ Total {} Mimic ".format(str(len(target)))
								client.sendMention(to, result, target)
						elif cmd.startswith("micadd "):
							if 'MENTION' in msg.contentMetadata.keys()!= None:
								names = re.findall(r'@(\w+)', text)
								mention = ast.literal_eval(msg.contentMetadata['MENTION'])
								mentionees = mention['MENTIONEES']
								lists = []
								for mention in mentionees:
									if mention["M"] not in lists:
										lists.append(mention["M"])
								for ls in lists:
									try:
										if ls in settings["mimic"]["target"]:
											client.sendMessage(to, "Target sudah ada dalam list")
										else:
											settings["mimic"]["target"][ls] = True
											client.sendMessage(to, "Berhasil menambahkan target")
									except:
										client.sendMessage(to, "Gagal menambahkan target")
						elif cmd.startswith("micdel "):
							if 'MENTION' in msg.contentMetadata.keys()!= None:
								names = re.findall(r'@(\w+)', text)
								mention = ast.literal_eval(msg.contentMetadata['MENTION'])
								mentionees = mention['MENTIONEES']
								lists = []
								for mention in mentionees:
									if mention["M"] not in lists:
										lists.append(mention["M"])
								for ls in lists:
									try:
										if ls not in settings["mimic"]["target"]:
											client.sendMessage(to, "Target sudah tida didalam list")
										else:
											del settings["mimic"]["target"][ls]
											client.sendMessage(to, "Berhasil menghapus target")
									except:
										client.sendMessage(to, "Gagal menghapus target")


						elif cmd.startswith("instainfo"):
							sep = text.split(" ")
							txt = text.replace(sep[0] + " ","")
							url = requests.get("http://rahandiapi.herokuapp.com/instainfo/{}?key=betakey".format(txt))
							data = url.json()
							icon = "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a5/Instagram_icon.png/599px-Instagram_icon.png"
							name = "Instagram"
							link = "https://www.instagram.com/{}".format(data["result"]["username"])
							result = "╔════➢ Instagram Info "
							result += "\n╠ Name : {}".format(data["result"]["name"])
							result += "\n╠ Username: {}".format(data["result"]["username"])
							result += "\n╠ Bio : {}".format(data["result"]["bio"])
							result += "\n╠ Follower : {}".format(data["result"]["follower"])
							result += "\n╠ Following : {}".format(data["result"]["following"])
							result += "\n╠ Private : {}".format(data["result"]["private"])
							result += "\n╠ Post : {}".format(data["result"]["mediacount"])
							result += "\n╚════➢ Finish "
							client.sendImageWithURL(to, data["result"]["url"])
							client.sendFooter(to, result, icon, name, link)
						elif cmd.startswith("instastory "):
							sep = text.split(" ")
							query = text.replace(sep[0] + " ","")
							cond = query.split("|")
							search = str(cond[0])
							if len(cond) == 2:
								url = requests.get("http://rahandiapi.herokuapp.com/instastory/{}?key=betakey".format(search))
								data = url.json()
								num = int(cond[1])
								if num <= len(data["url"]):
									search = data["url"][num - 1]
									if search["tipe"] == 1:
										client.sendImageWithURL(to, str(search["link"]))
									elif search["tipe"] == 2:
										client.sendVideoWithURL(to, str(search["link"]))
						elif cmd == "quotes":
							url = requests.get("https://botfamily.faith/api/quotes/?apikey=beta")
							data = url.json()
							result = "╔════➢ Quotes of Today"
							result += "\n╠ Author : {}".format(data["result"]["author"])
							result += "\n╠ Category : {}".format(data["result"]["category"])
							result += "\n╠ Quote : {}".format(data["result"]["quote"])
							result += "\n╚════➢ Finish "
							client.sendMessage(to, result)
						elif cmd.startswith("say-"):
							sep = text.split("-")
							sep = sep[1].split(" ")
							lang = sep[0]
							if settings["setKey"] == False:
								txt = text.lower().replace("say-" + lang + " ","")
							else:
								txt = text.lower().replace(settings["keyCommand"] + "say-" + lang + " ","")
							if lang not in language["gtts"]:
								return client.sendMessage(to, "Bahasa {} tidak ditemukan".format(lang))
							tts = gTTS(text=txt, lang=lang)
							tts.save("line/tmp/tts-{}.mp3".format(lang))
							client.sendAudio(to, "line/tmp/tts-{}.mp3".format(lang))
							client.deleteFile("line/tmp/tts-{}.mp3".format(lang))
						elif cmd.startswith("youtube "):
							sep = text.split(" ")
							txt = msg.text.replace(sep[0] + " ","")
							cond = txt.split("|")
							search = cond[0]
							url = requests.get("http://api.w3hills.com/youtube/search?keyword={}&api_key=86A7FCF3-6CAF-DEB9-E214-B74BDB835B5B".format(search))
							data = url.json()
							if len(cond) == 1:
								no = 0
								result = "╔════➢ Youtube Search "
								for anu in data["videos"]:
									no += 1
									result += "\n╠ {}. {}".format(str(no),str(anu["title"]))
								result += "\n╚════➢ Total {} Result ".format(str(len(data["videos"])))
								client.sendMessage(to, result)
							elif len(cond) == 2:
								num = int(str(cond[1]))
								if num <= len(data):
									search = data["videos"][num - 1]
									ret_ = "╔════➢ Youtube Info "
									ret_ += "\n╠ Channel : {}".format(str(search["publish"]["owner"]))
									ret_ += "\n╠ Title : {}".format(str(search["title"]))
									ret_ += "\n╠ Release : {}".format(str(search["publish"]["date"]))
									ret_ += "\n╠ Viewers : {}".format(str(search["stats"]["views"]))
									ret_ += "\n╠ Likes : {}".format(str(search["stats"]["likes"]))
									ret_ += "\n╠ Dislikes : {}".format(str(search["stats"]["dislikes"]))
									ret_ += "\n╠ Rating : {}".format(str(search["stats"]["rating"]))
									ret_ += "\n╠ Description : {}".format(str(search["description"]))
									ret_ += "\n╚════➢ {} ".format(str(search["webpage"]))
									client.sendImageWithURL(to, str(search["thumbnail"]))
									client.sendMessage(to, str(ret_))
						elif cmd.startswith("image "):
							sep = text.split(" ")
							txt = text.replace(sep[0] + " ","")
							url = requests.get("http://rahandiapi.herokuapp.com/imageapi?key=betakey&q={}".format(txt))
							data = url.json()
							client.sendImageWithURL(to, random.choice(data["result"]))
						elif cmd.startswith("music "):
							sep = text.split(" ")
							query = text.replace(sep[0] + " ","")
							cond = query.split("|")
							search = str(cond[0])
							url = requests.get("http://api.ntcorp.us/joox/search?q={}".format(str(search)))
							data = url.json()
							if len(cond) == 1:
								num = 0
								ret_ = "╔════➢ Result Music "
								for music in data["result"]:
									num += 1
									ret_ += "\n╠ {}. {}".format(str(num), str(music["single"]))
								ret_ += "\n╚════➢ Total {} Music ".format(str(len(data["result"])))
								ret_ += "\n\nUntuk mengirim music, silahkan gunakan command {}Music {}|「number」".format(str(setKey), str(search))
								client.sendMessage(to, str(ret_))
							elif len(cond) == 2:
								num = int(cond[1])
								if num <= len(data["result"]):
									music = data["result"][num - 1]
									url = requests.get("http://api.ntcorp.us/joox/song_info?sid={}".format(str(music["sid"])))
									data = url.json()
									ret_ = "╔════➢ Music "
									ret_ += "\n╠ Title : {}".format(str(data["result"]["song"]))
									ret_ += "\n╠ Album : {}".format(str(data["result"]["album"]))
									ret_ += "\n╠ Size : {}".format(str(data["result"]["size"]))
									ret_ += "\n╠ Link : {}".format(str(data["result"]["mp3"][0]))
									ret_ += "\n╚════➢ Finish "
									client.sendImageWithURL(to, str(data["result"]["img"]))
									client.sendMessage(to, str(ret_))
									client.sendAudioWithURL(to, str(data["result"]["mp3"][0]))
						elif cmd.startswith("lyric "):
							sep = text.split(" ")
							txt = text.replace(sep[0] + " ","")
							cond = txt.split("|")
							query = cond[0]
							with requests.session() as web:
								web.headers["user-agent"] = "Mozilla/5.0"
								url = web.get("https://www.musixmatch.com/search/{}".format(urllib.parse.quote(query)))
								data = BeautifulSoup(url.content, "html.parser")
								result = []
								for trackList in data.findAll("ul", {"class":"tracks list"}):
									for urlList in trackList.findAll("a"):
										title = urlList.text
										url = urlList["href"]
										result.append({"title": title, "url": url})
								if len(cond) == 1:
									ret_ = "╔════➢ Musixmatch Result "
									num = 0
									for title in result:
										num += 1
										ret_ += "\n╠ {}. {}".format(str(num), str(title["title"]))
									ret_ += "\n╚════➢ Total {} Lyric ".format(str(len(result)))
									ret_ += "\n\nUntuk melihat lyric, silahkan gunakan command {}Lyric {}|「number」".format(str(setKey), str(query))
									client.sendMessage(to, ret_)
								elif len(cond) == 2:
									num = int(cond[1])
									if num <= len(result):
										data = result[num - 1]
										with requests.session() as web:
											web.headers["user-agent"] = "Mozilla/5.0"
											url = web.get("https://www.musixmatch.com{}".format(urllib.parse.quote(data["url"])))
											data = BeautifulSoup(url.content, "html5lib")
											for lyricContent in data.findAll("p", {"class":"mxm-lyrics__content "}):
												lyric = lyricContent.text
									if text.lower() == "mykey":
							client.sendMessage(to, "Keycommand yang diset saat ini : 「{}」".format(str(settings["keyCommand"])))
						elif text.lower() == "setkey on":
							if settings["setKey"] == True:
								client.sendMessage(to, "Setkey telah aktif")
							else:
								settings["setKey"] = True
								client.sendMessage(to, "Berhasil mengaktifkan setkey")
						elif text.lower() == "setkey off":
							if settings["setKey"] == False:
								client.sendMessage(to, "Setkey telah nonaktif")
							else:
								settings["setKey"] = False
								client.sendMessage(to, "Berhasil menonaktifkan setkey")
						if text is None: return
						if "/ti/g/" in msg.text.lower():
							if settings["autoJoinTicket"] == True:
								link_re = re.compile('(?:line\:\/|line\.me\/R)\/ti\/g\/([a-zA-Z0-9_-]+)?')
								links = link_re.findall(text)
								n_links = []
								for l in links:
									if l not in n_links:
										n_links.append(l)
								for ticket_id in n_links:
									group = client.findGroupByTicket(ticket_id)
									client.acceptGroupInvitationByTicket(group.id,ticket_id)
									client.sendMessage(to, "Berhasil masuk ke group %s" % str(group.name))
				elif cmd.startswith('kick '):
			        if msg.toType != 2: return line.sendMessage(to, 'Failed kick member, use this command only on group chat')
			        if 'MENTION' in msg.contentMetadata.keys():
			            mentions = ast.literal_eval(msg.contentMetadata['MENTION'])
			            for mention in mentions['MENTIONEES']:
			                mid = mention['M']
			                if mid == myMid:
			                    continue
			                try:
			                    line.kickoutFromGroup(to, [mid])
			                except TalkException as talk_error:
			                    return line.sendMessage(to, 'Failed kick members, the reason is `%s`' % talk_error.reason)
			                time.sleep(0.8)
			            line.sendMessage(to, 'Success kick members, totals %i members' % len(mentions['MENTIONEES']))
			        else:
			            line.sendMessage(to, 'Failed kick member, please mention user you want to kick')
			    elif cmd.startswith('vkick '):
			        if msg.toType != 2: return line.sendMessage(to, 'Failed vultra kick member, use this command only on group chat')
			        if 'MENTION' in msg.contentMetadata.keys():
			            mentions = ast.literal_eval(msg.contentMetadata['MENTION'])
			            for mention in mentions['MENTIONEES']:
			                mid = mention['M']
			                if mid == myMid:
			                    continue
			                try:
			                    line.kickoutFromGroup(to, [mid])
			                    line.findAndAddContactsByMid(mid)
			                    line.inviteIntoGroup(to, [mid])
			                    line.cancelGroupInvitation(to, [mid])
			                except TalkException as talk_error:
			                    return line.sendMessage(to, 'Failed vultra kick members, the reason is `%s`' % talk_error.reason)
			                time.sleep(0.8)
			            line.sendMessage(to, 'Success vultra kick members, totals %i members' % len(mentions['MENTIONEES']))
			        else:
			            line.sendMessage(to, 'Failed vultra kick member, please mention user you want to kick')

					elif msg.contentType == 1:
						if settings["changePictureProfile"] == True:
							path = client.downloadObjectMsg(msg_id, saveAs="LineAPI/tmp/{}-cpp.bin".format(time.time()))
							settings["changePictureProfile"] = False
							client.updateProfilePicture(path)
							client.sendMessage(to, "Berhasil mengubah foto profile")
							client.deleteFile(path)
						if msg.toType == 2:
							if to in settings["changeGroupPicture"]:
								path = client.downloadObjectMsg(msg_id, saveAs="LineAPI/tmp/{}-cgp.bin".format(time.time()))
								settings["changeGroupPicture"].remove(to)
								client.updateGroupPicture(to, path)
								client.sendMessage(to, "Berhasil mengubah foto group")
								client.deleteFile(path)
					elif msg.contentType == 7:
						if settings["checkSticker"] == True:
							stk_id = msg.contentMetadata['STKID']
							stk_ver = msg.contentMetadata['STKVER']
							pkg_id = msg.contentMetadata['STKPKGID']
							ret_ = "╔════➢ Sticker Info "
							ret_ += "\n╠ STICKER ID : {}".format(stk_id)
							ret_ += "\n╠ STICKER PACKAGES ID : {}".format(pkg_id)
							ret_ += "\n╠ STICKER VERSION : {}".format(stk_ver)
							ret_ += "\n╠ STICKER URL : line://shop/detail/{}".format(pkg_id)
							ret_ += "\n╚════➢ Bentar Lagi ditarik "
							client.sendMessage(to, str(ret_))
					elif msg.contentType == 13:
						if settings["checkContact"] == True:
							try:
								contact = client.getContact(msg.contentMetadata["mid"])
								cover = client.getProfileCoverURL(msg.contentMetadata["mid"])
								ret_ = "╔════➢ Details Contact "
								ret_ += "\n╠ Nama : {}".format(str(contact.displayName))
								ret_ += "\n╠ MID : {}".format(str(msg.contentMetadata["mid"]))
								ret_ += "\n╠ Bio : {}".format(str(contact.statusMessage))
								ret_ += "\n╠ Gambar Profile : http://dl.profile.line-cdn.net/{}".format(str(contact.pictureStatus))
								ret_ += "\n╠ Gambar Cover : {}".format(str(cover))
								ret_ += "\n╚════➢ Bentar Lagi dibanned "
								client.sendImageWithURL(to, "http://dl.profile.line-cdn.net/{}".format(str(contact.pictureStatus)))
								client.sendMessage(to, str(ret_))
							except:
								client.sendMessage(to, "Kontak tidak valid")
					elif msg.contentType == 16:
						if settings["checkPost"] == True:
							try:
								ret_ = "╔════➢ Details Post "
								if msg.contentMetadata["serviceType"] == "GB":
									contact = client.getContact(sender)
									auth = "\n╠ Penulis : {}".format(str(contact.displayName))
								else:
									auth = "\n╠ Penulis : {}".format(str(msg.contentMetadata["serviceName"]))
								purl = "\n╠ URL : {}".format(str(msg.contentMetadata["postEndUrl"]).replace("line://","https://line.me/R/"))
								ret_ += auth
								ret_ += purl
								if "mediaOid" in msg.contentMetadata:
									object_ = msg.contentMetadata["mediaOid"].replace("svc=myhome|sid=h|","")
									if msg.contentMetadata["mediaType"] == "V":
										if msg.contentMetadata["serviceType"] == "GB":
											ourl = "\n╠ Objek URL : https://obs-us.line-apps.com/myhome/h/download.nhn?tid=612w&{}".format(str(msg.contentMetadata["mediaOid"]))
											murl = "\n╠ Media URL : https://obs-us.line-apps.com/myhome/h/download.nhn?{}".format(str(msg.contentMetadata["mediaOid"]))
										else:
											ourl = "\n╠ Objek URL : https://obs-us.line-apps.com/myhome/h/download.nhn?tid=612w&{}".format(str(object_))
											murl = "\n╠ Media URL : https://obs-us.line-apps.com/myhome/h/download.nhn?{}".format(str(object_))
										ret_ += murl
									else:
										if msg.contentMetadata["serviceType"] == "GB":
											ourl = "\n╠ Objek URL : https://obs-us.line-apps.com/myhome/h/download.nhn?tid=612w&{}".format(str(msg.contentMetadata["mediaOid"]))
										else:
											ourl = "\n╠ Objek URL : https://obs-us.line-apps.com/myhome/h/download.nhn?tid=612w&{}".format(str(object_))
									ret_ += ourl
								if "stickerId" in msg.contentMetadata:
									stck = "\n╠ Stiker : https://line.me/R/shop/detail/{}".format(str(msg.contentMetadata["packageId"]))
									ret_ += stck
								if "text" in msg.contentMetadata:
									text = "\n╠ Tulisan : {}".format(str(msg.contentMetadata["text"]))
									ret_ += text
								ret_ += "\n╚════➢ Bentar Lagi direport "
								client.sendMessage(to, str(ret_))
							except:
								client.sendMessage(to, "Post tidak valid")
			except Exception as error:
				logError(error)


		if op.type == 26:
			try:
				print("[ 26 ] RECEIVE MESSAGE")
				msg = op.message
				text = str(msg.text)
				msg_id = msg.id
				receiver = msg.to
				sender = msg._from
				if msg.toType == 0 or msg.toType == 1 or msg.toType == 2:
					if msg.toType == 0:
						if sender != client.profile.mid:
							to = sender
						else:
							to = receiver
					elif msg.toType == 1:
						to = receiver
					elif msg.toType == 2:
						to = receiver
					if sender in settings["mimic"]["target"] and settings["mimic"]["status"] == True and settings["mimic"]["target"][sender] == True:
						if msg.contentType == 0:
							client.sendMessage(to, text)
						elif msg.contentType == 1:
							path = client.downloadObjectMsg(msg_id, saveAs="LineAPI/tmp/{}-mimic.bin".format(time.time()))
							client.sendImage(to, path)
							client.deleteFile(path)
					if msg.contentType == 0:
						if settings["autoRead"] == True:
							client.sendChatChecked(to, msg_id)
						if sender not in clientMid:
							if msg.toType != 0 and msg.toType == 2:
								if 'MENTION' in msg.contentMetadata.keys()!= None:
									names = re.findall(r'@(\w+)', text)
									mention = ast.literal_eval(msg.contentMetadata['MENTION'])
									mentionees = mention['MENTIONEES']
									for mention in mentionees:
										if clientMid in mention["M"]:
											if settings["autoRespon"] == True:
												client.sendMention(sender, settings["autoResponMessage"], [sender])
											break

						if text is None: return
						if "/ti/g/" in msg.text.lower():
							if settings["autoJoinTicket"] == True:
								link_re = re.compile('(?:line\:\/|line\.me\/R)\/ti\/g\/([a-zA-Z0-9_-]+)?')
								links = link_re.findall(text)
								n_links = []
								for l in links:
									if l not in n_links:
										n_links.append(l)
								for ticket_id in n_links:
									group = client.findGroupByTicket(ticket_id)
									client.acceptGroupInvitationByTicket(group.id,ticket_id)
									client.sendMessage(to, "Berhasil masuk ke group %s" % str(group.name))
						if settings["detectUnsend"] == True:
							try:
								unsendTime = time.time()
								unsend[msg_id] = {"text": text, "from": sender, "time": unsendTime}
							except Exception as error:
								logError(error)
					if msg.contentType == 1:
						if settings["detectUnsend"] == True:
							try:
								unsendTime = time.time()
								image = client.downloadObjectMsg(msg_id, saveAs="LineAPI/tmp/{}-image.bin".format(time.time()))
								unsend[msg_id] = {"from": sender, "image": image, "time": unsendTime}
							except Exception as error:
								logError(error)
			except Exception as error:
				logError(error)


		if op.type == 55:
			print ("[ 55 ] NOTIFIED READ MESSAGE")
			if op.param1 in read["readPoint"]:
				if op.param2 not in read["readMember"][op.param1]:
					read["readMember"][op.param1].append(op.param2)


		if op.type == 65:
			try:
				if settings["detectUnsend"] == True:
					to = op.param1
					sender = op.param2
					if sender in unsend:
						unsendTime = time.time()
						contact = client.getContact(unsend[sender]["from"])
						if "text" in unsend[sender]:
							try:
								sendTime = unsendTime - unsend[sender]["time"]
								sendTime = timeChange(sendTime)
								ret_ = "╔════➢ Unsend Message "
								ret_ += "\n╠ Sender : @!"
								ret_ += "\n╠ Text : {}".format(unsend[sender]["text"])
								ret_ += "\n╚════➢"
								client.sendMention(to, ret_, [contact.mid])
								del unsend[sender]
							except:
								del unsend[sender]
						elif "image" in unsend[sender]:
							try:
								sendTime = unsendTime - unsend[sender]["time"]
								sendTime = timeChange(sendTime)
								ret_ = "╔════➢ Unsend Picture "
								ret_ += "\n╠ Sender : @!"
								ret_ += "\n╚════➢  "
								client.sendMention(to, ret_, [contact.mid])
								client.sendImage(to, unsend[sender]["image"])
								client.deleteFile(unsend[sender]["image"])
								del unsend[sender]
							except:
								client.deleteFile(unsend[sender]["image"])
								del unsend[sender]
					else:
						client.sendMessage(to, "")
			except Exception as error:
				logError(error)
		backupData()
	except Exception as error:
		logError(error)

def run():
	while True:
		ops = clientPoll.singleTrace(count=50)
		if ops != None:
			for op in ops:
				try:
					clientBot(op)
				except Exception as error:
					logError(error)
				clientPoll.setRevision(op.revision)

if __name__ == "__main__":
	run()
