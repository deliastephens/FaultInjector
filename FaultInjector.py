#!/usr/bin/python
from dronekit_sitl import SITL
# Import DroneKit-Python
from dronekit import connect, VehicleMode
from Tkinter import *
import time, thread, sys, struct, os
from curses import ascii
from pymavlink import mavparm, mavutil
from pymavlink.dialects.v10 import common as mavlink

# Connect to the Vehicle.
#print("Connecting to vehicle on: %s" % (connection_string,))
updatePanes = None
vehicle = None
sitl = None
root = None
connected = False

#toggle buttons:
gpsButton = None
rcButton = None
battButton = None
thrButton = None
GCSButton = None

gcsfs = bfs = tfs = rfs = gpsfs = "Inactive"

#connects to a drone sitting at ip:port and dispatches a thread to display it's
#inforamtion to the readout window
def connectToDrone(sip, sport, dkip, dkport):
  #sitl connection
  global sitl
  sitl = mavutil.mavlink_connection('tcp:'+sip+':'+sport, dialect='ardupilotmega', write=True, input=False)
  print("Waiting for APM heartbeat")
  msg = sitl.recv_match(type='HEARTBEAT', blocking=False)
  print("Heartbeat from APM")
   	
  #Dronekit connection
  global vehicle
  #connect to vehicle at ip:port
  vehicle = connect(dkip+':'+dkport, wait_ready=True)
  global connected 
  connected = True
  
  #initialize globals associated with the vehicle
  global THR_FS_VAL
  THR_FS_VAL = vehicle.parameters['THR_FS_VALUE']
  
  global FS_BATT_MAH
  FS_BATT_MAH = vehicle.parameters['FS_BATT_MAH'] 

  global SYSID_MYGCS
  SYSID_MYGCS = vehicle.parameters['SYSID_MYGCS']

  # create thread to update readout information in real time
  thread.start_new_thread(updateVehicleStatus, (vehicle,))
  
def connectToSITL(ip, port):
  
  global sitl
  sitl = mavutil.mavlink_connection('tcp:'+ip+':'+port, dialect='ardupilotmega', write=True, input=False)
  print("Waiting for APM heartbeat")
  msg = sitl.recv_match(type='HEARTBEAT', blocking=True)
  print("Heartbeat from APM")
  
#disconnects the vehicle and cleans the readout
def disconnect():
  #close vehicle connection
  vehicle.close()
  updateReadoutWindow(updatePanes[0], "Disconneced")
  global connected
  connected = False
  sitl = none;
#def disconnectSTIL():
  #todo 

#continually updates the readout with vehicle information
def updateVehicleStatus(vehicle):
  while(connected): 
    #update the readout with vehicle information  
    updateText = '';
    updateText += ("System Status: %s" % vehicle.system_status.state + 
		      "\nLast Heartbeat: %s" %vehicle.last_heartbeat + 
		      "\nMode: %s" % vehicle.mode.name +
		      "\nIs Atmable?: %s" % vehicle.is_armable + "\n")

    updateText += ("\nBattery Capacity: %s MAH" % vehicle.parameters['BATT_CAPACITY'] +
                   "\nGPS Info: %s" % vehicle.gps_0 + 
	 	   "\nLattitude: %s " % vehicle.location.global_relative_frame.lat +
		   "\nLongitude: %s" % vehicle.location.global_relative_frame.lon +
                   "\nAirspeed: %s" % vehicle.velocity +
                   "\nAltitude: %s" % vehicle.location.global_relative_frame.alt +
		   "\nWind Speed: %s" % vehicle.parameters['SIM_WIND_SPD'] +
		   "\nWind Direction: %s\n" % vehicle.parameters['SIM_WIND_DIR'])
    
    updateText += ("\nGPS Failsafe:      " + gpsfs +
		   "\nRadio Failsafe:    " + rfs +
		   "\nThrottle Failsafe: "  + tfs +
		   "\nBattery Failsafe:  " + bfs +
		   "\nGCS Failsafe:      " + gcsfs) 


    updateReadoutWindow(updatePanes[0], updateText)
    root.update()
    #wait for 1 second
    time.sleep(1)

#helper function to write information to the readout
def updateReadoutWindow(textWindow, text):
  #sets the readout window from read only to read/write
  textWindow.config(state=NORMAL)
  #clears the readout window
  textWindow.delete('1.0', END)
  #inserts text into readout window
  textWindow.insert(END, text)
  #sets window back to read only 
  textWindow.config(state=DISABLED)

#adds toolbar to root frame
def loadToolbar(root):
  #Creates toolbar frame
  toolbar = Frame(root);
  mpToolbar = Frame(toolbar);
  sToolbar = Frame(toolbar);

  mpLabel = Label(mpToolbar, text = "Connect to Mavproxy: ")
  mpLabel.pack(side=LEFT, padx=2, pady=2)
  #creates IP label
  MPipLabel = Label(mpToolbar, text="IP Address")
  MPipLabel.pack(side=LEFT, padx=2, pady=2)
  
  #creates IP entry box
  MPipBox = Entry(mpToolbar)
  MPipBox.delete(0, END)
  MPipBox.insert(0, "127.0.0.1")  
  MPipBox.pack(side=LEFT, padx=2, pady=2)
 
  #creates port label
  MPportLabel = Label(mpToolbar, text="Port")
  MPportLabel.pack(side=LEFT, padx=2, pady=2)

  #creates port entry box
  MPportBox = Entry(mpToolbar)
  MPportBox.delete(0, END)
  MPportBox.insert(0, "14551")  
  MPportBox.pack(side=LEFT, padx=2, pady=2)
  
  #creates connection button
  MPcon = Button(mpToolbar, text="Connect", width=6, command=lambda: connectToDrone(SipBox.get(), SportBox.get(), MPipBox.get(), MPportBox.get()))
  MPcon.pack(side=LEFT, padx=2, pady=2)  
  #creates disconnect button
  MPdis = Button(mpToolbar, text="Disconnect", width=6, command=disconnect)
  MPdis.pack(side=LEFT, padx=2, pady=2)
  
  sLabel = Label(sToolbar, text="Connect to SITL:         ")
  sLabel.pack(side=LEFT, padx=2, pady=2)  

  SipLabel = Label(sToolbar, text="IP Address")
  SipLabel.pack(side=LEFT, padx=2, pady=2)
  
  #creates IP entry box
  SipBox = Entry(sToolbar)
  SipBox.delete(0, END)
  SipBox.insert(0, "127.0.0.1")  
  SipBox.pack(side=LEFT, padx=2, pady=2)
 
  #creates port label
  SportLabel = Label(sToolbar, text="Port")
  SportLabel.pack(side=LEFT, padx=2, pady=2)

  #creates port entry box
  SportBox = Entry(sToolbar)
  SportBox.delete(0, END)
  SportBox.insert(0, "5763")  
  SportBox.pack(side=LEFT, padx=2, pady=2)
  
  #creates connection button
  mpToolbar.pack(side=TOP, fill=X)
  sToolbar.pack(side=TOP, fill=X)
  toolbar.pack(side=TOP, fill=X)

#creates a split panned window, with a text box on the left, and fault buttons on the left
def loadInfoPane(root):
  window = PanedWindow(orient=HORIZONTAL)
  window.pack(fill=BOTH, expand=1) 
  
  leftSubwindow = PanedWindow(orient=VERTICAL) 
  #TBH not sure what bottom left will do yet, but it's here
  bottomLeft = PanedWindow(orient=HORIZONTAL)
  bottomLeft.pack()

  #creates a text box on the left side (this is the readout window)
  readout = Text(root, height=20, width=50)
  readout.pack(side=LEFT)
  readout.config(state=DISABLED)
  
  leftSubwindow.add(readout)
  leftSubwindow.add(bottomLeft)
  
  window.add(leftSubwindow)

  #creates a simple paned window on the right side
  buttonArray = PanedWindow(orient=VERTICAL)
  window.add(buttonArray)
  
  #returns panes
  return [readout, buttonArray, bottomLeft]

def wind(windSPD, windDIR):
  mav_param = mavparm.MAVParmDict()
  mav_param.mavset(sitl, "SIM_WIND_DIR", float(windDIR), retries = 100)
  mav_param.mavset(sitl, "SIM_WIND_SPD", float(windSPD), retries = 100)

def gps():
  global gpsButton, gpsfs
  mav_param = mavparm.MAVParmDict()
  if gpsButton.configure('text')[-1] == 'Disable GPS':
  	if mav_param.mavset(sitl, "SIM_GPS_DISABLE", float(1), retries = 100):
		gpsButton.configure(text='Enable GPS')
		gpsfs = "Active"
	#usse mavlink to disable gps
  else:
  	if mav_param.mavset(sitl, "SIM_GPS_DISABLE", float(0), retries = 100):
		gpsfs = "Inactive"
		gpsButton.configure(text='Disable GPS')

	#uses mavlink to enable gps

def rc():
  global rcButton, rfs
  mav_param = mavparm.MAVParmDict()
  if rcButton.configure('text')[-1] == 'Disable RC':
	if mav_param.mavset(sitl, "SIM_RC_FAIL", float(1), retries = 100):
		rfs = "Active"
		rcButton.configure(text='Enable RC')
	#uses mavlink to disable rc
  else:
  	if mav_param.mavset(sitl, "SIM_RC_FAIL", float(0), retries = 100):
		rfs = "Inactive"
		rcButton.configure(text='Disable RC')
	#uses mavlink to enable rc

def throttle():
  mav_param = mavparm.MAVParmDict()
  global vehicle, thrButton, THR_FS_VAL, tfs
  if thrButton.configure('text')[-1] == 'Activate Throttle Failsafe':
  	if mav_param.mavset(sitl, "THR_FS_VALUE", float(2000), retries = 100):
		tfs = "Active"
		thrButton.configure(text="Deactivate Throttle Failsafe")
  else:
	if mav_param.mavset(sitl, "THR_FS_VALUE", float(THR_FS_VAL), retries = 100):
		thrButton.configure(text="Activate Throttle Failsafe")
		tfs = "Inactive"
	
def battery():
  mav_param = mavparm.MAVParmDict()
  global vehicle, battButton, FS_BATT_MAH, bfs
  if battButton.configure('text')[-1] == 'Activate Battery Failsafe':
  	if mav_param.mavset(sitl, "FS_BATT_MAH", float(4000), retries = 100):
		bfs = "Active"
		battButton.configure(text="Deactivate Battery Failsafe")
  else:
	if mav_param.mavset(sitl, "FS_BATT_MAH", float(FS_BATT_MAH), retries = 100):
		bfs = "Inactive"
		battButton.configure(text="Activate Battery Failsafe")

def gcs():
  mav_param = mavparm.MAVParmDict()
  global vehicle, GCSButton, SYSID_MYGCS, gcsfs
  if GCSButton.configure('text')[-1] == 'Disconnect GCS':
  	if mav_param.mavset(sitl, "SYSID_MYGCS", float(0), retries = 100):
		GCSButton.configure(text="Reconnect GCS")
		gcsfs = "Active"
  else:
   	if mav_param.mavset(sitl, "SYSID_MYGCS", float(SYSID_MYGCS), retries = 100):
  		GCSButton.configure(text="Disconnect GCS")
  		gcsfs = "Inactive"
  
#adds faults to the window
def createFaultButtons(pane):
  #add wind button
  windPane = Frame(pane)
   
  windSPDFrame = Frame(windPane)
  mpLabel = Label(windSPDFrame, text = "Set Wind Speed: ")
  mpLabel.pack(side=TOP, padx=2, pady=2)
  
  windSPDBox = Entry(windSPDFrame)
  windSPDBox.delete(0, END)
  windSPDBox.insert(0, "0")  
  windSPDBox.pack(side=TOP, padx=2, pady=2)
  
  windSPDFrame.pack(side=TOP)

  windDIRFrame = Frame(windPane)
 
  mpLabel = Label(windDIRFrame, text = "Set Wind Direction in Degrees: ")
  mpLabel.pack(side=TOP, padx=2, pady=2)
  
  windDIRBox = Entry(windDIRFrame)
  windDIRBox.delete(0, END)
  windDIRBox.insert(0, "0")  
  windDIRBox.pack(side=TOP, padx=2, pady=2)

  windDIRFrame.pack(side=TOP)

  windB = Button(windPane, text="Set Wind", width = 8,  command=lambda: wind(windSPDBox.get(), windDIRBox.get()))
  windB.pack(pady=5)
  windPane.pack()

  gpsPane = Frame(pane)
  global gpsButton
  gpsButton = Button(gpsPane, text = "Disable GPS", width = 8, command=lambda: gps())
  gpsButton.pack(pady=5);
  gpsPane.pack();

  rcPane = Frame(pane)
  global rcButton
  rcButton = Button(rcPane, text = "Disable RC", width = 8, command=lambda: rc())
  rcButton.pack(pady=5);
  rcPane.pack();

  thrPane = Frame(pane)
  global thrButton
  thrButton = Button(thrPane, text = "Activate Throttle Failsafe", width = 20, command=lambda: throttle())
  thrButton.pack(pady=5);
  thrPane.pack();
  #add engine failure button

  battPane = Frame(pane)
  global battButton
  battButton = Button(battPane, text = "Activate Battery Failsafe", width = 20, command=lambda: battery())
  battButton.pack(pady=5)
  battPane.pack();
   
  GCSPane = Frame(pane)
  global GCSButton
  GCSButton = Button(GCSPane, text = "Disconnect GCS", width = 20, command=lambda: gcs())
  GCSButton.pack(pady=5);
  GCSPane.pack(); 

def main():
  global root
  root = Tk()
  root.title("Fault Injector")
  root.geometry("760x420")
  loadToolbar(root)
  global updatePanes 
  updatePanes = loadInfoPane(root)
  updateReadoutWindow(updatePanes[0],"Use the connect button to connect to a drone!")
  createFaultButtons(updatePanes[1]) 
  root.mainloop()
  
if __name__ == "__main__":
  main()
