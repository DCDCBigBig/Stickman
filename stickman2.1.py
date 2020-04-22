#!/usr/bin/python
from tkinter import *
import time,random,sys,pickle
Gametime=0
Timelimit=[[30,40,50],[30,40,50],[30,40,50],[30,40,50],[30,40,50]]
Userslevel=[True,False,False,False,False,False]
try: 
	import easygui
	gui=True
except ImportError:
	gui=False
if not gui:
	print("Sorry,you didn't download easygui.\nPlease download it to continue.")
	input()
	sys.exit(0)
class Coords():
	"""Coords' class"""
	def __init__(self,x1=0,y1=0,x2=0,y2=0):
		self.x1=x1
		self.x2=x2
		self.y1=y1
		self.y2=y2
def within_x(c1,c2):
	if (c1.x1>c2.x1 and c1.x1<c2.x2)or(c1.x2>c2.x1 and c1.x2<c2.x2)or(c2.x1>c1.x1 and c2.x1<c1.x2)or(c2.x2>c1.x1 and c2.x2<c1.x1):
		return True
	else:
		return False
def within_y(c1,c2):
	if (c1.y1>c2.y1 and c1.y1<c2.y2)or(c1.y2>c2.y1 and c1.y2<c2.y2)or(c2.y1>c1.y1 and c2.y1<c1.y2)or(c2.y2>c1.y1 and c2.y2<c1.y1):
		return True
	else:
		return False
def hit_left(c1,c2):
	if within_y(c1,c2):
		if c1.x1<=c2.x2 and c1.x1>=c2.x1:
			return True
		else:
			return False
def hit_right(c1,c2):
	if within_y(c1,c2):
		if c1.x2>=c2.x1 and c1.x2<=c2.x2:
			return True
		else:
			return False
def hit_top(c1,c2):
	if within_x(c1,c2):
		if c1.y1<=c2.y2 and c1.y1>=c2.y1:
			return True
		else:
			return False
def hit_bottom(y,c1,c2):
	if within_x(c1,c2):
		y_calc=c1.y2+y
		if y_calc>=c2.y1 and y_calc<=c2.y2:
			return True
	return False
class Sprite():
	"""Sprite's class"""
	def __init__(self,game):
		self.game=game
		self.endgame=False
		self.coord=None
	def move(self):
		pass
	def coords(self):
		return self.coord
class Stick(Sprite):
	"""Stickman"""
	def __init__(self,game,door,speed,xx,yy,t,l):
		Sprite.__init__(self,game)
		self.image_left=[PhotoImage(file="picture\\l1.gif"),PhotoImage(file="picture\\l2.gif"),PhotoImage(file="picture\\l3.gif")]
		self.image_right=[PhotoImage(file="picture\\r1.gif"),PhotoImage(file="picture\\r2.gif"),PhotoImage(file="picture\\r3.gif")]
		self.image=game.cv.create_image(xx,yy,image=self.image_right[1],anchor="nw")
		self.game.cv.create_text(50,15,text="Level "+str(l+1),font=("Times",15))	
		self.x=0
		self.y=0
		self.current_image=0
		self.current_image_add=1
		self.jump_count=0
		self.last_time=time.time()
		self.coord=Coords()
		self.win=True
		self.door=door
		self.speed=speed
		self.turn=t
		game.cv.bind_all("<KeyPress-Up>",self.jump);
		game.cv.bind_all("<KeyPress-Left>",self.turn_left)
		game.cv.bind_all("<KeyPress-Right>",self.turn_right)
		game.cv.bind_all("<space>",self.jump)
	def turn_left(self,evt):
		if self.y==0:
			self.x=-2
	def turn_right(self,evt):
		if self.y==0:
			self.x=2
	def jump(self,evt):
		if self.y==0:
			self.y=-4
			self.jump_count=0
	def animate(self):
		if self.x!=0 and self.y==0:
			if time.time()-self.last_time>0.1:
				self.last_time=time.time()
				self.current_image+=self.current_image_add
				if self.current_image>=2:
					self.current_image_add=-1
				if self.current_image<=0:
					self.current_image_add=1
		if self.x<0:
			if self.y!=0:
				self.game.cv.itemconfig(self.image,image=self.image_left[2])
			else:
				self.game.cv.itemconfig(self.image,image=self.image_left[self.current_image])
		elif self.x>0:
			if self.y!=0:
				self.game.cv.itemconfig(self.image,image=self.image_right[2])
			else:
				self.game.cv.itemconfig(self.image,image=self.image_right[self.current_image])
	def coords(self):
		xy=self.game.cv.coords(self.image)
		self.coord.x1=xy[0]
		self.coord.y1=xy[1]
		self.coord.x2=xy[0]+27
		self.coord.y2=xy[1]+30
		return self.coord
	def move(self):
		self.animate()
		if self.y<0:
			self.jump_count+=1
			if self.jump_count>20:
				self.y=4
		if self.y>0:
			self.jump_count-=1
		co=self.coords()
		left=True
		right=True
		top=True
		bottom=True
		falling=True
		if self.y>0 and co.y2>=self.game.cv_height:
			self.y=0
			bottom=False
		elif self.y<0 and co.y1<=0:
			self.y=0
			top=False
		if self.x>0 and co.x2>=self.game.cv_width:
			self.x=0
			right=False
		elif self.x<0 and co.x1<0:
			self.x=0
			left=False
		for sprite in self.game.sprites:
			if sprite==self:
				continue
			sprite_co=sprite.coords()
			if top and self.y<0 and hit_top(co,sprite_co):
				self.y=-self.y
				top=False
			if bottom and self.y>0 and hit_bottom(self.y,co,sprite_co):
				self.y=sprite_co.y1-co.y2
				if self.y<0:
					self.y=0
				bottom=False
				top=False
			if bottom and falling and self.y==0 and co.y2<self.game.cv_height and hit_bottom(1,co,sprite_co):
				falling=False
			if left and self.x<0 and hit_left(co,sprite_co):
				self.x=0
				left=False
				if sprite.endgame:
					self.game.run=False
					if self.turn:
						self.game.cv.move(self.image,-13,0)
						self.game.cv.itemconfig(self.image,image=self.image_left[1])
					else:
						self.game.cv.move(self.image,18,0)
						self.game.cv.itemconfig(self.image,image=self.image_right[1])
			if right and self.x>0 and hit_right(co,sprite_co):
				self.x=0
				right=False
				if sprite.endgame:
					self.game.run=False
					if self.turn:
						self.game.cv.move(self.image,-23,0)
						self.game.cv.itemconfig(self.image,image=self.image_left[1])
					else:
						self.game.cv.move(self.image,23,0)
						self.game.cv.itemconfig(self.image,image=self.image_right[1])
			if co.y2>=self.game.cv_height:
				self.win=False
		if falling and bottom and self.y==0 and co.y2<self.game.cv_height:
			self.y=4
		self.game.cv.move(self.image,self.x*self.speed,self.y)
class MovePlatform(Sprite):
	"""MovePlatform"""
	def __init__(self,game,image,x,y,w,h,s,speed):
		Sprite.__init__(self,game)
		self.photo=image
		self.image=game.cv.create_image(x,y,image=self.photo,anchor="nw")
		self.coord=Coords(x,y,x+w,y+h)
		self.w=w
		self.h=h
		self.speed=speed
		if s:
			self.x=-2
		else:
			self.x=2
	def coords(self):
		xy=self.game.cv.coords(self.image)
		self.coord.x1=xy[0]
		self.coord.y1=xy[1]
		self.coord.x2=xy[0]+self.w
		self.coord.y2=xy[1]+self.h
		return self.coord
	def move(self):
		co=self.coords()
		if co.x1<=0:
			self.x=2
		if co.x2>=500:
			self.x=-2
		self.game.cv.move(self.image,self.x*self.speed,0)
class Platform(Sprite):
	"""Platform"""
	def __init__(self,game,image,x,y,w,h):
		Sprite.__init__(self,game)
		self.photo=image
		self.image=game.cv.create_image(x,y,image=self.photo,anchor="nw")
		self.coord=Coords(x,y,x+w,y+h)	
class Door(Sprite):
	"""Door"""
	def __init__(self,game,image,x,y,w,h):
		Sprite.__init__(self,game)
		self.photo=image
		self.image=game.cv.create_image(x,y,image=self.photo,anchor="nw")
		self.coord=Coords(x,y,x+(w/2),y+h)
		self.endgame=True
class Game():
	"""Main class"""
	def __init__(self,level,dif):
		self.tk=Tk()
		self.tk.title("Mr. Stick Game")
		self.tk.resizable(0,0)
		self.cv=Canvas(self.tk,width=500,height=500,highlightthickness=0)
		self.cv.pack()
		self.back=PhotoImage(file="picture\\backboard.gif")
		for i in range(5):
			for j in range(5):
				self.cv.create_image(i*100,j*100,image=self.back,anchor="nw")
		self.cv_height=500
		self.cv_width=500
		self.sprites=[]
		self.run=True
		self.timelimit=Timelimit[level][dif]
	def mainloop(self):
		self.begintime=time.time();
		self.nowtime=time.time();
		self.gametime=self.nowtime-self.begintime;
		self.gametimenum=self.cv.create_text(300,15,text="Time limit:%ds    Gametime:%.2fs"%(self.timelimit,self.gametime),font=("Times",15))
		while 1:
			self.nowtime=time.time();
			self.gametime=self.nowtime-self.begintime;
			self.cv.delete(self.gametimenum)
			self.gametimenum=self.cv.create_text(300,15,text="Time limit:%ds    Gametime:%.2fs"%(self.timelimit,self.gametime),font=("Times",15))
			if self.gametime>self.timelimit:
				s.win=False
			if self.run and s.win:
				for sprite in self.sprites:
					sprite.move()
			else:
				Gametime=self.gametime
				break
			self.tk.update_idletasks()
			self.tk.update()
			time.sleep(0.01)
settings=[1,1]
dif=0
ga=0
log=False
while 1:
	while 1:
		n=easygui.indexbox("Mr. Stick Game\nVers:2.1 Official version","Mr. Stick Game",choices=("Begin","Login","Settings","About","Exit"))
		if n==0:
			if not log:
				while 1:
					easygui.msgbox("Please login first","Please login first")
					lo=easygui.indexbox("Login or Register",choices=("Login","Register"))
					if lo==0:
						while 1:
							inf=open("picture\\save.txt","rb")
							data=pickle.load(inf)
							inf.close()
							name,password=easygui.multpasswordbox("Login","Login",("User name","password"))
							if name in data:
								if data[name][1]==password:
									easygui.msgbox("Login success\nWelcome,"+str(name),"Welcome")
									Userslevel=data[name][2]
									log=True
									break
								else:
									easygui.msgbox("Login fail,\nPlease input right password!","Login fail")
							else:
								easygui.msgbox("Login fail,\nUsername not found","Login fail")
					if lo==1:
						while 1:
							name=""
							name,password=easygui.multpasswordbox("Register","Register",("User name","password"),(name,))
							if name=="":
								easygui.msgbox("Please entry user name","Register fail")
							elif password=="":
								easygui.msgbox("Please entry password","Register fail")
							else:
								inf=open("picture\\save.txt","rb")
								data=pickle.load(inf)
								inf.close()
								data[name]={1:password,2:Userslevel}
								ouf=open("picture\\save.txt","wb")
								pickle.dump(data,ouf)
								ouf.close()
								easygui.msgbox("Register success.\nWelcome,"+str(name),"Welcome")
								log=True
								break
					if log:
						break
			Can=False
			while 1:
				ga=easygui.indexbox("Please choose a level:","Mr. Stick Game",choices=("1","2","3","4","5","Difficulty"))
				if ga==5:
					dif=easygui.indexbox("Please choose the difficulty:","Mr. Stick Game",choices=("Easy","Medium","Hard"))
				else:
					if Userslevel[ga]:
						Can=True
						break
					else:
						easygui.msgbox("Please pass level %d first!"%ga,"You can't play this level now!")		
			if Can:
				break	
		if n==1:
			if not log:
					while 1:
						lo=easygui.indexbox("Login or Register",choices=("Login","Register"))
						if lo==0:
							while 1:
								inf=open("picture\\save.txt","rb")
								data=pickle.load(inf)
								inf.close()
								name,password=easygui.multpasswordbox("Login","Login",("User name","password"))
								if name in data:
									if data[name][1]==password:
										easygui.msgbox("Login success\nWelcome,"+str(name),"Welcome")
										data[name][2]=Userslevel
										log=True
										break
									else:
										easygui.msgbox("Login fail,\nPlease input right password!","Login fail")
								else:
									easygui.msgbox("Login fail,\nUsername not found","Login fail")
						if lo==1:
							while 1:
								name=""
								name,password=easygui.multpasswordbox("Register","Register",("User name","password"),(name,))
								if name=="":
									easygui.msgbox("Please entry user name","Register fail")
								elif password=="":
									easygui.msgbox("Please entry password","Register fail")
								else:
									inf=open("picture\\save.txt","rb")
									data=pickle.load(inf)
									inf.close()
									data[name]={1:password,2:Userslevel}
									ouf=open("picture\\save.txt","wb")
									pickle.dump(data,ouf)
									ouf.close()
									easygui.msgbox("Register success.\nWelcome,"+str(name),"Welcome")
									log=True
									break
						if log:
							break
			else:
				easygui.msgbox("You've logined!","Login")
		if n==2:
			settings=easygui.multenterbox("Settings","Settings",("Platporms' speed","Stickman's speed"),tuple(settings))
		if n==3:
			easygui.msgbox("About:\nAuthor:DCDCBigBig\nTel:13502410898\nEmail:ctdingchang23@163.com\nAddress:$#%&^!\nThanks:MC_Hacker\nWeb:http://code-hub.com/\nCopyright © 2013-2016 Code-hub. All rights reserved.","About",ok_button="Back to menu")
		if n==4:
			sys.exit(0)
	while 1:
		g=Game(ga,dif)
		platform=[]
		if ga==0:
			platform.append(Platform(g,PhotoImage(file="picture\\p3.gif"),0,480,100,10))
			if dif>0:
				platform.append(MovePlatform(g,PhotoImage(file="picture\\p3.gif"),150,440,100,10,True,float(settings[0])))
				platform.append(MovePlatform(g,PhotoImage(file="picture\\p2.gif"),50,300,66,10,False,float(settings[0])))
			else:
				platform.append(Platform(g,PhotoImage(file="picture\\p3.gif"),150,440,100,10))
				platform.append(Platform(g,PhotoImage(file="picture\\p2.gif"),50,300,60,10))
			if dif>1:
				platform.append(MovePlatform(g,PhotoImage(file="picture\\p2.gif"),170,120,60,10,False,float(settings[0])))
				platform.append(MovePlatform(g,PhotoImage(file="picture\\p3.gif"),300,400,100,10,True,float(settings[0])))
			else:
				platform.append(Platform(g,PhotoImage(file="picture\\p2.gif"),170,120,60,10))
				platform.append(Platform(g,PhotoImage(file="picture\\p3.gif"),300,400,100,10))
			platform.append(Platform(g,PhotoImage(file="picture\\p3.gif"),300,160,100,10))
			platform.append(Platform(g,PhotoImage(file="picture\\p2.gif"),175,350,60,10))
			platform.append(Platform(g,PhotoImage(file="picture\\p2.gif"),45,60,60,10))
			platform.append(Platform(g,PhotoImage(file="picture\\p1.gif"),170,250,30,10))
			platform.append(Platform(g,PhotoImage(file="picture\\p1.gif"),230,200,30,10))
			door=Door(g,PhotoImage(file="picture\\d1.gif"),45,30,40,35)
			s=Stick(g,door,float(settings[1]),0,450,True,ga)
		if ga==1:
			platform.append(Platform(g,PhotoImage(file="picture\\p3.gif"),0,480,100,10))
			platform.append(Platform(g,PhotoImage(file="picture\\p2.gif"),400,60,60,10))
			if dif>1:
				platform.append(MovePlatform(g,PhotoImage(file="picture\\p2.gif"),280,400,60,10,True,float(settings[0])))
			else:
				platform.append(Platform(g,PhotoImage(file="picture\\p2.gif"),280,400,60,10))
			if dif>0:
				platform.append(MovePlatform(g,PhotoImage(file="picture\\p2.gif"),180,90,60,10,False,float(settings[0])))
				platform.append(Platform(g,PhotoImage(file="picture\\p2.gif"),400,360,60,10))
			else:
				platform.append(Platform(g,PhotoImage(file="picture\\p2.gif"),180,90,60,10))
				platform.append(Platform(g,PhotoImage(file="picture\\p3.gif"),400,360,100,10))
			platform.append(Platform(g,PhotoImage(file="picture\\p1.gif"),240,240,30,10))
			platform.append(Platform(g,PhotoImage(file="picture\\p2.gif"),160,440,60,10))
			platform.append(Platform(g,PhotoImage(file="picture\\p1.gif"),320,300,30,10))
			platform.append(Platform(g,PhotoImage(file="picture\\p1.gif"),160,180,30,10))
			platform.append(Platform(g,PhotoImage(file="picture\\p1.gif"),80,120,30,10))
			platform.append(Platform(g,PhotoImage(file="picture\\p2.gif"),290,80,60,10))
			door=Door(g,PhotoImage(file="picture\\d1.gif"),430,30,40,35)
			s=Stick(g,door,float(settings[1]),0,450,False,ga)
		if ga==2:
			platform.append(Platform(g,PhotoImage(file="picture\\p2.gif"),0,480,60,10))
			platform.append(Platform(g,PhotoImage(file="picture\\p2.gif"),390,60,60,10))
			if dif>0:
				platform.append(Platform(g,PhotoImage(file="picture\\p2.gif"),290,400,60,10))
				platform.append(Platform(g,PhotoImage(file="picture\\p2.gif"),50,140,60,10))
			else:
				platform.append(Platform(g,PhotoImage(file="picture\\p3.gif"),280,400,100,10))
				platform.append(Platform(g,PhotoImage(file="picture\\p3.gif"),10,140,100,10))
			if dif>1:
				platform.append(MovePlatform(g,PhotoImage(file="picture\\p2.gif"),235,250,60,10,True,float(settings[0])))
				platform.append(MovePlatform(g,PhotoImage(file="picture\\p2.gif"),145,190,60,10,False,float(settings[0])))
			else:
				platform.append(Platform(g,PhotoImage(file="picture\\p2.gif"),235,250,60,10))
				platform.append(Platform(g,PhotoImage(file="picture\\p2.gif"),145,190,60,10))
			platform.append(Platform(g,PhotoImage(file="picture\\p1.gif"),90,430,30,10))
			platform.append(Platform(g,PhotoImage(file="picture\\p1.gif"),150,380,30,10))
			platform.append(Platform(g,PhotoImage(file="picture\\p1.gif"),210,330,30,10))
			platform.append(Platform(g,PhotoImage(file="picture\\p2.gif"),413,350,60,10))
			platform.append(Platform(g,PhotoImage(file="picture\\p1.gif"),335,300,30,10))
			platform.append(Platform(g,PhotoImage(file="picture\\p2.gif"),180,100,60,10))
			platform.append(Platform(g,PhotoImage(file="picture\\p1.gif"),300,90,30,10))
			door=Door(g,PhotoImage(file="picture\\d1.gif"),420,30,40,35)
			s=Stick(g,door,float(settings[1]),0,450,False,ga)
		if ga==3:
			platform.append(Platform(g,PhotoImage(file="picture\\p3.gif"),400,480,100,10))
			platform.append(Platform(g,PhotoImage(file="picture\\p2.gif"),45,60,60,10))
			if dif>0:
				platform.append(Platform(g,PhotoImage(file="picture\\p2.gif"),370,170,60,10))
				platform.append(MovePlatform(g,PhotoImage(file="picture\\p3.gif"),150,370,100,10,True,float(settings[0])))
			else:
				platform.append(Platform(g,PhotoImage(file="picture\\p3.gif"),370,170,100,10))
				platform.append(Platform(g,PhotoImage(file="picture\\p3.gif"),150,370,100,10))
			if dif>1:
				platform.append(MovePlatform(g,PhotoImage(file="picture\\p2.gif"),130,260,60,10,False,float(settings[0])))
			else:
				platform.append(Platform(g,PhotoImage(file="picture\\p2.gif"),130,260,60,10))
			platform.append(Platform(g,PhotoImage(file="picture\\p2.gif"),290,430,60,10))
			platform.append(Platform(g,PhotoImage(file="picture\\p1.gif"),60,330,30,10))
			platform.append(Platform(g,PhotoImage(file="picture\\p2.gif"),250,210,60,10))
			platform.append(Platform(g,PhotoImage(file="picture\\p1.gif"),300,110,30,10))
			platform.append(Platform(g,PhotoImage(file="picture\\p1.gif"),230,140,30,10))
			platform.append(Platform(g,PhotoImage(file="picture\\p1.gif"),150,100,30,10))
			door=Door(g,PhotoImage(file="picture\\d1.gif"),45,30,40,35)
			s=Stick(g,door,float(settings[1]),470,450,True,ga)
		if ga==4:
			platform.append(Platform(g,PhotoImage(file="picture\\p1.gif"),0,480,30,10))
			platform.append(Platform(g,PhotoImage(file="picture\\p2.gif"),55,60,60,10))
			if dif>0:
				platform.append(Platform(g,PhotoImage(file="picture\\p1.gif"),440,250,30,10))
			else:
				platform.append(Platform(g,PhotoImage(file="picture\\p2.gif"),440,250,60,10))
			if dif>1:
				platform.append(MovePlatform(g,PhotoImage(file="picture\\p1.gif"),350,190,30,10,True,float(settings[0])))
			else:
				platform.append(Platform(g,PhotoImage(file="picture\\p1.gif"),350,190,30,10))
			platform.append(Platform(g,PhotoImage(file="picture\\p1.gif"),80,430,30,10))
			platform.append(Platform(g,PhotoImage(file="picture\\p1.gif"),150,370,30,10))
			platform.append(Platform(g,PhotoImage(file="picture\\p1.gif"),240,330,30,10))
			platform.append(Platform(g,PhotoImage(file="picture\\p1.gif"),365,320,30,10))
			platform.append(Platform(g,PhotoImage(file="picture\\p1.gif"),280,120,30,10))
			platform.append(Platform(g,PhotoImage(file="picture\\p1.gif"),180,90,30,10))
			platform.append(Platform(g,PhotoImage(file="picture\\p1.gif"),0,480,30,10))
			door=Door(g,PhotoImage(file="picture\\d1.gif"),55,30,40,35)
			s=Stick(g,door,float(settings[1]),0,450,True,ga)
		for i in platform:
			g.sprites.append(i)
		g.sprites.append(door)
		g.sprites.append(s)
		g.mainloop()
		if s.win:
			time.sleep(0.5)
			g.cv.delete(s.image)
			Userslevel[ga+1]=True
			inf=open("picture\\save.txt","rb")
			data=pickle.load(inf)
			inf.close()
			data[name][2][ga+1]=True
			ouf=open("picture\\save.txt","wb")
			pickle.dump(data,ouf)
			ouf.close()
			if ga==4:
				easygui.msgbox("Mr's Stick is lived!","Mr's Stick is lived!")
				g.tk.destroy()
				easygui.msgbox("Thank for you supporting DCDCBigBig's game.\nNow you've clear all the custorms.\nThanks you, "+str(name)+"\nAuthor:DCDC Big Big\nTel:13502410898\nEmail:ctdingchang23@163.com\nAddress:$#%&^!\nThanks:MC_Hacker\nWeb:http://code-hub.com/\nCopyright © 2013-2016 Code-hub. All rights reserved.","Thanks")
				sys.exit(0)
			while 1:
				winc=easygui.indexbox(str(name)+", You win!\nGametime:%.2fs"%g.gametime,"You win!",choices=("Back to menu","Play again","Next level","Change difficulty"))
				if winc==0:
					g.tk.destroy()
					break
				if winc==1:
					g.tk.destroy()
					break
				if winc==2:
					g.tk.destroy()
					ga+=1
					break
				if winc==3:
					dif=easygui.indexbox("Choose a difficulty:","Mr's Stick Game",choices=("Easy","Medium","Hard"))
			if winc==0:
				break
		else:
			time.sleep(0.1)
			Fall=False
			if g.gametime<g.timelimit:
				Fall=True
				for i in range(15):
					g.cv.move(s.image,0,2)
					time.sleep(0.035)
					g.tk.update()
					g.tk.update_idletasks()
			while 1:
				if Fall:
					losc=easygui.indexbox(str(name)+", You lose!","You lose!",choices=("Back to menu","Try again","Change difficulty"))
				else:
					losc=easygui.indexbox(str(name)+", Time Limit Exceeded!","TLE!",choices=("Back to menu","Try again","Change difficulty"))
				if losc==0:
					g.tk.destroy()
					break
				if losc==1:
					g.tk.destroy()
					break
				if losc==2:
					dif=easygui.indexbox("Choose a difficulty:","Mr's Stick Game",choices=("Easy","Medium","Hard"))
			if losc==0:
				break