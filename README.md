# SafeGear Check: An AI Powered Safety Gear Detector with Nicla Vision

SafeGear Check is a safety-gear-detecting system that scans individuals as they enter a work area to ensure they are wearing the required personal protective equipment (PPE). The system employs the Arduino Nicla Vision artificial intelligence (AI) camera module and an AI model trained on Edge Impulse. The system includes lights and a speaker for visual and voice feedback based on the detection results.
In this project, you will learn how to build the SafeGear Check system, including connecting the Nicla Vision outputs to a web interface to improve system efficiency. For more information, read the supplemental project article.

## Core Features
- Real-time AI detection by an Arduino Nicla Vision
- An interactive web dashboard that allows employers to define the required PPE, enables employees to log in and initiate a PPE scan, and displays detection results
- Visual and voice feedback controlled by the Nicla Vision based on detection results
- Automatic storage of worker logins and their detection results for employer review

## Required Hardware
- Arduino Nicla Vision
- Push buttons
- Tower Lights Tower Light – Red Yellow Green Alert Light with Buzzer – 12VDC (external power supply needed)
- DFPlayer Mini MP3 Player and Same Sky CMS-235-18L152 Speaker
- Refer to the article for more specific hardware requirements

## Required Software
- OpenMV IDE
- Visual Studio Code

## Hardware Set Up 
- Follow the schematic instructions in the article to set up the hardware.

## Software Set Up 
1) Firstly, clone the repository by running the following command `git clone [Arduino-Nicla-Vision_SafeGear-Check}`.
2) On the Visual Studio Code terminal, save all the VS Code files on VS Code, and run `npm init`, `npm install express`, and `npm install`.
3) Plug in the Nicla Vision to your computer. Save the **main.py**, **trained.tflite**, **labels.txt**, and **System_log.txt** to the Nicla Vision USB folder that should pop up in your File Explorer.
4) Open **main.py** on OpenMV IDE. Under **Tools**, click on **Save open script to OpenMV Cam (as main.py)**. A red light should blink once on the Nicla Vision. Close OpenMV, unplug your Nicla Vision, and plug it back in.
5) Open the Server.js and find the line that says `const portName = COM5;`. Change the COM5 to the correct COM port for your Nicla Vision on your computer.
6) Run the server by running `node server.js` on your VS Code terminal.

## System Workflow
1) Running `node server.js` should give you the link `http://localhost:3000`. Click on the link and it should bring you to the dashboard.
2) Click on **Employer Settings** and log in. Then clink on the buttons corresponding to the specific safety gear to set the gear requirements as per the instructions on the screen (refer to the **Execution** part of the article for more details on the workflow). Then, click **Return to Log In Page** to log out.
3) You should be back to the **Employee Sign in** Page. Enter your **First and Last Name** to log in. Click on **Start Safety Check**. The Nicla Vision should check and display the results accordingly on the screen, with the appropriate light and speaker feedback. Make sure you position yourself correctly in front of the camera so that the Nicla Vision can scan you properly to check for the required gear.
4) On the Nicla Vision USB folder, the **System_log.txt** file should be present, which should have the date, time, employee name, and their detection results stored.
