**Disclaimer**: This project was created only as a university project and should only be used for authorized testing or educational purposes only.

This Botnet Testing Tool is a testing tool that allows the user to simulate what a botnet can do to a system post-exploitaiton.

It includes features such as:
- A command and control (C&C) server
- A botnet client script
- 3 exploitations commands: Denial of Service (DoS), Email Spam and Status

To the GUI run:
1. Boot up a linux device
2. Run the C&C server script in the command line with the following command `python cc_server_gui.py 3300`
    - The port number can be changed to another port if you wish
3. You start the server by clicking on the "Start Server"
    - On the GUI interface, the "Start Server" button and "Command" drop down should be disabled 
4. Then run the following command in the command line to connect the bot the that server `sudo -E python bot.py [IP_ADDRESS] 3300`
    - Ensure to replace `[IP ADDRESS]` with the IPv4 address of the device that is running the `cc_server_gui.py` script
    - "Command" drop down menu should now be enabled
5. Select whichever command you wish to execute
6. If prompted, fill the entry boxes with the appropriate values
7. Click the "Execute" button and observe the "Command Details" text box on the right hand side 
8. Close the program by closing the GUI's window
    - Note: If either script continues to run, escape by pressing `Ctrl+C`

**Please observe the video demonstrations in the video_examples folder if there is any confusion.**