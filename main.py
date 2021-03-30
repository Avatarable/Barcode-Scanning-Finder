from tkinter import *
from tkinter import messagebox
import os, json

from win32api import GetSystemMetrics
from screeninfo import get_monitors


#====== define GUI variables ======
margin1, margin2, margin3, margin4 = 10, 20, 30, 40
marginList = 100
btn_lt_margin = 310
btn_vt_margin = 850

btnWidth, btnHeight = 100, 40
font = "Calibri"
size1, size2, size3 = 12, 14, 30

# gadget screen size
scr_height = GetSystemMetrics(0)
scr_width = GetSystemMetrics(1)
geometry = get_monitors()
geo_x = geometry[0].width
geo_y = geometry[0].height

color1 = '#A76D14'  # add
color2 = '#5FBB80'  # scan
color3 = '#A0447F'  # delete
color4 = '#305496'  # clear
color5 = '#181B28'  # dark bg
color6 = '#B2B3B7'  # border color
color7 = '#C75450'   # reset
mainColor = "#F0F0F0"

#====== Load Theme ==================
theme = ''
if os.path.isfile('theme.json'):
    with open('theme.json') as json_file:
        try:
            data = json.load(json_file)
            theme = data['theme']
        except:
            theme = 'light'

#====== define Logic variables ======
lostTotes_list = []
visiTotes_list = []
found_list = []
lost = 0
sighted = 0
found = 0
status = ""
lost_scan = True
barcode = ""


def reset():
    global lostTotes_list, visiTotes_list, lost, sighted, found
    confirm = messagebox.askyesno('Confirm', 'Remove all scanned totes?')
    if(confirm):
        listbox_lt.delete(0, END)
        listbox_vt.delete(0, END)
        lostTotes_list = []
        visiTotes_list = []
        lost, sighted, found = (0,0,0)
        val_lt.config(text=lost)
        val_sight.config(text=sighted)
        val_found.config(text=found)
        val_status.config(text='Reset completed!!')    # update status


def recheck():
    global found
    found = chk_found()
    indexes_lt = []
    indexes_vt = []
    if len(found)>0:
        for item in found:
            indexes_lt.append(lostTotes_list.index(item))       # get barcode index on lost tote list
            indexes_vt.append(visiTotes_list.index(item))       # get barcode index on visible tote list
        for index in indexes_lt:
            listbox_lt.selection_set(index)
    val_found.config(text=len(found))       # update found label
    val_status.config(text=f'Found {len(found)} totes!!')    # update status

def chk_found():
    found = []
    for item in lostTotes_list:
        chk = visiTotes_list.count(item)
        if chk>0:
            found.append(item)
    return found


def verify(list, listbox, barcode):
    global found
    root.update_idletasks()
    if list.count(barcode) > 0:
        val_status.config(text=f'Found {barcode} !!')
        listbox.selection_set(list.index(barcode))
        found_list = chk_found()
        found = len(found_list)
        val_found.config(text=found)


def get_code(e):
    global barcode
    if e.keycode!=13 or e.char!='\r':
        barcode = barcode + e.char

def add_code(event):
    global code, lost, sighted, barcode
    root.update_idletasks()
    if lost_scan == True:
        lostTotes_list.append(barcode)
        listbox_lt.insert(END, barcode)
        verify(visiTotes_list, listbox_vt, barcode)
        lost += 1
        val_lt.config(text=lost)
        if listbox_lt.size()>0:             # activate delete & clear buttons
            btn_delete_lt.config(state=NORMAL, cursor='hand2')
            btn_clear_lt.config(state=NORMAL, cursor='hand2')
    else:
        visiTotes_list.append(barcode)
        listbox_vt.insert(END, barcode)
        verify(lostTotes_list, listbox_lt, barcode)
        sighted += 1
        val_sight.config(text=sighted)

        if listbox_vt.size()>0:             # activate delete & clear buttons
            btn_delete_vt.config(state=NORMAL, cursor='hand2')
            btn_clear_vt.config(state=NORMAL, cursor='hand2')

    barcode = ""


def add_lt(e):
    global lost_scan
    lost_scan = True

    root.update_idletasks()
    disabledElements = [btn_delete_vt, btn_clear_vt]
    for element in disabledElements:
        element.config(state=DISABLED, cursor='X_cursor')
    val_status.config(text='Scanning lost totes...')

    if listbox_lt.size()>0:
        btn_delete_lt.config(state=NORMAL, cursor='hand2')
        btn_clear_lt.config(state=NORMAL, cursor='hand2')

def del_lostTotes():
    global lost
    items = listbox_lt.curselection()
    for item in items[::-1]:
        lostTotes_list.remove(listbox_lt.get(item))   #delete from lostTotes_list
        listbox_lt.delete(item)    #remove from listbox
        lost -= 1
        val_lt.config(text=lost)
    if listbox_lt.size()<1:             # de-activate delete & clear buttons
        btn_delete_lt.config(state=DISABLED, cursor='X_cursor')
        btn_clear_lt.config(state=DISABLED, cursor='X_cursor')

def clear_lt():
    global lostTotes_list, lost, found
    confirm = messagebox.askyesno('Confirm', 'Remove all lost totes?')
    if(confirm):
        listbox_lt.delete(0, END)
        lostTotes_list = []
        lost = 0
        found = 0
        val_lt.config(text=lost)
        val_found.config(text=found)

        btn_delete_lt.config(state=DISABLED, cursor='X_cursor')
        btn_clear_lt.config(state=DISABLED, cursor='X_cursor')


def add_vt(e):
    global lost_scan
    lost_scan = False

    root.update_idletasks()
    disabledElements = [btn_delete_lt, btn_clear_lt]
    for element in disabledElements:
        element.config(state=DISABLED, cursor='X_cursor')
    val_status.config(text='Scanning visible totes...')

    if listbox_vt.size()>0:
        btn_delete_vt.config(state=NORMAL, cursor='hand2')
        btn_clear_vt.config(state=NORMAL, cursor='hand2')


def del_visiTotes():
    global sighted
    items = listbox_vt.curselection()
    for item in items[::-1]:
        visiTotes_list.remove(listbox_vt.get(item))   #delete from lostTotes_list
        listbox_vt.delete(item)    #remove from listbox
        sighted -= 1
        val_sight.config(text=sighted)
    if listbox_vt.size()<1:             # de-activate delete & clear buttons
        btn_delete_vt.config(state=DISABLED, cursor='X_cursor')
        btn_clear_vt.config(state=DISABLED, cursor='X_cursor')

def clear_vt():
    global visiTotes_list, sighted, found
    confirm = messagebox.askyesno('Confirm', 'Remove all visible totes?')
    if(confirm):
        listbox_vt.delete(0, END)
        visiTotes_list = []
        sighted = 0
        found = 0
        val_sight.config(text=sighted)
        val_found.config(text=found)

        btn_delete_vt.config(state=DISABLED, cursor='X_cursor')
        btn_clear_vt.config(state=DISABLED, cursor='X_cursor')


# -------THEMES-----------------
def darken():
    root.config(bg=color5)
    frame_summary.config(bg=color5)
    section_frame.config(bg=color5)
    val_status.config(bg=color5)
    listbox_lt.config(bg=mainColor)
    listbox_vt.config(bg=mainColor)

    labels = [lbl_lt, val_lt, lbl_sight, val_sight, lbl_found, val_found, lbl_found, val_found, lbl_status, lbl_lt_desc, lbl_vt_desc]
    for label in labels:
        label.config(bg=color5, fg=mainColor)

    # save to json
    data = {'theme': 'darken'}
    if os.path.isfile('theme.json'):
        with open('theme.json', 'w') as file:
            json.dump(data, file)

def lighten():
    root.config(bg=mainColor)
    frame_summary.config(bg=mainColor)
    section_frame.config(bg=mainColor)
    val_status.config(bg=mainColor)
    listbox_lt.config(bg='white')
    listbox_vt.config(bg='white')

    labels = [lbl_lt, val_lt, lbl_sight, val_sight, lbl_found, val_found, lbl_found, val_found, lbl_status, lbl_lt_desc, lbl_vt_desc]
    for label in labels:
        label.config(bg=mainColor, fg='black')

    # save to json
    data = {'theme': 'lighten'}
    if os.path.isfile('theme.json'):
        with open('theme.json', 'w') as file:
            json.dump(data, file)
# -------------------------------


def menu_bar():
    menubar = Menu(root)
    filemenu = Menu(menubar, tearoff=0)
    filemenu.add_command(label="New")
    filemenu.add_command(label="Open")
    filemenu.add_command(label="Save")
    filemenu.add_command(label="Save as...")
    filemenu.add_separator()
    filemenu.add_command(label="Exit", command=root.quit)
    menubar.add_cascade(label="File", menu=filemenu)
    thememenu = Menu(menubar, tearoff=0)
    thememenu.add_command(label="Light", command=lighten)
    thememenu.add_command(label="Dark", command=darken)
    menubar.add_cascade(label="Theme", menu=thememenu)
    helpmenu = Menu(menubar, tearoff=0)
    helpmenu.add_command(label="Help Index")
    helpmenu.add_command(label="About...")
    menubar.add_cascade(label="Help", menu=helpmenu)
    return menubar



def mainScreen():
    global root
    global frame_summary, section_frame, listbox_lt, listbox_vt
    global lbl_lt, val_lt, lbl_sight, val_sight, lbl_found, val_found, lbl_status, val_status, lbl_lt_desc, lbl_vt_desc
    global btn_add_lt, btn_delete_lt, btn_clear_lt, btn_rescan_lt, btn_add_vt, btn_delete_vt, btn_clear_vt, btn_reset_vt

    root = Tk()
    root.title("Tote Barcode Finder")
    root.geometry("1010x560")
    # root.geometry(f"{scr_height}x{scr_width}")

    root.resizable(False, False)
    menu = menu_bar()
    root.config(menu=menu, bg=mainColor)

    frame_summary = Frame(root, bg=None, border=3, highlightbackground=color6, highlightcolor=color6, highlightthickness=2, bd=0)
    frame_summary.place(x=margin3, y=margin1, width=950, height=50)
    lbl_lt = Label(frame_summary, text='Lost Totes: ', font=(font, size1, 'bold'))
    lbl_lt.place(x=margin2, y=margin1)
    val_lt = Label(frame_summary, text=lost, font=(font, size1, 'bold'))
    val_lt.place(x=margin2+80, y=margin1)
    lbl_sight = Label(frame_summary, text='Sighted Totes: ', font=(font, size1, 'bold'), bg=None)
    lbl_sight.place(x=margin2+200, y=margin1)
    val_sight = Label(frame_summary, text=sighted, font=(font, size1, 'bold'), bg=None)
    val_sight.place(x=margin2+300, y=margin1)
    lbl_found = Label(frame_summary, text='Found: ', font=(font, size1, 'bold'), bg=None)
    lbl_found.place(x=margin2+450, y=margin1)
    val_found = Label(frame_summary, text=found, font=(font, size1, 'bold'), bg=None)
    val_found.place(x=margin2+500, y=margin1)
    lbl_status = Label(frame_summary, text='Status: ', font=(font, size1, 'bold'), bg=None)
    lbl_status.place(x=margin2+620, y=margin1)
    val_status = Label(frame_summary, text='Scanning lost totes...', fg=color2, font=(font, size2, 'bold'), bg=None)
    val_status.place(x=margin2+680, y=7)

# ========================== SECTION ================================================================================
    section_frame = Frame(root)
    section_frame.place(x=margin3, y=70, width=950, height=470)

    # ============================ Lost Totes Section ==================================
    lbl_lt_desc = Label(section_frame, text='Scan in Lost Totes: ', font=(font, size1), bg=None)
    lbl_lt_desc.place(x=0, y=margin2)

    scroll_lt = Scrollbar(section_frame, bg=mainColor)
    scroll_lt.place(x=280, y=50, height=400)
    listbox_lt = Listbox(section_frame, bg='#fcfcfc', cursor='hand2', relief='sunken', font=(font, size1), selectmode=SINGLE, yscrollcommand=scroll_lt.set)
    listbox_lt.place(x=0, y=50, width=280, height=400)
    scroll_lt.config(command=listbox_lt.yview)
    listbox_lt.bind('<Button-1>', add_lt)

    btn_add_lt = Button(section_frame, text='Add', bg=color1, cursor='hand2', font=(font, size1))
    btn_add_lt.place(x=btn_lt_margin, y=50, width=btnWidth, height=btnHeight)
    btn_add_lt.bind('<Button-1>', add_lt)
    btn_delete_lt = Button(section_frame, text='Delete', bg=color3, cursor='X_cursor', font=(font, size1), state=DISABLED, command=del_lostTotes)
    btn_delete_lt.place(x=btn_lt_margin, y=100, width=btnWidth, height=btnHeight)
    btn_clear_lt = Button(section_frame, text='Clear', bg=color4, cursor='X_cursor', font=(font, size1), state=DISABLED, command=clear_lt)
    btn_clear_lt.place(x=btn_lt_margin, y=150, width=btnWidth, height=btnHeight)
    btn_recheck = Button(section_frame, text='Recheck', bg=color2, cursor='hand2', font=(font, size1), state=NORMAL, command=recheck)
    btn_recheck.place(x=btn_lt_margin, y=410, width=btnWidth, height=btnHeight)

    if listbox_lt.size()>0:
        btn_delete_lt.config(state=NORMAL, cursor='hand2')

    # ============================= Visible Totes Section =====================================
    lbl_vt_desc = Label(section_frame, text='Scan in Totes in sight: ', font=(font, size1), bg=None)
    lbl_vt_desc.place(x=540, y=margin2)

    scroll_vt = Scrollbar(section_frame, bg=mainColor)
    scroll_vt.place(x=820, y=50, height=400)
    listbox_vt = Listbox(section_frame, bg='#fcfcfc', border=1, cursor='hand2', relief='sunken', font=(font, size1), selectmode=SINGLE, yscrollcommand=scroll_vt.set)
    listbox_vt.place(x=540, y=50, width=280, height=400)
    scroll_vt.config(command=listbox_vt.yview)
    listbox_vt.bind('<Button-1>', add_vt)

    btn_add_vt = Button(section_frame, text='Add', bg=color1, cursor='hand2', font=(font, size1))
    btn_add_vt.place(x=btn_vt_margin, y=50, width=btnWidth, height=btnHeight)
    btn_add_vt.bind('<Button-1>', add_vt)
    btn_delete_vt = Button(section_frame, text='Delete', bg=color3, cursor='X_cursor', font=(font, size1), state=DISABLED, command=del_visiTotes)
    btn_delete_vt.place(x=btn_vt_margin, y=100, width=btnWidth, height=btnHeight)
    btn_clear_vt = Button(section_frame, text='Clear', bg=color4, cursor='X_cursor', font=(font, size1), state=DISABLED, command=clear_vt)
    btn_clear_vt.place(x=btn_vt_margin, y=150, width=btnWidth, height=btnHeight)
    btn_reset_vt = Button(section_frame, text='Reset', bg=color7, cursor='hand2', font=(font, size1), command=reset)
    btn_reset_vt.place(x=btn_vt_margin, y=410, width=btnWidth, height=btnHeight)

    # ------- Apply theme --------
    if theme == 'darken':
        darken()
    else:
        lighten()
    # -----------------------------

    root.bind('<Return>', add_code)
    root.bind('<Key>', get_code)
    root.mainloop()


if __name__ == '__main__':
    mainScreen()

