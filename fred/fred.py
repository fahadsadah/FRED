#!/usr/bin/python
import serial
import pygame
import sys

ser = serial.Serial("/dev/alfie", 9600)

pygame.mixer.init(44100, -16, 2, 2048)
pygame.mixer.music.set_volume(1)
pygame.mixer.music.load("/root/alfred/doorbell.ogg")

print("FRED 0.3")

while 1:
        card_id = ser.readline().strip()

	if card_id == 'B':
		if not pygame.mixer.music.get_busy():
			pygame.mixer.music.play()
	else:
		sys.stdout.write("Card ID: %s - " % card_id)
		found = False

		members_f = open('members', 'a+')
		members = members_f.readlines()
	
		for member in members:
			member = member.split(',')
        		if card_id in member[0]:
        			ser.write('1')
				ser.write('G')
				found = True
				print("%s opened the door!" % member[1])

		if not found:
			ser.write('R')
			print("not found!")

		members_f.close()
