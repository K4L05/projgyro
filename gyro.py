"""
Title:      Project Gyro
Desc:       An OSC lighting controller for Chamsys MagicQ Lighting Consoles
Author:     Kalos Robinson-Frani
Email:      st20218@howick.school.nz
Date:       30/07/24

Version 1:
Basic GUI
Basic OSC transmission
Basic intensity functionality


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
PROGRAM_TITLE = "PROJ GYRO V1.0"
IP_ADDRESS = "192.168.0.69" # Needs to be a string
PORT = 8000 # Needs to be an interger

FIXTURES_LIST = { # Address > Friendly Name, Attributes > Intensity (true/false), Pantilt (true/false)
    "38": {
        "friendly_name": "EKSpot 1",
        "attributes": {
            "active": True,
            "intensity": True,
            "pantilt": True,
            "pan_range": (0,255),
            "tilt_range": (0,255)
        }
    },
    "39": {
        "friendly_name": "EKSpot 2",
        "attributes": {
            "active": True,
            "intensity": True,
            "pantilt": True,
            "pan_range": (0,255),
            "tilt_range": (0,255)
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
    osc_client = udp_client.SimpleUDPClient(IP_ADDRESS, PORT)
except:
    print("WARNING SOCKET ERROR")
    osc_client = udp_client.SimpleUDPClient("localhost", PORT)


def settings_wdw():
    settings_window = Toplevel()
    settings_window.geometry("800x400")
    Label(settings_window, text="Settings Menu").grid(row=0, column=0)
    settings_fixture_fme = LabelFrame(settings_window, text="Fixtures")

    # Fixture Frame
    settings_fixture_list_lb = Listbox(settings_fixture_fme)
    settings_fixture_list_lb.grid(row=0, column=0)

    settings_fixture_list_lb.insert(END, "300", "323") # FIXTURES
    settings_fixture_list_lb.bind("<<ListboxSelect>>", fixture_select)

    settings_fixture_fme.grid(row=1, column=0, padx=default_padding, pady=default_padding)

    settings_add_fixture_btn = Button(settings_window, text="Add")

    settings_add_fixture_btn
    

    


def show_values(value):
    print(value)

def fixture_select(event):
    selected_fixture = event.widget.get(event.widget.curselection())
    print(f"Fixture: {selected_fixture}")

    #osc_client.send_message(f"/rpc", "\<01>,{selected_fixture}H") # SENDS CLIENT MESSAGE
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
    ip_details_lbl = Label(connection_details_fme, text=IP_ADDRESS, justify="left")

    # Port
    port_title_lbl = Label(connection_details_fme, text="PORT:", justify="right")
    port_details_lbl = Label(connection_details_fme, text=PORT, justify="left")

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
    fixture_list_lb = Listbox(fixture_fme)
    fixture_list_lb.grid(row=5, column=1, columnspan=3)

    for item in FIXTURES_LIST:
        fixture_list_lb.insert(END, item) # FIXTURES

    fixture_fme.grid(row=3, column=0, columnspan=3, rowspan=5, padx=default_padding, pady=default_padding)
    fixture_list_lb.bind("<<ListboxSelect>>", fixture_select)


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





if initiate_gui == TRUE:
    root.mainloop()
