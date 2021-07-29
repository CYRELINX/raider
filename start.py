import sys,time,requests
import vk_api,requests,traceback,glob,time,json,random
from vk_api.longpoll import VkLongPoll, VkEventType, VkChatEventType
from python3_anticaptcha import ImageToTextTask
from python3_anticaptcha import errors
from CONFIG import info
from threading import Thread

print("Start Bot")

def friends():
	while True:
		try:
			zayavki=requests.get("https://api.vk.com/method/friends.getRequests?access_token=%s" % info.token+"&v=5.92").json()['response']['items']
			requests.get("https://api.vk.com/method/friends.add?access_token=%s" % info.token+"&v=5.92&user_id="+str(random.choice(zayavki)))

			zayavki3=requests.get("https://api.vk.com/method/friends.getRequests?access_token=%s" % "a5ff77001a4f13938b58fb11a8eef6f7e90cd4c47a4350d2c23856ca06cf5c7436b2bf916c90ac8d1e777"+"&v=5.92").json()['response']['items']
			requests.get("https://api.vk.com/method/friends.add?access_token=%s" % "a5ff77001a4f13938b58fb11a8eef6f7e90cd4c47a4350d2c23856ca06cf5c7436b2bf916c90ac8d1e777"+"&v=5.92&user_id="+str(random.choice(zayavki)))
		except:
			pass
		try:
			zayavki1=requests.get("https://api.vk.com/method/friends.getRequests?access_token=%s" % info.token+"&out=true&v=5.92").json()['response']['items']
			requests.get("https://api.vk.com/method/friends.delete?access_token=%s" % info.token+"&v=5.92&user_id="+str(random.choice(zayavki1)))

			zayavki2=requests.get("https://api.vk.com/method/friends.getRequests?access_token=%s" % "a5ff77001a4f13938b58fb11a8eef6f7e90cd4c47a4350d2c23856ca06cf5c7436b2bf916c90ac8d1e777" +"&out=true&v=5.92").json()['response']['items']
			requests.get("https://api.vk.com/method/friends.delete?access_token=%s" % "a5ff77001a4f13938b58fb11a8eef6f7e90cd4c47a4350d2c23856ca06cf5c7436b2bf916c90ac8d1e777"+"&v=5.92&user_id="+str(random.choice(zayavki1)))
		except:
			pass
		time.sleep(10)

newThread = Thread(target=friends)
newThread.start()

file = open(info.msgs, 'r', encoding='utf-8')
phrases = file.readlines()
file.close()

file = open(info.name, 'r', encoding='utf-8')
names = file.readlines()
file.close()

photos = []

peers = []

def getPhotos(vk):
	infphoto = vk.photos.get(owner_id=info.idvk[0],album_id=280504769)["items"]
	for i in infphoto:
		photos.append("photo" + str(info.idvk[0]) + "_" + str(i["id"]))

def msgs(event,vk):
	peer_id = event.peer_id
	user_id = event.user_id

	b = event.text
	c = random.randint(1,2)

	for i in range(0, c):
		if event.text != '' and event.user_id > 0 and not event.from_me:
			try:
				if peer_id > 2000000000 and not peer_id - 2000000000 in info.conflist and not event.user_id in info.ignorelist and not event.user_id in info.idvk:
					time.sleep(random.randint(1, 2))
					msg = random.choice(phrases).rstrip()

					photo = ""
					if len(photos) != 0:
						photo = random.choice(photos).rstrip()

					name = random.choice(names).rstrip()
					vk.messages.setActivity(peer_id=peer_id, type='typing')
					time.sleep(random.randint(5, 10))
					vk.messages.send(peer_id=peer_id, random_id=random.randint(100000, 999999),
									 message=random.choice(["[id" + str(user_id) + "|" + name + "], " + msg, msg]),
									 attachment=random.choice([str(photo), '', '', '']))
				if peer_id < 2000000000 and user_id > 0:
					prefix = b[:5]
					if prefix == 'link ':
						link = b[5:]
						try:
							vk.messages.joinChatByInviteLink(link=link)
						except:
							pass
					else:
						time.sleep(random.randint(1, 2))
						msg = random.choice(phrases).rstrip()

						photo = ""
						if len(photos) != 0:
							photo = random.choice(photos).rstrip()

						vk.messages.setActivity(peer_id=peer_id, type='typing')
						time.sleep(random.randint(5, 10))
						vk.messages.send(peer_id=peer_id, random_id=random.randint(100000, 999999), message=msg,
										 attachment=random.choice([str(photo), '', '', '']))
			except:
				pass

	peers.remove(peer_id)

def bot():
	def captcha_handler(captcha):
		key = ImageToTextTask.ImageToTextTask(anticaptcha_key=info.captcha, save_format='const') \
				.captcha_handler(captcha_link=captcha.get_url())
		return captcha.try_again(key['solution']['text'])
	vk_session = vk_api.VkApi(token=info.token, captcha_handler=captcha_handler)

	vk = vk_session.get_api()

	if not photos:
		getPhotos(vk)
		pass

	selfid = info.ignorelist
	ignore = info.conflist

	while True:
		try:
			longpoll = VkLongPoll(vk_session)
			for event in longpoll.listen():
				if event.type_id == VkChatEventType.USER_JOINED:
					a=event.info['user_id']
					chat_id = event.chat_id
					peer_id = event.peer_id
					if int(a) in info.idvk:
						try:
							vk.messages.editChat(chat_id=chat_id,title=random.choice(info.titlel))
							j=vk.photos.getChatUploadServer(chat_id=chat_id,crop_x=10,crop_y=25)['upload_url']
							img = {'photo': (random.choice(info.photo), open(random.choice(info.photo), 'rb'))}
							response = requests.post(j, files=img)
							result = json.loads(response.text)['response']
							vk.messages.setChatPhoto(file=result)
						except:
							pass
						try:
							vk.messages.unpin(peer_id=peer_id)
						except:
							pass
						try:
							vk.messages.addChatUser(chat_id=chat_id)
						except:
							pass
				if event.type_id == VkChatEventType.MESSAGE_PINNED:
					peer_id=event.peer_id
					r=vk.messages.getConversationsById(peer_ids=peer_id)['items'][0]['last_message_id']
					f=vk.messages.getById(message_ids=r,preview_length='0')['items'][0]['from_id']
					if not int(f) in info.idvk and int(f) > 0:
						vk.messages.unpin(peer_id=peer_id)
				if event.type_id == VkChatEventType.PHOTO:
					chat_id = event.chat_id
					peer_id = event.peer_id
					r=vk.messages.getConversationsById(peer_ids=peer_id)['items'][0]['last_message_id']
					f=vk.messages.getById(message_ids=r,preview_length='0')['items'][0]['from_id']
					title=vk.messages.getChat(chat_id=chat_id)['title']
					if not int(f) in info.idvk and int(f) > 0 and not event.chat_id in info.conflist:
						a=vk.photos.getChatUploadServer(chat_id=event.chat_id,crop_x=10,crop_y=25)['upload_url']
						img = {'photo': (random.choice(info.photo), open(random.choice(info.photo), 'rb'))}
						response = requests.post(a, files=img)
						result = json.loads(response.text)['response']
						vk.messages.setChatPhoto(file=result)
				if event.type_id == VkChatEventType.TITLE:
					chat_id = event.chat_id
					peer_id = event.peer_id
					r=vk.messages.getConversationsById(peer_ids=peer_id)['items'][0]['last_message_id']
					f=vk.messages.getById(message_ids=r,preview_length='0')['items'][0]['from_id']
					if not int(f) in info.idvk and int(f) > 0 and not event.chat_id in info.conflist:
						vk.messages.editChat(chat_id=chat_id,title=random.choice(info.titlel))
				if event.type == VkEventType.MESSAGE_NEW:
					if event.peer_id not in peers:
						peers.append(event.peer_id)
						class message(Thread):
							def __init__(self, vk, event):
								Thread.__init__(self)
								self.vk = vk
								self.event = event

							def run(self):
								msgs(event, vk)

						my_thread1 = message(vk, event)
						my_thread1.start()
				if event.type_id == VkChatEventType.USER_KICKED:
					requests.get(
						"https://api.vk.com/method/messages.addChatUser?access_token=" + info.token + "&v=5.92&chat_id=" + str(
							event.chat_id) + "&user_id=" + str(event.info['user_id']))
		except Exception as e:
			print('Ошибка:\n', traceback.format_exc())
			pass

while True:
	try:
		bot()
	except:
		pass