"""
Title:      Project Gyro
Desc:       An OSC lighting controller for Chamsys MagicQ Lighting Consoles
Author:     Kalos Robinson-Frani
Email:      st20218@howick.school.nz
Date:       05/08/24

Version 2:
Further Developed GUI
Settings Page

Required Dependencies:
python-osc
"""

# Import Required Dependencies
from tkinter import *; from PIL import Image, ImageTk; from tkinter import ttk
from pythonosc import udp_client
import datetime

initiate_gui = TRUE
default_padding = 10



# Constant Variables
PROGRAM_TITLE = "PROJ GYRO V2.0"

ip_address = "192.168.0.69" # Needs to be a string
port = 8000 # Needs to be an interger

FIXTURES_LIST = { 
    # Address > Friendly Name, Attributes > Intensity (true/false), Pantilt (true/false), PanTilt_Details > pan_range, default_pan, tilt_range, default_tilt.
    "38": {
        "friendly_name": "EKSpot 1",
        "attributes": {
            "active": True,
            "intensity": True,
            "pantilt": True,
            "pantilt_details": {
                "pan_range": (0,255),
                "def_pan": 0,
                "tilt_range": (0,255),
                "def_tilt": 0
            }
        }
    },
    "39": {
        "friendly_name": "EKSpot 2",
        "attributes": {
            "active": True,
            "intensity": True,
            "pantilt": True,
            "pantilt_details": {
                "pan_range": (0,255),
                "default_pan": 0,
                "tilt_range": (0,255),
                "default_tilt": 0
            }
            
        }
    }
}

"""class Fixture:
    def __init__(self, address, colour, position) -> None:
        self.address = address
        self.intensity = True
        self.colour = colour
        self.position = position

        self.cmd_select = 1 # Select one or more heads
        self.cmd_deselect = 2 # Deselect one or more heads
        self.cmd_deselect_all = 3 # Deselect all Heads
        self.cmd_select_group = 4 # Select Group
        self.cmd_intensity = 5 # Set intensity of selected head
        self.cmd_attribute = 6 # Set Attribute ! Important
        self.cmd_increase_attribute = 7 # Increase attribute value
        self.cmd_decrease_attribute = 8 # Decrease attribute value
        self.cmd_clear = 9 # Clear

        self.cmd_incl_pos_pal = 10 # Include position palette
        self.cmd_incl_col_pal = 11 # Include colour palette
        self.cmd_incl_beam_pal = 12 # Include beam palette
        self.cmd_incl_cue = 13 # Include cue
        self.cmd_update = 14 # Update
        
            
        pass


    def select():
        """




    #def select(head):
        #client.send_message("/rpc", "\<01>,0,1H")


try:
    osc_client = udp_client.SimpleUDPClient(ip_address, port)
except:
    print("WARNING SOCKET ERROR")
    osc_client = udp_client.SimpleUDPClient("localhost", port)


def confirm_fixture():
    new_fixture = new_fix_var.get()
    FIXTURES_LIST[new_fixture] = {
        "friendly_name": "",
        "attributes": {
            "active": False,
            "intensity": False,
            "pantilt": True,
            "pantilt_details": {
                "pan_range": (),
                "default_pan": None,
                "tilt_range": (),
                "default_tilt": None
            }
            
        }
    }

    # FIXTURE ADD
    for item in FIXTURES_LIST:
        listbox_item = (item, FIXTURES_LIST[item]["friendly_name"])
        if listbox_item not in settings_fixture_list_lb.get(0, END):
            settings_fixture_list_lb.insert(END, (listbox_item))
            fixture_list_lb.insert(END, (listbox_item))

        

    add_new_fixture_window.destroy()


def add_new_fixture():
    global add_new_fixture_window
    add_new_fixture_window = Toplevel()
    add_new_fixture_fme = LabelFrame(add_new_fixture_window, text="Add new fixture address")
    new_fixture_ety = Entry(add_new_fixture_fme, textvariable = new_fix_var)

    fixture_add_img = ImageTk.PhotoImage(Image.open('resources/check.png').resize((25, 25)))
    fixture_add_btn = Button(add_new_fixture_fme, image = fixture_add_img, text="Confirm", command=confirm_fixture)
    fixture_add_btn.image = fixture_add_img
    fixture_add_btn.grid(row=0, column=1)

    add_new_fixture_fme.grid(row=0, column=0, padx=default_padding*2, pady=default_padding*2)
    new_fixture_ety.grid(row=0, column=0)

def confirm_conn_details():
    ip_address = ip_address_var.get()
    print("New IP: ", ip_address)

    port = port_var.get()
    print("New Port: ", port)

    edit_conn_details_window.destroy()


def edit_conn_details():
    global edit_conn_details_window
    edit_conn_details_window = Toplevel()
    
    edit_conn_details_fme = LabelFrame(edit_conn_details_window, text="Edit Connection Details")

    edit_ipaddress_lbl = Label(edit_conn_details_fme, text="IP:")
    edit_ipaddress_ety = Entry(edit_conn_details_fme, textvariable=ip_address_var)

    edit_port_lbl = Label(edit_conn_details_fme, text="Port:")
    edit_port_ety = Entry(edit_conn_details_fme, textvariable=port_var)

    
    conn_details_confirm_img = ImageTk.PhotoImage(Image.open('resources/check.png').resize((50, 50)))
    conn_details_confirm_btn = Button(edit_conn_details_fme, image = conn_details_confirm_img, text="Confirm", command=confirm_conn_details)
    conn_details_confirm_btn.image = conn_details_confirm_img
    conn_details_confirm_btn.grid(row=0, column=3, rowspan=2)

    edit_ipaddress_lbl.grid(row=0, column=0)
    edit_ipaddress_ety.grid(row=0, column=1)
    edit_port_lbl.grid(row=1, column=0)
    edit_port_ety.grid(row=1, column=1)



    edit_conn_details_fme.grid(row=0, column=0, padx=default_padding*2, pady=default_padding*2)
    
    

def settings_fixture_select(fixture):
    # For future implementation
    pass

def settings_wdw():
    global settings_fixture_list_lb
    ip_address_var.set(ip_address)
    port_var.set(port)



    settings_window = Toplevel()
    settings_window.title("Settings")

    Label(settings_window, text="Settings Menu").grid(row=0, column=0, padx=default_padding, pady=default_padding)
    settings_fixture_fme = LabelFrame(settings_window, text="Fixtures")

    # Fixture Frame
    settings_fixture_list_lb = Listbox(settings_fixture_fme)
    settings_fixture_list_lb.grid(row=0, column=0)

    for item in FIXTURES_LIST:
        settings_fixture_list_lb.insert(END, (item, FIXTURES_LIST[item]["friendly_name"])) # FIXTURES
    
    settings_fixture_list_lb.bind("<<ListboxSelect>>", settings_fixture_select)

    settings_fixture_fme.grid(row=0, column=2, rowspan=3, padx=default_padding, pady=default_padding)

    settings_add_img = ImageTk.PhotoImage(Image.open('resources/add.jpg').resize((25, 25)))
    settings_add_btn = Button(settings_fixture_fme, image = settings_add_img, text="Add", command=add_new_fixture)
    settings_add_btn.image = settings_add_img
    settings_add_btn.grid(row=1, column=0)
    
    settings_connection_fme = LabelFrame(settings_window, text="Connection Details")

    settings_ipaddress_lbl = Label(settings_connection_fme, text="IP:")
    settings_ipaddress_ety = Entry(settings_connection_fme, textvariable=ip_address_var, state=DISABLED)

    settings_port_lbl = Label(settings_connection_fme, text="Port:")
    settings_port_ety = Entry(settings_connection_fme, textvariable=port_var, state=DISABLED)

    conn_details_edit_img = ImageTk.PhotoImage(Image.open('resources/edit.jpg').resize((25, 25)))
    conn_details_edit_btn = Button(settings_connection_fme, image = conn_details_edit_img, text="Edit", command=edit_conn_details)
    conn_details_edit_btn.image = conn_details_edit_img
    conn_details_edit_btn.grid(row=0, column=2, rowspan=2, padx=default_padding, pady=default_padding)


    settings_ipaddress_lbl.grid(row=0, column=0)
    settings_ipaddress_ety.grid(row=0, column=1)
    settings_port_lbl.grid(row=1, column=0)
    settings_port_ety.grid(row=1, column=1)



    settings_connection_fme.grid(row=0, column=0, columnspan=2, padx=default_padding, pady=default_padding)

def show_values(value):
    print(value)

def fixture_select(event):
    selected_fixture = event.widget.get(event.widget.curselection())[0]
    print(f"Fixture: {selected_fixture}")

    
    fixture_selection_lbl.config(text="> {} - {}".format(selected_fixture, FIXTURES_LIST[selected_fixture]["friendly_name"]))

    osc_client.send_message(f"/rpc", "\<01>,{}H".format(str(selected_fixture))) # SENDS CLIENT MESSAGE


    console_lb.insert(END, (f"<{(datetime.datetime.now()).strftime('%H:%M:%S')}> Selected Fixture {selected_fixture}"))
    console_lb.yview(END)


def intensity_update(event):
    intensity=event
    print(f"Intensity: {intensity}")
    osc_client.send_message("/rpc", "\<05>,{}H".format(str(intensity)))

def pan_update(event):
    pan = event
    print(f"Pan: {pan}")
    osc_client.send_message("/rpc", "\<06>,4,{}H".format(pan))

def tilt_update(event):
    tilt = event
    print(f"Tilt: {tilt}")
    osc_client.send_message("/rpc", "\<06>,5,{}H".format(tilt))


if initiate_gui == TRUE:
    root = Tk()
    root.title("Project GYRO")

    # SETTINGS
    settings_fme = Frame(root)
    settings_img = ImageTk.PhotoImage(Image.open('resources\settings.png').resize((50, 50)))
    settings_btn = Button(settings_fme, image = settings_img, text="Settings", command=settings_wdw)
    settings_btn.image = settings_img
    settings_btn.grid(row=0, column=0, rowspan=2)
    settings_fme.grid(column=0, row=0, rowspan=2, columnspan=2, padx=default_padding, pady=default_padding)

    # CONNECTION DETAILS
    # IP Address
    connection_details_fme = LabelFrame(root, text="Connection Details")
    ip_title_lbl = Label(connection_details_fme, text="IP:", justify="right", width=2)
    ip_details_lbl = Label(connection_details_fme, text=ip_address, justify="left")

    # Port
    port_title_lbl = Label(connection_details_fme, text="PORT:", justify="right")
    port_details_lbl = Label(connection_details_fme, text=port, justify="left")

    # Griddy
    ip_title_lbl.grid(row=0, column=0)
    ip_details_lbl.grid(row=0, column=1)

    port_title_lbl.grid(row=1, column=0)
    port_details_lbl.grid(row=1, column=1)

    connection_details_fme.grid(row=0, column=2, columnspan=2, rowspan=2, padx=5, pady=2)


    # Console Frame
    console_fme = LabelFrame(root, text="Console")
    console_lb = Listbox(console_fme, height=3, width=60)

    console_lb.insert(END)

    console_fme.grid(row=0, column=4, columnspan=4, rowspan=2)
    console_lb.grid(row=0, column=0, columnspan=4, rowspan=2)

    # Program Title
    program_title_lbl = Label(root, text=PROGRAM_TITLE).grid(row=1, column=8, padx=default_padding, pady=default_padding)

    # Fixture Frame
    fixture_fme = LabelFrame(root, text="Fixtures")

    global fixture_list_lb

    fixture_list_lb = Listbox(fixture_fme, width=30)
    fixture_list_lb.grid(row=5, column=1, columnspan=3, padx=10)

    for item in FIXTURES_LIST:
        fixture_list_lb.insert(END, (item, FIXTURES_LIST[item]["friendly_name"])) # FIXTURES

    fixture_fme.grid(row=3, column=0, columnspan=3, rowspan=5, padx=default_padding, pady=default_padding)
    fixture_list_lb.bind("<<ListboxSelect>>", fixture_select)

    # Fixture Selection Label
    fixture_selection_lbl = Label(fixture_fme, text="No Fixture Selected", font="24", width=15)
    fixture_selection_lbl.grid(row=1, column=2, padx=default_padding, pady=default_padding)

    attributes_fme = LabelFrame(root, text="Controller")
    intensity_fme = LabelFrame(attributes_fme, text="Intensity")
    intensity_sdr = Scale(intensity_fme, from_=0, to=100, orient=HORIZONTAL, length=200, command=intensity_update)
    intensity_sdr.grid(row=0, column=0)
    intensity_fme.grid(row=0, column=0)

    pantilt_fme = LabelFrame(attributes_fme, text="Pan/Tilt")
    pan_sdr = Scale(pantilt_fme, from_=0, to=100, orient=HORIZONTAL, length=200, command=pan_update).grid(row=0, column=0)
    tilt_sdr = Scale(pantilt_fme, from_=0, to=100, orient=VERTICAL, length=200, command=tilt_update).grid(row=0, column=1)

    pantilt_fme.grid(row=0, column=2)

    attributes_fme.grid(row=4, column=3, rowspan=5, columnspan=5, padx=default_padding, pady=default_padding)


new_fix_var = StringVar()
ip_address_var = StringVar()
port_var = StringVar()

if initiate_gui == TRUE:
    root.mainloop()
