#importing the libraries
from tkinter import ttk
from tkinter.font import BOLD 
from tinytag import TinyTag
from tkinter import *
from pygame import mixer
import os
import time
import random
import pyautogui

#library for album image managing
import eyed3
import io
from PIL import Image,ImageTk 

#sqlite3 for data management
import sqlite3

#database creation for the first time app opening
con=sqlite3.connect("Melo_database.db")
cur=con.cursor()

sql_songs_list1=[]
system_songs=[]
try:
	cur.execute("create table melo_dat(songs_without_path text,songs_with_path text,favourite int,most_played int default 0,current int default 1,playlist1 int default 0,p1name text default 'playlist_1',playlist2 int default 0,p2name text default 'playlist_2',playlist3 int default 0,p3name text default 'playlist_3',playlist4 int default 0,p4name text default 'playlist_4',playlist5 int default 0,p5name text default 'playlist_5')")
	cur.execute("")
except:
	pass

cur.execute("select * from melo_dat")
for i in cur:
	sql_songs_list1.append(i[1])

mixer.init()

#creating the list of songs
songs_list_without_index=[]
songs_list=[]
list1=""
x=os.path.join(os.path.expandvars("%userprofile%"))
drives = [ chr(x) + ":" for x in range(65,91) if os.path.exists(chr(x) + ":") ]
drives.remove("C:")
drives.append(x)
print(drives)
for i in drives:
	for root, dirs, files in os.walk(i+"\\"):
		for file in files:
			try:
				if (file.endswith('.mp3') or file.endswith('.mpeg')):
					#list1=root+"\\"+file
					b=root+"\\"+file
					a=file
					system_songs.append(b)
					if b not in sql_songs_list1:
						cur.execute(f"insert into melo_dat (songs_without_path,songs_with_path) values('{a}','{b}')")
						con.commit()
			except:
				pass

if sql_songs_list1==system_songs:
        print("Both list are equal")
else:
        print("not equla")
to_delete=[]
for i in sql_songs_list1:
        if i not in system_songs:
                to_delete.append(i)


for i in to_delete:
        cur.execute(f"delete from melo_dat where songs_with_path='{i}'")
        con.commit()


length_of_songsList=len(songs_list)

#creating a main window with title and icon
root=Tk()
root.geometry("1000x600+450+100")
root.resizable(0,0)
root.title("Melo")

#app icon
app_icon = PhotoImage(file = ".\\resources\\icon.png")
root.iconphoto(False, app_icon)

#defaut variables
starting_time=0
current_song=0
current_index=0
suffle=0
loop=1
repeat_one=0
selected_in_listbox=0
faourite_songs=[]
single=0
EXIT=0
a=0
minutes=0
seconds=0

#progressbar slider
var = IntVar()
def motion(event):
	global a,minutes,seconds
	proportion = event.x / event.widget.winfo_width()
	var.set(int(proportion*200))
	print(int(proportion*200))
	a=int(proportion*200)
	mixer.music.set_pos(a)
	minutes=int(a/60)
	seconds=int(a%60)

#timer
def timer(song):
		global songs_list,current_index,a,minutes,seconds
		tag=TinyTag.get(song)
		time1=tag.duration
		minutes=00
		seconds=00
		a=0
		progress_bar.config(maximum=int(time1))
		print(int(time1))
		while(a<=int(time1)):
			if seconds==60:
					minutes+=1
					seconds=0
			var.set(a)
			print(a)
			Time_view.config(text=str(minutes)+":"+str(seconds))
			time.sleep(0.1)
			root.update()
			time.sleep(0.1)
			root.update()
			time.sleep(0.1)
			root.update()
			time.sleep(0.1)
			root.update()
			time.sleep(0.1)
			root.update()
			time.sleep(0.1)
			root.update()
			time.sleep(0.1)
			root.update()
			time.sleep(0.1)
			root.update()
			time.sleep(0.1)
			root.update()
			time.sleep(0.1)
			root.update()
			seconds+=1
			while current_song==0:
					root.update()
					pass
			if EXIT==1:
					return
			a=a+1
		next()

#new implementations
def on_closing():
        global EXIT       
        EXIT=1
        try:
                mixer.music.stop()
                mixer.music.unload()
                mixer.quit()
        except:
                mixer.music.stop()
                mixer.music.unload()
        root.destroy()
        os._exit(0)		
root.protocol("WM_DELETE_WINDOW", on_closing)


#Song timer controls
def song_detaills():
	global songs_list,current_index
	tag=TinyTag.get(songs_list[current_index])
	artist=tag.artist
	try:
		Artist_name.config(text="Artist :"+artist)
	except:
		Artist_name.config(text="Artist : Not available")
	return

#function to play the song
def play():
	global starting_time,songs_list,list_of_tracks,current_song
	if starting_time==0:
		list_of_tracks.activate(0)
		mixer.music.load(songs_list[0])
		temp=songs_list[0]
		album_image_process(temp)
		mixer.music.play()
		play.config(image=Photo_play)
		favourite_heart.config(image=Photo_white_heart)
		starting_time=1
		current_song=1
		Track_title.config(text=list_of_tracks.get(0))
		song_detaills()
		most_played()
	elif current_song==1:
		mixer.music.pause()
		play.config(image=Photo_pause)
		current_song=0	
	else:
		mixer.music.unpause()
		play.config(image=Photo_play)
		current_song=1
	return

#function for nex button
def next():
	global songs_list,current_index,starting_time,current_song,suffle,selected_in_listbox
	if (loop==1 and selected_in_listbox==0):
		if (current_index<length_of_songsList-1):
			current_index+=1
		else:
			if loop==1:
				current_index=0
	elif (suffle==1 and selected_in_listbox==0):
		current_index=random.randrange(0,length_of_songsList)
	elif selected_in_listbox==1:
		current_index+=1
		selected_in_listbox=0	
	else:
		pass
	favourite_heart.config(image=Photo_white_heart)
	list_of_tracks.activate(current_index)
	mixer.music.load(songs_list[current_index])
	mixer.music.play()
	play.config(image=Photo_play)
	current_song=1
	starting_time=1
	temp=songs_list[current_index]
	album_image_process(temp)
	Text=list_of_tracks.get(current_index)
	data2=Text[0:43]
	Track_title.config(text=data2)
	song_detaills()
	most_played()
	timer(songs_list[current_index])
	return

#function for previous song
def previous():
	global songs_list,current_index,starting_time,current_song,selected_in_listbox
	if (loop==1 and selected_in_listbox==0):
		if (current_index>0):
			current_index-=1
		else:
			if loop==1:
				current_index=length_of_songsList-1
	elif (suffle==1 and selected_in_listbox==0):
		current_index=random.randrange(0,length_of_songsList)
	elif selected_in_listbox==1:
		current_index+=1
		selected_in_listbox=0	
	else:
		pass
	favourite_heart.config(image=Photo_white_heart)
	list_of_tracks.activate(current_index)
	mixer.music.load(songs_list[current_index])
	mixer.music.play()
	play.config(image=Photo_play)
	current_song=1
	starting_time=1
	temp=songs_list[current_index-1]
	album_image_process(temp)
	Text=list_of_tracks.get(current_index)
	data2=Text[0:43]
	Track_title.config(text=data2)
	song_detaills()
	most_played()
	timer(songs_list[current_index])
	return
	
#function to change track title when a listbox item is clicked
def callback(event):
	global current_song,starting_time,current_index,selected_in_listbox
	selection=event.widget.curselection()
	if selection:
		index=selection[0]
		data=event.widget.get(index)
		Track_title.configure(text=data)
		#from here i written to select and play option
		# selected_song(index)
		current_index=index-1
		selected_in_listbox=1
		next()
	else:
		Track_title.configure(text="No Track selected -------")
	return

#function  for volume controls
def volume_up():
	pyautogui.press('volumeup',3)

def volume_down():
	pyautogui.press('volumedown',3)

#suffle function
def Suffle():
	global suffle,loop,repeat_one
	if repeat_one==0 and loop==1:
		suffle=1
		repeat_one=0
		loop=0
		Music_Suffle.config(image=Photo_suffle)
	
	elif repeat_one==0 and suffle==1:
		repeat_one=1
		loop=0
		suffle=0
		Music_Suffle.config(image=Photo_repeat_one)
	elif loop==0:
		loop=1
		suffle=0
		repeat_one=0
		Music_Suffle.config(image=Photo_loop)
	else:
		pass
	return

#Album art modification functions
def album_image_process(song_name):
	try:	
		song_name=songs_list[current_index]
		song=eyed3.load(song_name)
		img=Image.open(io.BytesIO(song.tag.images[0].image_data))
		image1=img.resize((300,300),Image.ANTIALIAS)
		image1=ImageTk.PhotoImage(image1)
		album_label.configure(image=image1)
		album_label.image=image1
	except:
		i=random.randint(1,7)
		image_except=Image.open(f".\\resources\\{i}.jpg")
		image2=ImageTk.PhotoImage(image_except)
		album_label.configure(image=image2)
		album_label.image=image2
	return

#library songs
def library_songs():
    global songs_list_without_index,songs_list,length_of_songsList
    list_of_tracks.delete(0,END)
    songs_list=[]
    songs_list_without_index=[]
    length_of_songsList=0
    cur.execute("select * from melo_dat")
    for i in cur:
        songs_list_without_index.append(i[0])
        songs_list.append(i[1])
    length_of_songsList=len(songs_list)
    for i in range(length_of_songsList):
        a=str(i+1)+". "+songs_list_without_index[i]
        list_of_tracks.insert(i,str(i+1)+". "+songs_list_without_index[i])
    return
        
def add_favourite():
	global songs_list,current_index
	try:
		a=songs_list[current_index]
	except:
		a=list_for_most_played_buttons[current_index][1]
	cur.execute(f"update melo_dat set favourite=1 where songs_with_path='{a}'") 
	con.commit()
	favourite_heart.config(image=Photo_red_heart)
	root.update()
	return

#adding songs for library favourite
def library_favourite():
	global songs_list_without_index,songs_list,length_of_songsList
	list_of_tracks.delete(0,END)
	songs_list=[]
	songs_list_without_index=[]
	length_of_songsList=0
	cur.execute("select * from melo_dat where favourite=1")
	for i in cur:
		songs_list_without_index.append(i[0])
		songs_list.append(i[1])
	length_of_songsList=len(songs_list)
	for i in range(length_of_songsList):
		a=str(i+1)+". "+songs_list_without_index[i]
		list_of_tracks.insert(i,str(i+1)+". "+songs_list_without_index[i])
	return

#increamenting most played
def most_played():
	global songs_list,current_index
	a=songs_list[current_index]
	root.update()
	cur.execute(f"update melo_dat set most_played=most_played+1 where songs_with_path='{a}'")
	con.commit()
	root.update()
	return

cur.execute("select max(most_played),songs_with_path,songs_without_path from melo_dat group by songs_with_path")
list_for_most_played_buttons=[]
for i in cur:
	list_for_most_played_buttons.append(i)
list_for_most_played_buttons=sorted(list_for_most_played_buttons,reverse=True)

#functions for most played list buttons
def most_played_list():
	global songs_list_without_index,songs_list,length_of_songsList,list_for_most_played_buttons
	list_of_tracks.delete(0,END)
	songs_list=[]
	songs_list_without_index=[]
	length_of_songsList=0
	for i in list_for_most_played_buttons:
		songs_list_without_index.append(i[2])
		songs_list.append(i[1])
	length_of_songsList=len(songs_list)
	for i in range(length_of_songsList):
		a=str(i+1)+". "+songs_list_without_index[i]
		list_of_tracks.insert(i,str(i+1)+". "+songs_list_without_index[i])
	return

#common functions of buttons
button_music=0
def buttons_common(index):
	global button_music,starting_time,current_song,current_index,list_for_most_played_buttons,button_music
	current_index=0
	current_song=1
	starting_time=1
	button_music=list_for_most_played_buttons[index][1]
	mixer.music.load(button_music)
	mixer.music.play()	
	text=list_for_most_played_buttons[index][2]
	data2=text[0:43]
	Track_title.config(text=data2)
	play.config(image=Photo_play)
	tag=TinyTag.get(button_music)
	artist=tag.artist
	try:
		Artist_name.config(text="Artist :"+artist)
	except:
		Artist_name.config(text="Artist : Not available")
	root.update()
	timer(button_music)
	root.update()
	return

# most_played button album art 
def most_album_art(index):
	try:
		song_name=list_for_most_played_buttons[index][1]
		song=eyed3.load(song_name)
		img=Image.open(io.BytesIO(song.tag.images[0].image_data))
		image1=img.resize((300,300),Image.ANTIALIAS)

		image1=ImageTk.PhotoImage(image1)
		album_label.configure(image=image1)
		album_label.image=image1
	except:
		image3=PhotoImage(file=".\\resources\\music.png")
		album_label.configure(image=image3)
		album_label.image=image3
	return

# calling buttons
def button1():
	most_album_art(0)
	most_played_list()
	buttons_common(0)
	return
def button2():
	most_album_art(1)
	most_played_list()
	buttons_common(1)
	return
def button3():
	most_album_art(2)
	most_played_list()
	buttons_common(2)
	return
	
def button4():
	most_album_art(3)
	most_played_list()
	buttons_common(3)
	return
def button5():
	most_album_art(4)
	most_played_list()
	buttons_common(4)
	return

#window for add playlist
def add_playlist1(index):
	songs=[]
	selected_items=[]
	win=Toplevel(root)
	win.configure(bg="#999999")
	win.geometry("500x525+350+100")
	name=Label(win,text="Name ",bg="#999999")
	name.place(x=3,y=3)
	entry=Entry(win)
	entry.place(x=53,y=5)
	lbl_name=Label(win,text="Songs",font=("Georgia",15),fg="red",bg="#999999")
	lbl_name.place(x=210,y=40)
	lb=Listbox(win,font=("Georgia",12),bg="#343434",fg="white",width=49,height=22,border=0,selectbackground="red",selectmode=MULTIPLE)
	lb.place(x=2,y=67)
	songs2=[]
	cur.execute("select * from melo_dat")
	for i in cur:
		songs.append(i[1])
		songs2.append(i[0])
	for i in range(len(songs2)):
		lb.insert(i,str(i+1)+". "+songs2[i])
	def remove():
		for i in lb.curselection():
			song=songs[i]
			cur.execute(f"update melo_dat set playlist{index}=0 where songs_with_path='{song}'")
			con.commit()
		root.update()
		win.destroy()
	def add():
		for i in lb.curselection():
			song=songs[i]
			cur.execute(f"update melo_dat set playlist{index}=1 where songs_with_path='{song}'")
			con.commit()
		get_value=entry.get()
		if get_value!="":
			if index==1:
				cur.execute(f"update melo_dat set p1name='{get_value}' where playlist1>=0")
			if index==2:
				cur.execute(f"update melo_dat set p2name='{get_value}' where playlist2>=0")
			if index==3:
				cur.execute(f"update melo_dat set p3name='{get_value}' where playlist3>=0")
			if index==4:
				cur.execute(f"update melo_dat set p4name='{get_value}' where playlist4>=0")
			if index==5:
				cur.execute(f"update melo_dat set p5name='{get_value}' where playlist5>=0")
			con.commit()
		if index==1:
			cur.execute("select p1name from melo_dat")
			for i in cur:
				playlist1.config(text=i)
		if index==2:
			cur.execute("select p2name from melo_dat")
			for i in cur:
				playlist2.config(text=i)
		if index==3:
			cur.execute("select p3name from melo_dat")
			for i in cur:
				playlist3.config(text=i)
		if index==4:
			cur.execute("select p4name from melo_dat")
			for i in cur:
				playlist4.config(text=i)
		if index==5:
			cur.execute("select p5name from melo_dat")
			for i in cur:
				playlist5.config(text=i)
		if index==5:
			cur.execute("select p5name from melo_dat")
			for i in cur:
				playlist5.config(text=i)
		root.update()
		win.destroy()
	btn=Button(win,text="ADD",command=add,bd=0,width=15)
	btn.place(x=100,y=490)
	btn_rem=Button(win,text="REMOVE",command=remove,bd=0,width=15)
	btn_rem.place(x=260,y=490)
	win.mainloop()
	
#function of playlist buttons
def playlist0(index):
	global songs_list_without_index,songs_list,length_of_songsList
	list_of_tracks.delete(0,END)
	songs_list=[]
	songs_list_without_index=[]
	length_of_songsList=0
	cur.execute("select * from melo_dat")
	for i in cur:
		if (i[index]==1) and (i[0] not in songs_list):
			songs_list_without_index.append(i[0])
			songs_list.append(i[1])
	length_of_songsList=len(songs_list)
	for i in range(length_of_songsList):
		list_of_tracks.insert(i,str(i+1)+". "+songs_list_without_index[i])
	return

#most played default images
def most_played_images(index):
	try:
		song_name=list_for_most_played_buttons[index][1]
		song=eyed3.load(song_name)
		img=Image.open(io.BytesIO(song.tag.images[0].image_data))
		image1=img.resize((132,123),Image.ANTIALIAS)
		image1=ImageTk.PhotoImage(image1)
		if index==0:
			button_1.configure(image=image1)
			button_1.image=image1
		if index==1:
			button_2.configure(image=image1)
			button_2.image=image1
		if index==2:
			button_3.configure(image=image1)
			button_3.image=image1
		if index==3:
			button_4.configure(image=image1)
			button_4.image=image1
		if index==4:
			button_5.configure(image=image1)
			button_5.image=image1
	except:
		image2=PhotoImage(file=".\\resources\\8.png")
		if index==0:
			button_1.configure(image=image2)
			button_1.image=image2
		if index==1:
			button_2.configure(image=image2)
			button_2.image=image2
		if index==2:
			button_3.configure(image=image2)
			button_3.image=image2
		if index==3:
			button_4.configure(image=image2)
			button_4.image=image2
		if index==4:
			button_5.configure(image=image2)
			button_5.image=image2
	return

#calling function to add playlist
def add_playlist_1():
	add_playlist1(1)
	return
def add_playlist_2():
	add_playlist1(2)
	return
def add_playlist_3():
	add_playlist1(3)
	return
def add_playlist_4():
	add_playlist1(4)
	return
def add_playlist_5():
	add_playlist1(5)
	return

#calling playlist button functions
def playlist_1():
	playlist0(5)
	return
def playlist_2():
	playlist0(7)
	return
def playlist_3():
	playlist0(9)
	return
def playlist_4():
	playlist0(11)
	return
def playlist_5():
	playlist0(13)
	return

#options frame
Options=Frame(root,bg="#000000",height=560,width=170)
Options.place(x=0,y=0)
melo_label=Label(Options,text="Melo",font=("Georgia",35,"bold"),fg="red",bg="#000000")
melo_label.place(x=5,y=5)

#Library
playlist_options_label=Label(Options,text="Library",fg="white",bg="black",font=("Georgia",15,"bold"))
playlist_options_label.place(x=5,y=90)

#library images
songs_image=PhotoImage(file=".\\resources\\songs.png")
fav_image=PhotoImage(file=".\\resources\\fav.png")
most_play_image=PhotoImage(file=".\\resources\\most.png")

#library labels
songs_label=Label(Options,image=songs_image,bg="black")
songs_label.place(x=30,y=135)
fav_label=Label(Options,image=fav_image,bg="black")
fav_label.place(x=30,y=171)
most_play_label=Label(Options,image=most_play_image,bg="black")
most_play_label.place(x=30,y=205)

#library options
songs_button=Button(Options,text="Songs",fg="white",anchor="w",bd=0,bg="black",font=("Georgia",10,"bold"),width=9,command=library_songs)
songs_button.place(x=60,y=135)

Favourite_button=Button(Options,text="Favourite",anchor="w",fg="white",bd=0,bg="black",font=("Georgia",10,"bold"),width=9,command=library_favourite)
Favourite_button.place(x=60,y=171)

most_played_button=Button(Options,text="Most Played",anchor="w",fg="white",bd=0,bg="black",font=("Georgia",10,"bold"),width=9,command=most_played_list)
most_played_button.place(x=55,y=205)

#playlist
Playlist_label=Label(Options,text="Playlist",fg="white",bg="black",font=("Georgia",15,"bold"))
Playlist_label.place(x=5,y=280)

#option to add playlist
add_playlist1_button=Button(Options,text="+",fg="white",bd=0,bg="black",font=("Georgia",10,"bold"),command=add_playlist_1)
add_playlist1_button.place(x=10,y=350)
add_playlist2_button=Button(Options,text="+",fg="white",bd=0,bg="black",font=("Georgia",10,"bold"),command=add_playlist_2)
add_playlist2_button.place(x=10,y=380)
add_playlist3_button=Button(Options,text="+",fg="white",bd=0,bg="black",font=("Georgia",10,"bold"),command=add_playlist_3)
add_playlist3_button.place(x=10,y=410)
add_playlist4_button=Button(Options,text="+",fg="white",bd=0,bg="black",font=("Georgia",10,"bold"),command=add_playlist_4)
add_playlist4_button.place(x=10,y=440)
add_playlist5_button=Button(Options,text="+",fg="white",bd=0,bg="black",font=("Georgia",10,"bold"),command=add_playlist_5)
add_playlist5_button.place(x=10,y=470)

#playlists
cur.execute("select * from melo_dat")
p1name="Playlist_1"
p2name="Playlist_2"
p3name="Playlist_3"
p4name="Playlist_4"
p5name="Playlist_5"
for i in cur:
	p1name=i[6]
	p2name=i[8]
	p3name=i[10]
	p4name=i[12]
	p5name=i[14]

playlist1=Button(Options,text=p1name,fg="white",bd=0,bg="black",font=("Georgia",10,"bold"),command=playlist_1)
playlist1.place(x=40,y=350)
playlist2=Button(Options,text=p2name,fg="white",bd=0,bg="black",font=("Georgia",10,"bold"),command=playlist_2)
playlist2.place(x=40,y=380)
playlist3=Button(Options,text=p3name,fg="white",bd=0,bg="black",font=("Georgia",10,"bold"),command=playlist_3)
playlist3.place(x=40,y=410)
playlist4=Button(Options,text=p4name,fg="white",bd=0,bg="black",font=("Georgia",10,"bold"),command=playlist_4)
playlist4.place(x=40,y=440)
playlist5=Button(Options,text=p5name,fg="white",bd=0,bg="black",font=("Georgia",10,"bold"),command=playlist_5)
playlist5.place(x=40,y=470)

#Most_Played frame
Most_played=Frame(root,bg="#1f1d1d",height=160,width=830)
Most_played.place(x=170,y=0)
Most_played_label=Label(Most_played,text="Most Played",font=("Georgia",11,"bold"),bg="#1f1d1d",fg="white")
Most_played_label.place(x=0,y=0)

#most played items
button_1=Button(Most_played,height=120,width=130,bd=0,command=button1)
button_1.place(x=6,y=30)

button_2=Button(Most_played,height=120,width=130,bd=0,command=button2)
button_2.place(x=162,y=30)

button_3=Button(Most_played,height=120,width=130,bd=0,command=button3)
button_3.place(x=317,y=30)

button_4=Button(Most_played,height=120,width=130,bd=0,command=button4)
button_4.place(x=472,y=30)

button_5=Button(Most_played,height=120,width=130,bd=0,command=button5)
button_5.place(x=627,y=30)

# calling function to change button images
most_played_images(0)
most_played_images(1)
most_played_images(2)
most_played_images(3)
most_played_images(4)

#frame for playlist
Playlist=Frame(root,bg="#272223",bd=0,height=400,width=480)
Playlist.place(x=170,y=160)

#frame for music image and name
Music=Frame(root,bg="#444141",height=417,width=350)
Music.place(x=650,y=160)

#album image
album_image=PhotoImage(file=".\\resources\\music.png")

#Frame for music album
album_label=Label(Music,bg="black",height="300",width="300",image=album_image)
album_label.place(x=25,y=20)

#label for title of the music
Track_title=Label(Music,text="Title : title not available",font=("Georgia",10),bg="#444141",fg="white",width=35)
Track_title.place(x=2,y=340)

#labell for artist name
Artist_name=Label(Music,bg="#444141",fg="white",font=("Georgia",10),text="Artist name not available",width=35)
Artist_name.place(x=2,y=364)

#To display heading
heading_playlist=Label(Playlist,bg="#272223",fg="white",text="< ----------  Tracks  ---------- >",font=("Georgia",11,BOLD))
heading_playlist.place(x=125,y=5)

#List of the  songs from system
list_of_tracks=Listbox(Playlist,font=("Georgia",12),bg="#343434",fg="white",width=39,height=14,border=0,selectbackground="red")
list_of_tracks.place(x=5,y=42)
list_of_tracks.bind("<<ListboxSelect>>",callback)

#bottom frame for controls
Controls=Frame(root,bg="#333333",height=40,width=1000)
Controls.place(x=0,y=560)

#image of play button
Photo_pause=PhotoImage(file=".\\resources\\play.png")
Photo_play=PhotoImage(file=".\\resources\\pause.png")
Photo_next=PhotoImage(file=".\\resources\\next.png")
Photo_previous=PhotoImage(file=".\\resources\\previous.png")

Photo_volume_up=PhotoImage(file=".\\resources\\volume_up.png")
Photo_volume_down=PhotoImage(file=".\\resources\\volume_down.png")

Photo_loop=PhotoImage(file=".\\resources\\loop.png")
Photo_suffle=PhotoImage(file=".\\resources\\suffle.png")
Photo_repeat_one=PhotoImage(file=".\\resources\\repeat_one.png")
Photo_red_heart=PhotoImage(file=".\\resources\\red_heart.png")
Photo_white_heart=PhotoImage(file=".\\resources\\white_heart.png")

#control buttons
play=Button(Controls,bg="#333333",fg="#333333",image=Photo_pause,border=0,activebackground="#293241",command=play)
play.place(x=160,y=4)
previous=Button(Controls,bg="#333333",fg="#333333",image=Photo_previous,border=0,activebackground="#293241",command=previous)
previous.place(x=110,y=4)
Next=Button(Controls,bg="#333333",fg="#333333",image=Photo_next,border=0,activebackground="#293241",command=next)
Next.place(x=210,y=4)

#volume buttons
Vol_up=Button(Controls,image=Photo_volume_up,bg="#333333",fg="#333333",text="vol UP",border=0,activebackground="#293241",command=volume_up)
Vol_up.place(x=960,y=4)
Vol_down=Button(Controls,image=Photo_volume_down,bg="#333333",fg="#333333",text="V -",border=0,activebackground="#293241",comman=volume_down)
Vol_down.place(x=920,y=4)

#volume percentage label
vol_label=Label(Controls,text="vol",font=("Georgia",12),bg="#343434",fg="white",border=0)
vol_label.place(x=875,y=6)

#label for timer
Time_view=Label(Controls,bg="#333333",fg="white",text="-:-",font=("Georgia",11),border=0,activebackground="#293241")
Time_view.place(x=260,y=6)

#Progressbar of song
s = ttk.Style()
s.theme_use('default')
s.configure("red.Horizontal.TProgressbar", foreground='red', background='red',thickness=4)
progress_bar=ttk.Progressbar(Controls, style="red.Horizontal.TProgressbar", orient="horizontal",
                length=400, mode="determinate", maximum=4)
progress_bar.place(x=310,y=15)

#progressbar modification
progress_bar.start()
progress_bar.stop()
progress_bar.bind('<B1-Motion>', motion)
progress_bar.config(variable=var)

#suffle and loop buttions
Music_Suffle=Button(Controls,image=Photo_loop,bg="#333333",fg="#333333",border=0,activebackground="#293241",comman=Suffle)
Music_Suffle.place(x=60,y=4)

#button to add favourite
favourite_heart=Button(Controls,image=Photo_white_heart,bg="#333333",fg="#333333",text="SUFF",border=0,activebackground="#293241",comman=add_favourite)
favourite_heart.place(x=780,y=6)

root.mainloop()