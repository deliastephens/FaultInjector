#!/usr/bin/python
import dronekit_sitl
# Import DroneKit-Python
from dronekit import connect, VehicleMode
from Tkinter import *
import time
import thread
# Connect to the Vehicle.
#print("Connecting to vehicle on: %s" % (connection_string,))
updatePanes = None
vehicle = None
root = None

def connectToDrone(ip, port):
  print "Connecting To Drone"
  #vehicle = connect('127.0.0.1:14551', wait_ready=True)
  global vehicle
  vehicle = connect(ip+':'+port, wait_ready=True)
  # Get some vehicle attributes (state)
  
  print "Get some vehicle attribute values:"
  print " GPS: %s" % vehicle.gps_0
  print " Battery: %s" % vehicle.battery
  print " Last Heartbeat: %s" % vehicle.last_heartbeat
  print " Is Armable?: %s" % vehicle.is_armable
  print " System status: %s" % vehicle.system_status.state
  print " Mode: %s" % vehicle.mode.name    # settable
  
  thread.start_new_thread(updateVehicleStatus, (vehicle,))
  # Close vehicle object before exiting script
  #vehicle.close()
  
  # Shut down simulator
  #sitl.stop()
  print("Completed")

def disconnect():
  vehicle.close()

def updateVehicleStatus(vehicle):
  while(1): 
    updateReadoutWindow(updatePanes[0], "%s" % vehicle.gps_0 +
    "\n%s" % vehicle.battery +
    "\nLast Heartbeat: %s" % vehicle.last_heartbeat +
    "\nIs Armable?: %s" % vehicle.is_armable +
    "\nSystem status: %s" % vehicle.system_status.state +
    "\nMode: %s" % vehicle.mode.name)  
    root.update()
    time.sleep(1)

def updateReadoutWindow(textWindow, text):
  textWindow.config(state=NORMAL)
  textWindow.delete('1.0', END)
  textWindow.insert(END, text)
  textWindow.config(state=DISABLED)

def loadToolbar(root):
  toolbar = Frame(root);
  
  ipLabel = Label(toolbar, text="IP Address")
  ipLabel.pack(side=LEFT, padx=2, pady=2)
  
  ipBox = Entry(toolbar)
  ipBox.delete(0, END)
  ipBox.insert(0, "127.0.0.1")  
  ipBox.pack(side=LEFT, padx=2, pady=2)
 
  portLabel = Label(toolbar, text="Port")
  portLabel.pack(side=LEFT, padx=2, pady=2)

  portBox = Entry(toolbar)
  portBox.delete(0, END)
  portBox.insert(0, "14550")  
  portBox.pack(side=LEFT, padx=2, pady=2)
  
  b = Button(toolbar, text="Connect", width=6, command=lambda: connectToDrone(ipBox.get(), portBox.get()))
  b.pack(side=LEFT, padx=2, pady=2)  
  
  d = Button(toolbar, text="Disconnect", width=6, command=disconnect)
  d.pack(side=LEFT, padx=2, pady=2)
  toolbar.pack(side=TOP, fill=X)

def loadInfoPane(root):
  m = PanedWindow(orient=HORIZONTAL)
  m.pack(fill=BOTH, expand=1) 
  
  text2 = Text(root, height=20, width=50)
  #scroll = Scrollbar(root, command=text2.yview)
  #text2.configure(yscrollcommand=scroll.set)
  #scroll.pack(side=LEFT, fill=Y)
  text2.pack(side=LEFT)
  text2.config(state=DISABLED)
  
  m.add(text2)

  T2 = PanedWindow(orient=VERTICAL)
  m.add(T2)
  
  return [text2, T2]

def wind():
  print "boy, it's windy"

def createFaultButtons(pane):
  b = Button(pane, text="Wind", width = 3, command = wind)
  b.pack()

def main():
  global root
  root = Tk()
  root.geometry("800x600")
  loadToolbar(root)
  global updatePanes 
  updatePanes = loadInfoPane(root)
  updateReadoutWindow(updatePanes[0],"Use the connect button to connect to a drone!")
  createFaultButtons(updatePanes[1])
  root.mainloop()
  
if __name__ == "__main__":
  main()
