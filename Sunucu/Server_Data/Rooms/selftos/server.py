#    [PROGRAM]
#
# Selftos Server by therenaydin.
# Windows 10 ve Linux ile test edildi. Diğer windows sürümleri veya işletim sistemleri ile düzgün çalışmayabilir!
# Gerekli kütüphaneleri pip ile indirmeniz gerekmektedir. Yoksa program başlamaz.
# SSH sunucusunda screen komutu ile çalıştırmanızı öneririz. Aksi taktirde ssh sunucusu ile olan bağlantıyı kestiğiniz anda sunucu kapanır.
# Detaylı bilgi: https://www.fullstackpython.com/screen.html
# 175. satırda kendi sunucunuzun IP adresini yazmayı unutmayın.
# PORT numarasını port.txt adlı dosyadan alır buraya ekleme yapmanıza gerek yok.
#
#    [YAPIMCI]
#
# Eren Aydın ~ therenaydin
# E-posta: therenaydin@gmail.com
# Discord: therenaydin#0911
#
#    [LISANS]
#
# Bu program ücretsizdir.
# İnsanların üzerinde değişiklik yapması ve kendini geliştirmesi için topluluk ile paylaşılmıştır.
# Programı düzenleyip paylaşabilirsiniz.
# Ödevlerinizde kullanabilirsiniz.
#
#    [KAYNAKÇA]
#
# https://www.neuralnine.com/
# https://python-forum.io/
# https://www.youtube.com/channel/UC8wZnXYK_CGKlBcZp-GxYPA (NeuralNine)
# https://pythonprogramming.net/
# https://www.youtube.com/user/sentdex
# https://www.youtube.com/channel/UCi8b7ab1pEJ40hz4E_PDROQ (Melih Görgülü)
# https://stackoverflow.com/

import socket
from threading import Thread
import time
import sys
from colorama import Fore, Back, Style, init

init(autoreset=True)

def accept_incoming_connections(): # Gelen bağlantıları kabul eder.
	while True:
		client, client_address = SERVER.accept()
		print("%s:%s connected." % client_address)
		client.send(bytes("8jhhaZaaq766712h5aaoaoaoaoppp17127477VVVAHAGgagx0Pz_12", "utf8")) # Sunucuya "şifreli" mesaj gönderir. Oynamayın.
		addresses[client] = client_address
		Thread(target=handle_client, args=(client,)).start()

def handle_client(client):
	while True:
		t = time.localtime()
		current_time = time.strftime("[%H:%M:%S]", t)
		Thread(target=announcements, args=(client,)).start()
		try:
			name = client.recv(BUFSIZ).decode("utf8")
			if name in users:
				client.send(bytes("Looks like you're already connected to the server!", "utf8")) # aynı sunucuya birden fazla client ile bağlanmaya çalışırsanız cliente gönderilecek mesaj.
				try:
					del clients[client]
				except KeyError:
					raise KeyError("[ERROR 100] "+name+" Multiple Client Try.") # aynı sunucuya birden fazla client ile bağlanmaya çalışırsanız sunucu konsolunda gösterilecek mesaj.
			else:
				users.append(name)
				global usernames
				usernames = ', '.join(users)
				welcome = '[Room] Welcome '+ name +'. Enjoy!' + "+"
				tmp = " "
				tmp = tmp.join(list(clients.values()))
				welcome = welcome + tmp
				client.send(bytes(welcome, "utf8"))
				clients[client] = name
				msg = name +" connected to room."+"+"
				joinlog = current_time +" >>>>>"+name +" connected to room." + "<<<<<"
				with open("LOGS.txt","a") as output: # LOGS.txt dosyasına giren kişiyi kayıt alır. 
					output.write(joinlog + '\n')
				output.close()
				tmp = " "
				tmp = tmp.join(list(clients.values()))
				msg = msg + tmp
				broadcast(bytes(msg, "utf8"))
				break
		except ConnectionResetError:

			try:
				del clients[client]
			except:
				pass
			try:
				users.remove(name)
			except:
				pass
				
		except BrokenPipeError:
			pass
	while True:

		try:
			msg = client.recv(BUFSIZ)
			checkMessage = str(msg)
			if len(msg) > 60:
				client.send(bytes("[Room] Message is too long (maximum is 60 characters).", "utf8")) # mesaj 60 karakterden uzun ise yayınlanmaz ve hata mesajı gönderilir.

			elif (msg == "7AHSGHA8125125125.AGSAGMKJASAH_1571257125AHSH.ZZZZZ"): # oynamayın.
				client.send(bytes("[Room] Failed to send message, try again...", "utf8"))

			elif (checkMessage.find("kagsjhHYA") != -1): # Dosya gönderildiği zaman sunucudaki herkese bildirilir. Oynaşmayın.
				sender = checkMessage.split("+")[1]
				filename = checkMessage.split("+")[2]
				newFile = "jkkasgjasg76666AJHAHAHxxxxCf"+"+"+"[Room] "+sender + " has sent '"+filename+"."
				broadcast(bytes(newFile, "utf8"))

			else:
				broadcast(msg, name+": ")
			
			
		except:
			try:
				client.close()
				users.remove(name)
				del clients[client]
				msg = name +" left the chat."+"+"
				leftlog = current_time +" >>>>>"+name + " left the chat." + "<<<<<"
				with open("LOGS.txt","a") as output: # Sunucudan ayrılınca LOGS.txt dosyasına kayıt alır.
					output.write(leftlog + '\n')
				output.close()
				msg = msg + name
				broadcast(bytes(msg, "utf8"))
				break
			except KeyError:
				break
			else:
				msg = name +" left the chat."+"+"
				leftlog1 = current_time +" >>>>>" +name + " left the chat." + "<<<<<"
				with open("LOGS.txt","a") as output: # Sunucudan ayrılınca LOGS.txt dosyasına kayıt alır.
					output.write(leftlog1 + '\n')
				output.close()
				msg = msg + name
				try:
					del clients[client]
				except KeyError:
					break
				broadcast(bytes(msg, "utf8"))
				users.remove(name)
				break

		if msg != "1J731JSG81jags881952kdpiSf18shj-123aasgxXAGa11_sfgCCCXXzzzz":

			msglog = msg.decode("utf8").rstrip()
			namelog = name

			message_log = current_time +" " +namelog + ": " + msglog
			with open("LOGS.txt","a") as output: # Gönderilen bütün mesajları LOGS.txt dosyasına kaydeder.
				output.write(message_log + '\n')

def announcements(client): # zaman aşımına uğramamak için yazılmış fonksiyon. Oynamayın.
	while True:
		try:
			time.sleep(120)
			timeoutProtect = "1J731JSG81jags881952kdpiSf18shj-123aasgxXAGa11_sfgCCCXXzzzz"
			client.send(bytes(timeoutProtect, "utf8"))
			time.sleep(120)
		except OSError:
			pass
def broadcast(msg, prefix=""): # Mesajları bütün clientlere ileten fonksiyon.
	for sock in clients:
		sock.send(bytes(prefix, "utf8")+msg)

users = []
clients = {}
addresses = {}

with open("port.txt", 'r') as f: # port.txt dosyasından portu alır.
	portstr = f.readline().strip()

HOST = '127.0.0.1' # Buraya ssh serverinizin IP adresini girin.
PORT = int(portstr)
BUFSIZ = 1024
ADDR = (HOST, PORT)

SERVER = socket.socket(family = socket.AF_INET, type = socket.SOCK_STREAM, proto = 0)
SERVER.bind((ADDR))

if __name__ == "__main__": # konsolda çıkacak yazılar. Print dışındaki bölümlerle fazla oynamayın.
	SERVER.listen(5)
	print(Fore.GREEN + "Server Started!")
	print(Fore.GREEN + "Clients now can connect.")
	print(Fore.GREEN + "Listening...\n")
	ACCEPT_THREAD = Thread(target=accept_incoming_connections)
	ACCEPT_THREAD.start()
	ACCEPT_THREAD.join()
	SERVER.close()

