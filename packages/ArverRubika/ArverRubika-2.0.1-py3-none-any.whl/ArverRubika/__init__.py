from random import randint
from ArverRubika.ArverMaker import makers
from colorama import Fore
import requests
import pyuseragents
__version__,__maker__,__channel__="1.0.0","Abolfazl Mirzai","@ArverTeam"
def text_flush(text):
	for txt in text:
		from time import sleep
		print(txt,end='',flush=True)
		sleep(0.035)
class ArverBot:
	def __init__(self,token):
		if len(token) > 32:
			raise IndexError("Auth is Not True .!")
		self.auth = token
		self.method = makers(token).method
	def send_message(self,guid,text,message_id=None):
		date={
            'object_guid': guid,
            'rnd': str(randint(10000000, 999999999)),
            'text': text,
            'reply_to_message_id': message_id,
        }
		return self.method('sendMessage',date)
	def get_info_username(self,username):
		date={
		'username' : username,
		}
		return self.method('getObjectByUsername',date)
	def forward_message(self,from_guid,message_ids,to_guid):
		date={
		'from_object_guid': from_guid,
		'message_ids': message_ids,
		'rnd': str(randint(10000000, 999999999)),
		'to_object_guid': to_guid
		}
		return self.method('forwardMessages',date)
	def get_chats(self,start_id=None):
		date={
		'start_id':start_id
		}
		return self.method('getChats',date)
	def online(self):
		headers = {'accept': 'application/json, text/plain, */*', 'accept-encoding': 'gzip, deflate, br', 'accept-language': 'en-US,en;q=0.9', 'content-length': '338', 'content-type': 'text/plain', 'origin': 'https://web.rubika.ir', 'referer': 'https://web.rubika.ir/', 'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="104"' , 'sec-ch-ua-mobile': '?0', 'sec-ch-ua-platform': '"Linux"', 'sec-fetch-dest': 'empty', 'sec-fetch-mode': 'cors', 'sec-fetch-site': 'cross-site', 'user-agent': pyuseragents.random()}
		send = requests.post(json={"data":{},"method":"getUser","api_version":"2","auth":self.auth,"Messenger":{"app_name":"Main","package":"m.rubika.ir","app_version":"1.2.1","platform":"PWA"}},url='https://messengerg2c1.iranlms.ir/', headers=headers).json()
		if send["status_det"] == "OK":
			return True
		else:
			return False
	def get_url_info(self,url):
		date={
		"app_url":url
		}
		return self.method("getLinkFromAppUrl",date)
	def get_messages_info(self,guid,message_ids):
		date={
		"object_guid":guid,
		"message_ids":message_ids
		}
		return self.method("getMessagesByID",date)
	def get_messages(self, guid, middle_message_id):
		date={
        "object_guid":guid,
        "middle_message_id":middle_message_id
        }
		return self.method("getMessagesInterval",date)
	def get_last_messages(self,guid,min_id):
		date={
        "object_guid": guid,
        "sort":"FromMin",
        "min_id": min_id
            }
		return self.method("getMessages",date)
	def join_group(self,link):
		date={
		"hash_link":link.split("/")[-1]
		}
		return self.method("joinGroup",date)
	def leave_group(self,guid):
		date={
		"group_guid":guid
		}
		return self.method("leaveGroup",date)
	def get_chat_info(self,guid):
	       if guid.startswith('u'): data = 'User'
	       elif guid.startswith('g'): data = 'Group'
	       elif guid.startswith('c'): data = 'Channel'
	       elif guid.startswith('b'): data = 'Bot'
	       elif guid.startswith('s'): data = 'Service'
	       else: raise KeyError("is not guid true .!")
	       return self.method("get"+data+"Info",{data.lower()+"_guid":guid})
	def get_chat_messages(self,guid):
	     date=self.get_chat_info(guid)["data"]["chat"]["last_message_id"]
	     return self.get_messages(guid,date)