#__author__ = 'Otniel Yeheskiel'

#import sys
from __future__ import print_function
from time import sleep
from sys import stdin, exit
from PodSixNet.Connection import connection, ConnectionListener
from thread import *
import random
import os
hangmanpics = ['''
                +---+
                |   |
                    |
                    |
                    |
                    |
                    |
              =========== ''','''
                +---+
                |   |
                O   |
                    |
                    |
                    |
                    |
              =========== ''','''
                +---+
                |   |
                O   |
                |   |
                    |
                    |
                    |
              =========== ''','''
                +---+
                |   |
                O   |
               /|   |
                    |
                    |
                    |
              =========== ''','''
                +---+
                |   |
                O   |
               /|\  |
                    |
                    |
                    |
              =========== ''','''
                +---+
                |   |
                O   |
               /|\  |
               /    |
                    |
                    |
              =========== ''','''
                +---+
                |   |
                O   |
               /|\  |
               / \  |
                    |
              =========== ''']

Kosakata = 'bankok bangalore hyderabad newyork shangai berlin calcutta ' \
           'india australia egypt ghana japan china pakistan afghanistan kenya libya chile ' \
           'bankok bangalore hyderabad newyork shangai berlin calcutta shashank ' \
           'gandhi hitler nehru che jackie brucelee vallabaipatel vivekananda'

def RefKosakata():
    print('Tebak huruf dibawah ini')
    return Kosakata.split()

# RandomKata - Fungsi untuk mengambil 1 kata secara Random yang akan ditebak
def RandomKata(list_kata):
    indeks_kata = random.randint(0,len(list_kata)-1)    # Random indeks yang ada di list Kosakata
    return list_kata[indeks_kata]
# Display - tampilkan tebakan (logic game)
def display(hangmanpics, huruf_salah, huruf_benar, tebak_kata):
    os.system('cls')
    print(hangmanpics[len(huruf_salah)])  # Tampilkan Hang-man sejumlah huruf yang salah
    print()

    print("Huruf yang salah:", end=" ")   # Huruf yang salah
    for huruf in huruf_salah:
        print(huruf, end=" ")
    print()
    print()

    kosong = '_' * len(tebak_kata)  # Simpan kolom kosong yang masih belum ditebak

    for a in range(len(tebak_kata)):
        if tebak_kata[a] in huruf_benar:    # Jika huruf ke-i sudah benar maka ditampilkan
            kosong = kosong[:a] + tebak_kata[a] + kosong[a+1:]  # Isi Kolom yang benar dengan Huruf yang benar
    # Tampilkan kolom yg blm benar ditebak
    for huruf in kosong:
        print(huruf,end=" ")
    print()
    print()
# Uji huruf yang ditebak apakah benar atau tidak
def is_tebak(tebakhuruf):
    while True:
        print('Masukkan huruf yang ingin ditebak ')
        tebak = raw_input()
        tebak = tebak.lower()
        if len(tebak) != 1:
            print('Masukkan hanya 1 huruf')
        elif tebak in tebakhuruf:
            print('Huruf ini sudah ditebak, masukkan huruf yang lain ')
        else:
            return tebak
def playagain():
    print('Do you wanna play again? (Yes or No)')
    return raw_input().lower().startswith('y')
class Client(ConnectionListener):
    def __init__(self, host, port):
        self.Connect((host, port))
        print ("Chat client started")
        print ("Ctrl-C to exit")
        # get a pemain from the user before starting
        print ("Enter your pemain: ")
        connection.Send({"action": "pemain", "pemain": stdin.readline().rstrip("\n")})
        # launch our threaded input loop
        t = start_new_thread(self.InputLoop, ())
        self.la = []

    def Loop(self):
        connection.Pump()
        self.Pump()

    def InputLoop(self):
        # horrid threaded input loop
        # continually reads from stdin and sends whatever is typed to the server
        kata = RefKosakata()
        huruf_salah = ""
        huruf_benar = ""
        tebak_kata = RandomKata(kata)
        done = False
        while 1:
            display(hangmanpics,huruf_salah,huruf_benar,tebak_kata)
            guess = is_tebak(huruf_salah + huruf_benar)
            if guess in tebak_kata:
                huruf_benar = huruf_benar + guess
                found = True
                for i in range(len(tebak_kata)):
                    if tebak_kata[i] not in huruf_benar:
                        found = False
                        break
                if found:
                    print('Menang! ')
                    print('Berhasil menebak kata -----> ' +tebak_kata.upper())
                    done = True
            else:
                huruf_salah = huruf_salah + guess
                if len(huruf_salah) == len(hangmanpics)-1 :
                    display(hangmanpics,huruf_salah,huruf_benar,tebak_kata)
                    print('Anda telah kalah, kata yang benar adalah :' +tebak_kata)
                    done = True
            if done:
                if playagain():
                    os.system('cls')
                    kata = RefKosakata()
                    huruf_salah = ''
                    huruf_benar = ''
                    done = False
                    tebak_kata = RandomKata(kata)
                else:
                    print('Terimakasih sudah bermain')
                    break

            #connection.Send({"action": "message", "message": stdin.readline().rstrip("\n")})

    #######################################
    ### Network event/message callbacks ###
    #######################################

    # Menerima data players dari action 'players' lalu menampilkan di client
    def Network_players(self, data):
        print ("*** players: " + ", ".join([p for p in data['players']]))
    # Menerima data message dari action 'message' Server lalu menampilkan di client
    def Network_message(self, data):
        print (data['who'] + ": " + data['message'])
    # Menerima gambar
    def Network_gambar(self, data):
        self.la = [p for p in data['gambar']]
        self.terima_gambar()
    # built in stuff
    def terima_gambar(self):
        print (self.la[3])

    def Network_connected(self, data):
        print ("You are now connected to the server")

    def Network_error(self, data):
        print ('error:', data['error'][1])
        connection.Close()

    def Network_disconnected(self, data):
        print ('Server disconnected')
        exit()
if __name__ == '__main__':
    host,port = ["localhost",31425]
    c = Client(host, int(port))
    while 1:
        c.Loop()
        sleep(0.001)