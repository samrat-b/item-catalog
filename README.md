Project Details
---------------
A German Application, which allows user to view all German course levels available for a user. Once user authenticate himself with google login, user can add, update and delete a course of a particular level.

Setup Runtime Environment
-------------------------
It is recommended to set up the environment first like the one is used to 
develop this program. 

> Install Vagrant: 
Download Vagrant software using [URL](https://www.vagrantup.com/downloads.html)
, then install the version respective to your OS.

> Install VirtualBox:
Download VirtualBox using [URL](https://www.virtualbox.org/wiki/Download_Old_Builds_5_1), then install the version respective to your OS.

How to run the application
--------------------------
1. Clone [Reporsitory](https://github.com/udacity/fullstack-nanodegree-vm)
2. Place the code part of this project inside catalog folder of above cloned repository 
3. Run Vagrant - 'vagrant up'
4. Login to Vagrant - 'vagrant ssh'
5. Navigate inside the catalog folder of cloned repository in step one
6. Run - 'python create_categories.py' to create three German Course levels
7. Run - 'python project.py'
8. Open 'Learn German Easy Way App' in web browser with "http://localhost:5000"
9. You are free to play with this app now :)

Consume this App's data into another App using below JSON endpoints:
-------------------------------------------------------------------- 
1. /levels/json
    - Returns all German Course levels
2. /courses/<int:level_id>/json
    - Returns all courses details belonging a particular level
3. /course/<int:course_id>/json 
    - Returns a particular course level detail
    
Acknowledgment
--------------
I acknowledge [Udacity](https://www.udacity.com/) for the tutorials and resources, which assisted me to develop this app.
