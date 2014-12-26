#__author__ = 'Otniel Yeheskiel'
from __future__ import print_function
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
"""
print('Welcome to Hangman!')
#print(hangmanpics[6])
kata = RefKosakata()
huruf_salah = ""
huruf_benar = ""
tebak_kata = RandomKata(kata)
done = False"""
if __name__ == '__main__':
    print('Welcome to Hangman!')
    #print(hangmanpics[6])
    kata = RefKosakata()
    huruf_salah = ""
    huruf_benar = ""
    tebak_kata = RandomKata(kata)
    done = False
    while True:
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