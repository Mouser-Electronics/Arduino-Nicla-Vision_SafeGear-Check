# Arduino Nicla Vision's SafeGear Check

SafeGear Check is a smart object-recognition system powered by Arduino Nicla Vision. This system checks safety gears like helmets, vests, masks, and gloves in real-time to check and make sure the workers are well equipped with all the required safety gear to prevent workplace accidents.
This is a system that enables employers to first choose and set the required gear that the employees will need to wear. From there, the Nicla Vision will use the trained Edge Impulse AI model designed for object recognition to then check for the gear
set by the employers. From there, the Nicla Vision will control the Adafruit Tower Light and Speaker as visual and voice feedback based on the detection results. All the results will be stored in a file for employers to review later. This system also has a web interface element
with Visual Studio Code to create a web dashboard for employers to set requirements and a log in interface for workers. With SafeGear Check, let’s strive to ensure that all the workers are well equipped and protected before they enter hazardous environments and decrease the number of workplace accidents. 

## Core Features
  - Real Time AI Detection done by Nicla Vision
  - Safety Gear requirements can be set by the employer under "Employer Settings" by pressing push buttons on the circuit. This will update the Nicla Vision on what it has to check for.
  - Interactive web dashboard for employers to set the required gear and employees to log in and get checked. Detection results will also be displayed here.
  - Visual and voice feedback provided by the tower light and speaker controlled by the Nicla Vision based on what it detects
  - Automatically stores the worker login and their detection results for employer review

## Required Hardware
- Arduino Nicla Vision
- Push buttons
- Tower Lights Tower Light – Red Yellow Green Alert Light with Buzzer – 12VDC (external power supply needed)
- DFPlayer Mini MP3 Player and Same Sky CMS-235-18L152 Speaker
- Memory Cards A2 class micro-SD card

## Required Software
- OpenMV IDE
- Visual Studio Code

## Hardware Set Up 
- Follow the instructions in the article to set up the hardware - mouser.com/[urlforarticle]

## Software Set Up 
1) Firstly, clone the repository by running the following command `git clone [Arduino-Nicla-Vision_SafeGear-Check}`
2) On the Visual Studio Code terminal, save all the VS Code files on VS Code, and run `npm init`, `npm install express`, and `npm install`.
3) Plug in the Nicla Vision to your computer. Save the **main.py**, **trained.tflite**, **labels.txt**, and **System_log.txt** to the Nicla Vision USB folder that should pop up in your File Explorer.
4) Open **main.py** on OpenMV IDE. Under **Tools**, click on **Save open script to OpenMV Cam (as main.py)**. A red light should blink once on the Nicla Vision. Close OpenMV, unplug your Nicla Vision, and plug it back in.
5) Open the Server.js and find the line that says `const portName = COM5;`. Change the COM5 to the correct COM port for your Nicla Vision on your computer.
6) Run the server by running `node server.js` on your VS Code terminal.

## System Workflow
1) Running `node server.js` should give you the link `http://localhost:3000`. Click on the link and it should bring you to the dashboard.
2) Click on **Employer Settings** and log in. Then clink on the buttons corresponding to the specific safety gear to set the gear requirements. Then, click **Return to Log In Page** to log out.
3) You should be back to the **Employee Sign in** Page. Enter your **First and Last Name** to log in. Click on **Start Safety Check**. The Nicla Vision should check and display the results accordingly on the screen, with the appropriate light and speaker feedback.
4) On the Nicla Vision USB folder, the **System_log.txt** file should be present, which should have stored the date, time, employee name, and their detection results.
