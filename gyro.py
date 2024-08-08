"""
Title:      Project Gyro
Desc:       An OSC lighting controller for Chamsys MagicQ Lighting Consoles
Author:     Kalos Robinson-Frani
Email:      st20218@howick.school.nz
Date:       09/08/24

Version 4:
Major Process Change
Object Oriented Fixtures

Required Dependencies:
python-osc
"""

# Import Required Dependencies
from tkinter import *; from PIL import Image, ImageTk; from tkinter import filedialog
from pythonosc import udp_client
import datetime

import json

initiate_gui = TRUE
default_padding = 10



# Constant Variables
PROGRAM_TITLE = "PROJ GYRO\nV3.2"

ip_address = "localhost" # Needs to be a string
port = "0000" # Needs to be an interger

fixtures = []

class LightFixture:
    def __init__(self, 
                 address, 
                 friendly_name="New Fixture", 
                 att_active=False, 
                 att_intensity=False, 
                 att_colour=False,  # For Future Versions
                 att_pantilt=False,

                 current_intensity=0,
                 current_colour=0, # For Future Versions

                 #current_pantilt=(0,0), Deprecated
                 current_pan=0,
                 current_tilt=0,

                 default_pantilt=(50,50), # For Future Versions
                 pan_range=(0,255), # For Future Versions
                 tilt_range=(0,255) # For Future Versions


                 ):
        self.address = address
        self.friendly_name = friendly_name

        self.att_active = att_active
        self.att_intensity = att_intensity
        self.att_colour = att_colour
        self.att_pantilt = att_pantilt

        self.current_intensity = current_intensity
        self.current_colour = current_colour
        self.current_pan = current_pan
        self.current_tilt = current_tilt

        self.default_pantilt = default_pantilt
        self.pan_range = pan_range
        self.tilt_range = tilt_range

"""
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
"""

# Initiates / Reinitiates the OSC Object
def init_osc(): 
    global osc_client, ip_address, port

    try:
        osc_client = udp_client.SimpleUDPClient(ip_address, int(port))
    except:
        print("WARNING SOCKET ERROR")
        osc_client = udp_client.SimpleUDPClient("localhost", 8000)

def console_log(data):
    package = "<{}> {}".format((datetime.datetime.now().strftime('%H:%M:%S')), data)
    console_lb.insert(END, package)
    console_lb.yview(END)

def reload_settings():
    settings_fixture_list_lb.delete(0,END)

    for fixture in fixtures:
        settings_fixture_list_lb.insert(END, (fixture.address, fixture.friendly_name))

    settings_ipaddress_detail_lbl.config(text=ip_address)
    settings_port_detail_lbl.config(text=ip_address)

def reload_main():
    init_osc()

    ip_details_lbl.config(text=ip_address)
    port_details_lbl.config(text=port)

    fixture_list_lb.delete(0, END)

    for fixture in fixtures:
        if fixture.att_active:
            fixture_list_lb.insert(END, (fixture.address, fixture.friendly_name)) # FIXTURES



    console_log("Updated Main")

# The genius thing that locates fixture 
def specify_fixture(address):
    for fixture in fixtures:
        if fixture.address == address:
            return fixture
    return None

def confirm_fixture():
    global fixtures
    new_fixture_address = None
    new_fixture_address = new_fixture_var.get()

    fixture = LightFixture(new_fixture_address)
    
    fixtures.append(fixture)
    
    for fixture in fixtures:
        print(fixture)

    # FIXTURE ADD
    for fixture in fixtures:
        listbox_item = (fixture.address, fixture.friendly_name)
        if listbox_item not in settings_fixture_list_lb.get(0, END):
            settings_fixture_list_lb.insert(END, (listbox_item))

        

    add_new_fixture_window.destroy()

def add_new_fixture():
    global add_new_fixture_window
    add_new_fixture_window = Toplevel()
    add_new_fixture_fme = LabelFrame(add_new_fixture_window, text="Add new fixture address")
    new_fixture_ety = Entry(add_new_fixture_fme, textvariable = new_fixture_var)

    fixture_add_img = ImageTk.PhotoImage(Image.open('resources/check.png').resize((25, 25)))
    fixture_add_btn = Button(add_new_fixture_fme, image = fixture_add_img, text="Confirm", command=confirm_fixture)
    fixture_add_btn.image = fixture_add_img
    fixture_add_btn.grid(row=0, column=1)

    add_new_fixture_fme.grid(row=0, column=0, padx=default_padding*2, pady=default_padding*2)
    new_fixture_ety.grid(row=0, column=0)

def confirm_conn_details():
    global ip_address, port

    print("DEBUGGING", ip_address_var.get(), port_var.get())

    ip_address = ip_address_var.get()
    print("New IP: ", ip_address)

    port = port_var.get()
    print("New Port: ", port)

    settings_ipaddress_detail_lbl.config(text=ip_address)
    settings_port_detail_lbl.config(text=port)




    edit_conn_details_window.destroy()

def confirm_edit_friendly_name():
    new_friendly_name = new_friendly_name_var.get()
    print(new_friendly_name)

    settings_fixture.friendly_name = new_friendly_name

    reload_settings()

    settings_edit_friendly_name_window.destroy()

def edit_conn_details():
    global edit_conn_details_window, ip_address, port, ip_address_var, port_var


    edit_conn_details_window = Toplevel()
    
    edit_conn_details_fme = LabelFrame(edit_conn_details_window, text="Edit Connection Details")

    edit_ipaddress_lbl = Label(edit_conn_details_fme, text="IP:")
    edit_ipaddress_ety = Entry(edit_conn_details_fme, text=ip_address_var)

    edit_port_lbl = Label(edit_conn_details_fme, text="Port:")
    edit_port_ety = Entry(edit_conn_details_fme, text=port_var)

    
    conn_details_confirm_img = ImageTk.PhotoImage(Image.open('resources/check.png').resize((50, 50)))
    conn_details_confirm_btn = Button(edit_conn_details_fme, image = conn_details_confirm_img, text="Confirm", command=confirm_conn_details)
    conn_details_confirm_btn.image = conn_details_confirm_img
    conn_details_confirm_btn.grid(row=0, column=3, rowspan=2)

    edit_ipaddress_lbl.grid(row=0, column=0)
    edit_ipaddress_ety.grid(row=0, column=1)
    edit_port_lbl.grid(row=1, column=0)
    edit_port_ety.grid(row=1, column=1)



    edit_conn_details_fme.grid(row=0, column=0, padx=default_padding*2, pady=default_padding*2)
      
def settings_edit_friendly_name():
    global settings_edit_friendly_name_window
    settings_edit_friendly_name_window = Toplevel()

    edit_friendly_name_fme= LabelFrame(settings_edit_friendly_name_window, text="Edit Friendly Name")
    edit_friendly_name_ety = Entry(edit_friendly_name_fme, textvariable = new_friendly_name_var)

    edit_friendly_name_img = ImageTk.PhotoImage(Image.open('resources/check.png').resize((25, 25)))
    edit_friendly_name_confirm_btn = Button(edit_friendly_name_fme, image = edit_friendly_name_img, text="Confirm", command=confirm_edit_friendly_name)
    edit_friendly_name_confirm_btn.image = edit_friendly_name_img
    edit_friendly_name_confirm_btn.grid(row=0, column=1)

    edit_friendly_name_fme.grid(row=0, column=0, padx=default_padding*2, pady=default_padding*2)
    edit_friendly_name_ety.grid(row=0, column=0)

def settings_fixture_select(selection):
    global settings_fixture

    selected_fixture = selection.widget.get(selection.widget.curselection())[0]
    print(f"DEBUG?: {selected_fixture}")

    settings_fixture = specify_fixture(selected_fixture)



    settings_fixture_selected_lbl.config(text="> {} - {}".format(selected_fixture, settings_fixture.friendly_name))

    settings_fixture_attribute_friendly_name_lbl.config(text=settings_fixture.friendly_name)

    settings_fixture_attribute_friendly_name_edit_btn.config(state="active")

    settings_fixture_attribute_active_cbx.config(state="active")
    att_active_var.set(settings_fixture.att_active)

    settings_fixture_attribute_intensity_cbx.config(state="active")
    att_intensity_var.set(settings_fixture.att_intensity)

    settings_fixture_attribute_colour_cbx.config(state="active")
    att_colour_var.set(settings_fixture.att_colour)


    settings_fixture_attribute_pantilt_cbx.config(state="active")
    att_pantilt_var.set(settings_fixture.att_pantilt)

def fixture_attribute_active():
    settings_fixture.att_active = att_active_var.get()

def fixture_attribute_intensity():
    settings_fixture.att_intensity = att_intensity_var.get()

def fixture_attribute_colour():
    settings_fixture.att_colour = att_colour_var.get()
    
def fixture_attribute_pantilt():
    settings_fixture.att_pantilt = att_pantilt_var.get()

def accept_settings():
    print("Accept Settings")
    settings_window.destroy()
    reload_main()
    pass

def save_settings():
    print("Save Settings")

    snapshot = {
        "connection": {
            "ip": ip_address,
            "port": port,
        },
        "fixtures": {}
    }

    for fixture in fixtures:
        fixture_line = [fixture.friendly_name, fixture.att_active, fixture.att_intensity, fixture.att_colour, fixture.att_pantilt, fixture.current_intensity, fixture.current_colour, fixture.current_pan, fixture.current_tilt, fixture.default_pantilt, fixture.pan_range, fixture.tilt_range]

        snapshot["fixtures"][fixture.address] = fixture_line

    

    file_save_dialog = filedialog.asksaveasfilename(initialfile='gyro_config.json', defaultextension=".json")
    
    with open(file_save_dialog, 'w') as file_save:
        json.dump(snapshot, file_save, ensure_ascii=False, indent=4)

def import_settings():
    global ip_address, port, fixtures

    print("Import Settings")


    file_load_dialog = filedialog.askopenfilename(title="Select a File", filetypes=[("JSON Config files", "*.json"), ("All files", "*.*")])
    
    if file_load_dialog:
        settings_window.attributes('-topmost', True)
        with open(file_load_dialog, 'r') as file_load:
            load_snapshot = json.load(file_load)

            ip_address = load_snapshot['connection']['ip']
            port = load_snapshot['connection']['port']

            for fixture_data in load_snapshot['fixtures']:
                fixture = LightFixture(fixture_data, load_snapshot['fixtures'][fixture_data][0],load_snapshot['fixtures'][fixture_data][1],load_snapshot['fixtures'][fixture_data][2],load_snapshot['fixtures'][fixture_data][3],load_snapshot['fixtures'][fixture_data][4],load_snapshot['fixtures'][fixture_data][5],load_snapshot['fixtures'][fixture_data][6],load_snapshot['fixtures'][fixture_data][7],load_snapshot['fixtures'][fixture_data][8],load_snapshot['fixtures'][fixture_data][9],load_snapshot['fixtures'][fixture_data][10],load_snapshot['fixtures'][fixture_data][11])
                fixtures.append(fixture)

        reload_settings()


# Settings Window
def settings_wdw():
    global settings_window, settings_fixture_list_lb, ip_address, port


    settings_window = Toplevel()
    settings_window.title("Settings")

    Label(settings_window, text="Settings Menu").grid(row=0, column=0, padx=default_padding, pady=default_padding)
    settings_fixture_fme = LabelFrame(settings_window, text="Fixtures")

    control_fme = Frame(settings_window)

    # Accept Settings
    settings_accept_img = ImageTk.PhotoImage(Image.open('resources/check.png').resize((25, 25)))
    settings_accept_btn = Button(control_fme, image = settings_accept_img, text="Accept Settings", command=accept_settings, compound="left", width=180, anchor=N)
    settings_accept_btn.image = settings_accept_img
    settings_accept_btn.grid(row=1, column=0)

    # Save Changes
    settings_save_img = ImageTk.PhotoImage(Image.open('resources/save.jpg').resize((25, 25)))
    settings_save_btn = Button(control_fme, image = settings_save_img, text="Save Settings", command=save_settings, compound="left", width=180, anchor=N)
    settings_save_btn.image = settings_save_img
    settings_save_btn.grid(row=2, column=0)

    # Import 
    settings_save_img = ImageTk.PhotoImage(Image.open('resources/import.png').resize((25, 25)))
    settings_save_btn = Button(control_fme, image = settings_save_img, text="Import Settings", command=import_settings, compound="left", width=180, anchor=N)
    settings_save_btn.image = settings_save_img
    settings_save_btn.grid(row=3, column=0)

    control_fme.grid(column=0, row=1, rowspan=4, padx=default_padding)

    # Fixture Frame
    settings_fixture_list_lb = Listbox(settings_fixture_fme)
    settings_fixture_list_lb.grid(row=0, column=0, rowspan=2)

    for fixture in fixtures:
        settings_fixture_list_lb.insert(END, (fixture.address, fixture.friendly_name)) # FIXTURES
    
    settings_fixture_list_lb.bind("<<ListboxSelect>>", settings_fixture_select)

    settings_fixture_fme.grid(row=0, column=2, rowspan=5, padx=default_padding, pady=default_padding)

    settings_add_img = ImageTk.PhotoImage(Image.open('resources/add.jpg').resize((25, 25)))
    settings_add_btn = Button(settings_fixture_fme, image = settings_add_img, text="Add New Fixture", command=add_new_fixture, compound="left")
    settings_add_btn.image = settings_add_img
    settings_add_btn.grid(row=3, column=0)
    
    settings_connection_fme = LabelFrame(settings_window, text="Connection Details")

    global settings_ipaddress_detail_lbl, settings_port_detail_lbl

    settings_ipaddress_lbl = Label(settings_connection_fme, text="IP:")
    settings_ipaddress_detail_lbl = Label(settings_connection_fme, text=ip_address, state=DISABLED)

    settings_port_lbl = Label(settings_connection_fme, text="Port:")
    settings_port_detail_lbl = Label(settings_connection_fme, text=port, state=DISABLED)

    conn_details_edit_img = ImageTk.PhotoImage(Image.open('resources/edit.jpg').resize((25, 25)))
    conn_details_edit_btn = Button(settings_connection_fme, image = conn_details_edit_img, text="Edit", command=edit_conn_details)
    conn_details_edit_btn.image = conn_details_edit_img
    conn_details_edit_btn.grid(row=0, column=2, rowspan=2, padx=default_padding, pady=default_padding)


    settings_ipaddress_lbl.grid(row=0, column=0)
    settings_ipaddress_detail_lbl.grid(row=0, column=1)
    settings_port_lbl.grid(row=1, column=0)
    settings_port_detail_lbl.grid(row=1, column=1)

    settings_connection_fme.grid(row=0, column=0, columnspan=2, padx=default_padding, pady=default_padding)

    settings_fixture_selected_fme = LabelFrame(settings_fixture_fme, text="Selected Fixture")

    global settings_fixture_selected_lbl, settings_fixture_attribute_friendly_name_lbl, settings_fixture_attribute_active_cbx, settings_fixture_attribute_intensity_cbx, settings_fixture_attribute_colour_cbx, settings_fixture_attribute_pantilt_cbx,settings_fixture_attribute_friendly_name_edit_btn

    settings_fixture_selected_lbl = Label(settings_fixture_selected_fme, text="None")

    settings_fixture_selected_lbl.grid(row=0, column=0)
    settings_fixture_selected_fme.grid(row=0, column=1)

    settings_fixture_attribute_fme = LabelFrame(settings_fixture_fme, text="Attributes")



    settings_fixture_attribute_friendly_name_lbl = Label(settings_fixture_attribute_fme, text="", width=17, anchor="w")

    settings_fixture_attribute_friendly_name_edit_img = ImageTk.PhotoImage(Image.open('resources/edit.jpg').resize((15, 15)))
    settings_fixture_attribute_friendly_name_edit_btn = Button(settings_fixture_attribute_fme, image = settings_fixture_attribute_friendly_name_edit_img, text="Edit", command=settings_edit_friendly_name, state="disabled")
    settings_fixture_attribute_friendly_name_edit_btn.image = settings_fixture_attribute_friendly_name_edit_img
    settings_fixture_attribute_friendly_name_edit_btn.grid(row=0, column=3)

    settings_fixture_attribute_active_cbx = Checkbutton(settings_fixture_attribute_fme, text="Enable Active", variable=att_active_var, onvalue=True, offvalue=False, anchor="w", width=15, state="disabled", command=fixture_attribute_active)
    settings_fixture_attribute_intensity_cbx = Checkbutton(settings_fixture_attribute_fme, text="Enable Intensity", variable=att_intensity_var, onvalue=1, offvalue=0, anchor="w", width=15, state="disabled", command=fixture_attribute_intensity)
    settings_fixture_attribute_colour_cbx = Checkbutton(settings_fixture_attribute_fme, text="Enable Colour", variable=att_colour_var, onvalue=True, offvalue=False, anchor="w", width=15, state="disabled", command=fixture_attribute_colour)
    settings_fixture_attribute_pantilt_cbx = Checkbutton(settings_fixture_attribute_fme, text="Enable Pan/Tilt", variable=att_pantilt_var, onvalue=True, offvalue=False, anchor="w", width=15, state="disabled", command=fixture_attribute_pantilt)

    settings_fixture_attribute_friendly_name_lbl.grid(row=0, column=0, columnspan=4)
    settings_fixture_attribute_active_cbx.grid(row=1, column=0, columnspan=4)
    settings_fixture_attribute_intensity_cbx.grid(row=2, column=0, columnspan=4)
    settings_fixture_attribute_colour_cbx.grid(row=3, column=0, columnspan=4)
    settings_fixture_attribute_pantilt_cbx.grid(row=4, column=0, columnspan=4)

    settings_fixture_attribute_fme.grid(row=1, column=1, rowspan=3, padx=default_padding)


def show_values(value):
    print(value)

def fixture_select(event):
    selected_fixture = event.widget.get(event.widget.curselection())[0]
    print(f"Fixture: {selected_fixture}")

    fixture = specify_fixture(selected_fixture)
    fixture_selection_lbl.config(text="> {} - {}".format(selected_fixture, fixture.friendly_name))

    osc_client.send_message(f"/rpc", "\<01>,{}H".format(str(selected_fixture))) # SENDS CLIENT MESSAGE

    console_log("Selected Fixture: {}".format(selected_fixture))

    if fixture.att_intensity:
        intensity_sdr.config(state=ACTIVE)
    else:
        intensity_sdr.config(state=DISABLED)

    if fixture.att_pantilt:
        pan_sdr.config(state=ACTIVE, from_=fixture.pan_range[0], to=fixture.pan_range[1])

        tilt_sdr.config(state=ACTIVE, from_=fixture.tilt_range[0], to=fixture.tilt_range[1])
    else:
        pan_sdr.config(state=DISABLED)
        tilt_sdr.config(state=DISABLED)


    intensity_sdr.set(fixture.current_intensity)
    pan_sdr.set(fixture.current_pan)
    tilt_sdr.set(fixture.current_tilt)


    global global_fixture
    global_fixture = fixture

def intensity_update(event):
    intensity=event
    print(f"Intensity: {intensity}")

    global_fixture.current_intensity = intensity
    osc_client.send_message("/rpc", "\<05>,{}H".format(str(intensity)))

def pan_update(event):
    pan = event
    print(f"Pan: {pan}")

    global_fixture.current_pan = pan
    osc_client.send_message("/rpc", "\<06>,4,{}H".format(pan))

def tilt_update(event):
    tilt = event

    global_fixture.current_tilt = tilt
    print(f"Tilt: {tilt}")
    osc_client.send_message("/rpc", "\<06>,5,{}H".format(tilt))




## Begin??

init_osc()


# globalisation
global root, ip_details_lbl, port_details_lbl, fixture_list_lb, fixture_selection_lbl, console_lb, intensity_sdr, pan_sdr, tilt_sdr

fixture = None

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

if ip_address == None or ip_address == "":
    display_ip_address = "None"
else:
    pass
if port == None or port == "":
    display_port = "None"
else:
    pass


# IP Address
connection_details_fme = LabelFrame(root, text="Connection Details")
ip_title_lbl = Label(connection_details_fme, text="IP:", anchor="e", width=5)
ip_details_lbl = Label(connection_details_fme, text=ip_address, anchor="w", width=15)

# Port
port_title_lbl = Label(connection_details_fme, text="PORT:", anchor="e", width=5)
port_details_lbl = Label(connection_details_fme, text=port, anchor="w", width=15)

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

fixture_list_lb = Listbox(fixture_fme, width=30)
fixture_list_lb.grid(row=5, column=1, columnspan=3, padx=10)

for fixture in fixtures:
    fixture_list_lb.insert(END, (fixture.address, fixture.friendly_name)) # FIXTURES

fixture_fme.grid(row=3, column=0, columnspan=3, rowspan=5, padx=default_padding, pady=default_padding)
fixture_list_lb.bind("<<ListboxSelect>>", fixture_select)

# Fixture Selection Label
fixture_selection_lbl = Label(fixture_fme, text="No Fixture Selected", font="24", width=15)
fixture_selection_lbl.grid(row=1, column=2, padx=default_padding, pady=default_padding)

attributes_fme = LabelFrame(root, text="Controller")
intensity_fme = LabelFrame(attributes_fme, text="Intensity")
intensity_sdr = Scale(intensity_fme, from_=0, to=100, orient=HORIZONTAL, length=200, command=intensity_update, state="disabled")
intensity_sdr.grid(row=0, column=0)
intensity_fme.grid(row=0, column=0)

pantilt_fme = LabelFrame(attributes_fme, text="Pan/Tilt")
pan_sdr = Scale(pantilt_fme, from_=0, to=100, orient=HORIZONTAL, length=200, command=pan_update, state="disabled")
tilt_sdr = Scale(pantilt_fme, from_=0, to=100, orient=VERTICAL, length=200, command=tilt_update, state="disabled")

pan_sdr.grid(row=0, column=0)
tilt_sdr.grid(row=0, column=1)
pantilt_fme.grid(row=0, column=2)

attributes_fme.grid(row=4, column=3, rowspan=5, columnspan=5, padx=default_padding, pady=default_padding)




new_fixture_var = StringVar()
new_friendly_name_var = StringVar()

ip_address_var = StringVar()
port_var = StringVar()

att_friendly_name = StringVar()
att_active_var = IntVar()
att_intensity_var = IntVar()
att_colour_var = IntVar() # For Future Versions
att_pantilt_var = IntVar()

root.mainloop()

