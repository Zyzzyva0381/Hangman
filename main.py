# Hangman
# Copyright 2018 by Zhiheng Wang
# All rights reserved. 

try:
	import pygame
	from pygame.locals import *
except ImportError:
	print("Failed to import pygame. ")
try:
	import sys
	import random
	from datetime import datetime
except ImportError:
	print("Failed to import one of the built-in modules. ")
	
def terminate():
	HIGH_SCORE_FW.write(str(HIGH_SCORE))
	HIGH_SCORE_FW.close()
	pygame.quit()
	sys.exit()

def a2s(a):
	s = ""
	for i in a:
		s = s + i + " "
	return s

def posList(a, l):
	returns = []
	length = len(l)
	for i in range(length):
		if l[i] == a:
			returns.append(i)
	return returns

def checkQuit():
	for event in pygame.event.get(QUIT):
		terminate()

def gameOverAni(waitTime):
	print("Step count: %d"%(step))
	startTime = datetime.now().timestamp()
	while True:
		nowTime = datetime.now().timestamp()
		passedTime = nowTime - startTime
		if passedTime >= waitTime:
			HIGH_SCORE_FW.write(str(HIGH_SCORE))
			HIGH_SCORE_FW.close()
			main()
		for event in pygame.event.get(QUIT):
			terminate()

def main():
	global HIGH_SCORE_FW, HIGH_SCORE, step
	
	pygame.init()
	pygame.display.set_caption("Hangman - A Game By Zyzzyva038")
	WORDFILE = open("dicts\\dictionary.txt","r")
	WORD_RLIST = WORDFILE.readlines()
	WORDFILE.close()
	WORDS = []
	for i in WORD_RLIST:
		WORDS.append(i.strip().lower())
	WORD = list(random.choice(WORDS))
	print(WORD)
	WORDLEN = len(WORD)
	step = 0
	WORDWIDTH = 83
	WINDOWWIDTH = WORDLEN * WORDWIDTH
	if WINDOWWIDTH < 498:
		WINDOWWIDTH = 498
	HALFWINDOWWIDTH = WINDOWWIDTH / 2
	WINDOWHEIGHT = 300
	GAMEOVERPOS = (HALFWINDOWWIDTH, 200)
	HASWONPOS = (HALFWINDOWWIDTH, 125)
	SCOREPOS = (HALFWINDOWWIDTH, 175)
	BOARDPOS = (20, 0)
	HELPPOS = (WINDOWWIDTH - 1, WINDOWHEIGHT - 1)
	HELPSCREENPOS = [HALFWINDOWWIDTH, 20]
	HELPSCREENPOSP = 20
	FPS = 40
	FPSCLOCK = pygame.time.Clock()
	nowAni = 0
	HANGMANPOS = (HALFWINDOWWIDTH - 100,50)
	TEXTSIZE = 40
	STEXTSIZE = 10
	FONT = pygame.font.Font("fonts\\console.ttf", TEXTSIZE)
	SFONT = pygame.font.Font("fonts\\console.ttf", STEXTSIZE)
	DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
	correct = []
	for i in range(len(WORD)):
		correct.append("_")
	print(correct)
	helpFile = open("text\\help.txt", "r")
	helpText = helpFile.readlines()
	helpFile.close()
	helpTextLines = []
	for line in helpText:
		helpTextLines.append(line.strip())
	winSound = pygame.mixer.Sound("sounds\\triumph.wav")
	HIGH_SCORE_FR = open("text\\high_score.txt","r")
	HIGH_SCORE = int(HIGH_SCORE_FR.read())
	HIGH_SCORE_FR.close()
	print("Last time high: %d"%(HIGH_SCORE))
	HIGH_SCORE_FW = open("text\\high_score.txt", "w")
	#HIGH_SCORE_FW.write(str(HIGH_SCORE))

	WHITE = (255,255,255)
	BLACK = (0, 0, 0)
	RED = (255,0,0)
	GREEN = (0,255,0)
	BLUE = (0, 0, 255)
	BOARDCOLOR = BLACK
	
	gameOverScrSurf = FONT.render("GAME OVER", True, RED)
	gameOverScrRect = gameOverScrSurf.get_rect()
	gameOverScrRect.center = GAMEOVERPOS
	hasWonScrSurf = FONT.render("YOU WON", True, GREEN)
	hasWonScrRect = gameOverScrSurf.get_rect()
	hasWonScrRect.center = HASWONPOS
	helpButtonSurf = SFONT.render("HELP", True, GREEN, BLUE)
	helpButtonRect = helpButtonSurf.get_rect()
	helpButtonRect.bottomright = HELPPOS
	helpScreenOn = False
	helpTextSurf = []
	helpTextRect = []
	for line in helpTextLines:
		newSurf = SFONT.render(line, True, BLACK)
		newRect = newSurf.get_rect()
		newRect.center = HELPSCREENPOS
		helpTextSurf.append(newSurf)
		helpTextRect.append(newRect)
		HELPSCREENPOS[1] += HELPSCREENPOSP
		
	hangmanAnimation= []
	for i in range(1, 12):
		hangmanAnimation.append(pygame.image.load("pics\\hangmanAnimation\\%d.png"%(i)))
	#print(hangmanAnimation)
	icon = pygame.image.load("pics\\icons\\icon.png")
	pygame.display.set_icon(icon)

	while True:# MAIN LOOP
		DISPLAYSURF.fill(WHITE)
		checkQuit()

		nextAni = False
		posWord = None
		gameOver = False
		hasWon = False

		for event in pygame.event.get():
			if event.type == KEYDOWN and event.unicode != "" and event.unicode != " ":
				if not(event.unicode in correct):
					step += 1
				if not event.unicode in WORD:# guess wrong
					nextAni = True
				else:# guess right
					pos = posList(event.unicode, WORD)
					for i in pos:
						correct[i] = event.unicode
					print(correct)
			if event.type == MOUSEBUTTONUP:
				if helpButtonRect.collidepoint(event.pos):
					helpScreenOn = not helpScreenOn
					print("Help screen on is now %s. "%(helpScreenOn))

		if nextAni:
			if nowAni < 10:
				nowAni += 1
		if nowAni >= 10:
			gameOver = True

		if correct == WORD:
			hasWon = True


		boardSurf = FONT.render(a2s(correct), True, BOARDCOLOR)
		boardRect = boardSurf.get_rect()
		boardRect.topleft = BOARDPOS
		DISPLAYSURF.blit(hangmanAnimation[nowAni],HANGMANPOS)
		DISPLAYSURF.blit(boardSurf, boardRect)
		DISPLAYSURF.blit(helpButtonSurf, helpButtonRect)
		if helpScreenOn:
			for i in range(len(helpTextSurf)):
				DISPLAYSURF.blit(helpTextSurf[i], helpTextRect[i])
		if gameOver:
			DISPLAYSURF.blit(gameOverScrSurf, gameOverScrRect)
		if hasWon:
			winSound.play()
			points = int(WORDLEN / step * 1000)
			if points > HIGH_SCORE:
				HIGH_SCORE = points
			scoreSurf = FONT.render("Score: %d"%(points),True, GREEN)
			scoreRect = scoreSurf.get_rect()
			scoreRect.center = SCOREPOS
			DISPLAYSURF.blit(hasWonScrSurf, hasWonScrRect)
			DISPLAYSURF.blit(scoreSurf, scoreRect)

		pygame.display.update()
		if hasWon or gameOver:
			gameOverAni(3)
			
		FPSCLOCK.tick(FPS)

if __name__ == "__main__":
	main()
