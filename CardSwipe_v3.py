from tkinter import *
from tkinter import messagebox
from winsound import *
from datetime import *
import os


exe_path = os.getcwd()
ico_file = 'MathCenter_tiny.ico' #Can be any logo you want here
successSound = 'Success.wav'
succSound_path = os.path.join(exe_path, successSound)

failSound = 'Failure.wav'
failSound_path = os.path.join(exe_path, failSound)

ico_path = os.path.join(exe_path, ico_file)


root = Tk()
root.title("CardSwipe")
root.geometry("300x200")
root['background']='#FFC222'
root.iconbitmap(ico_path)



SwipeFrame = Frame(root)
SwipeFrame.pack()

DisplayFrame = Frame(root)
DisplayFrame.pack()
dispBox = Text(DisplayFrame)
dispBox.pack()

entries = []
entryDict = dict()
insertList = []
studentNum = 1
docPath = os.getcwd()


entryLabel = Label(SwipeFrame,text='Please Swipe',bg='#6A4C92',fg='#FFFFFF')
entryLabel.pack()

e = Entry(SwipeFrame)
e.focus_set()
e.pack()

def entryFormat(IDnum):
    display = ''
    for a in entries:
        if a['ID Number'] == IDnum:
            if a['Time Out'] == '':
                display = str(a['Student Number'])+"\t\t "
                display += str(a['Time In'].strftime('%I:%M%p'))
            else:
                display = str(a['Student Number'])+"\t\t "
                display += str(a['Time In'].strftime('%I:%M%p'))+"\t  "
                display += str(a['Time Out'].strftime('%I:%M%p'))
    return display


#Insert the string in tBox at index of position
def insert_toText(theString,tBox,position):
    tBox.insert(float(position),theString+"\n")

#Headers for Text Box
insert_toText("Student Number \t Time In \t Time Out",dispBox,1)


#First delete text at position, then add the new text
def replace_toText(theString,tBox,position):
    tBox.delete(float(position),float(position+1))
    tBox.insert(float(position),theString+"\n")

#Checks if the ID number is already in our entries
def checkOut(IDnum):
    check=0 #assume false
    for a in entries:
        if a['ID Number'] == IDnum:
            check=1
    return check

#Makes a new entry
def entriesIn(studentNum,IDnum):
    theDict = {'Student Number':studentNum,
                                        'ID Number':IDnum,
                                        'Time In':datetime.now(),
                                        'Time Out':''
                            }
    entries.append(theDict)

def entriesOut(IDnum):
    for a in entries:
        if a['ID Number'] == IDnum:
            a['Time Out']=datetime.now()

def getStudentNum(IDnum):
    for a in entries:
        if a['ID Number'] == IDnum:
            return a['Student Number']

def insert_toWrite(IDnum):
    insertString = ''
    for a in entries:
        if a['ID Number'] == IDnum:
            insertString = tuple(a.values())
    insertList.append(insertString)

def remove(IDnum):
    i = 0
    for a in entries:
        if a['ID Number'] == IDnum:
            entries.pop(i)
        i+=1 

def enter_Data(IDNumber,stdNum):
    global studentNum
    #If checkInOut is false -> new entry insert a new line
    if checkOut(IDNumber)==0:
        entriesIn(stdNum,IDNumber) #The ID is not in entries, add a new entry record
        insert_toText(entryFormat(IDNumber),dispBox,stdNum+1)
        studentNum +=1
    else:
        num = getStudentNum(IDNumber)
        entriesOut(IDNumber) #update that entry with date time in time out
        replace_toText(entryFormat(IDNumber),dispBox,num+1) #replace with updated time out
        insert_toWrite(IDNumber)
        remove(IDNumber) #this ID is signing out, remove it from entries

    PlaySound(succSound_path,SND_FILENAME)
    e.delete(0,'end')

def Confirm_ID(IDNumber,wd,f,event=None):
    global studentNum
    global ID
    if IDNumber == ID:
        enter_Data(IDNumber,studentNum)
        wd.destroy()
    else:
        f.delete(0,'end') #clear the entry when wrong ID entered
        PlaySound(failSound_path,SND_FILENAME)




def func(event):
    global studentNum
    global ID
    IDNumber = e.get()
    ID = IDNumber
    ID_Len = len(IDNumber)

    if ID_Len>1 and ID_Len<7: #ID is between 2 and 6 then confirm
        Confirm = Toplevel()
        Confirm.title("Please Confirm")
        Confirm.geometry("300x200")
        Confirm['background']='#FFC222'
        Confirm.iconbitmap(ico_path)

        confirmLabel = Label(Confirm,text='Please Confirm Your ID',bg='#6A4C92',fg='#FFFFFF')
        confirmLabel.pack()

        f = Entry(Confirm)
        f.focus_set()
        f.pack()

        confirmButton = Button(Confirm,text="Confirm",command = lambda: Confirm_ID(IDNumber = f.get(),wd = Confirm, f = f))
        confirmButton.pack()

        #Need to update this
        Confirm.bind('<Return>',lambda x: Confirm_ID(f.get(),Confirm,f,x))

    if ID_Len == 7: #Most IDs are 7 digits
        enter_Data(IDNumber,studentNum)

    if ID_Len < 2:
        PlaySound(failSound_path,SND_FILENAME)
        e.delete(0,'end')

root.bind('<Return>', func)


def saveData():
    if entries is not [] and insertList is not []:
        path = docPath+"/CardSwipeData_"+datetime.now().strftime("%m%d%Y")+".csv"
        f = open(path,'a')
        if os.stat(path).st_size == 0:
            f.write("Student Number,ID Number,Time In,Time Out,Date"+"\n")
        
        #These are the students that swiped in and out
        f.write("\n".join([str(a[0])+
                        ","+str(a[1])+
                        ","+str(a[2].strftime('%I:%M%p'))+
                        ","+str(a[3].strftime('%I:%M%p'))+
                        ","+str(a[3].strftime('%x')) for a in insertList]))
        
        f.write("\n") #Need to update with a case if first line doesnt have a swipe out time
        #Add the students that didn't swipe out - entries only has students that didn't swipe out!
        f.write("\n".join([str(a['Student Number'])+
                        ","+str(a['ID Number'])+
                        ","+str(a['Time In'].strftime('%I:%M%p'))+
                        ",N/A"+
                        ","+str(a['Time In'].strftime('%x')) for a in entries]))
        
        f.close()
    else:
        print("No Swipes!")

def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        saveData()
        root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()
input()
