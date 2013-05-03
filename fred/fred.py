#!/usr/bin/python
import serial
import pygame
import sys
import logging
import socket

def sendMessage(message):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('localhost', 12345))
        s.send('%s' % message)
        s.close()
    except Exception, e:
        pass

ser = serial.Serial("/dev/alfie", 9600)

pygame.mixer.init(44100, -16, 2, 2048)
pygame.mixer.music.set_volume(1)
pygame.mixer.music.load("doorbell.ogg")

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s %(message)s')

fh = logging.FileHandler('fred.log')
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)
logger.addHandler(fh)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
logger.addHandler(ch)

logging.info("FRED 0.4")
sendMessage('#hacmantest ALFRED Rebooted')

while 1:
    card_id = ser.readline().strip()

    if card_id == 'B':
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.play()
            logging.info('Buzzer')
            sendMessage('Buzzer')
    else:
        logging.info("Card ID: %s", card_id)
        found = False

        members_f = open('members', 'r')
        members = members_f.readlines()
    
        for member in members:
            member = member.strip().split(',')
            if card_id in member[0]:
                ser.write('1')
                ser.write('G')
                found = True
                logging.info("%s found, %s opened the door!", card_id, member[1])
                sendMessage("%s opened the hackspace door!" % member[1])

        if not found:
            ser.write('R')
            logging.info("%s not found!", card_id)

        members_f.close()
