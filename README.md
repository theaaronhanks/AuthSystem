# Authentication System

## Description
This application is a simple system to authenticate users and control access to resources. The system allows users to login, change their password, and perform various mathematical operations. The system also allows administrators to manage users and view calculations performed by users. Users have one of the following roles: Administrator, Human Resources, Junior Accountant, Senior Accountant, Junior Engineer, Senior Engineer, or Mathematician. Each role has a different set of permissions. The system is designed to be run on a single machine, and all data is stored in text files. This system is not designed to be secure, as the data and user files can be accessed and edited outside the application. This is only intended to demonstrate the use of authentication and authorization. This application implements a Role Based Access Control (RBAC) system. It enforces the principle of least privelege and checks every access to verify acceptable usage. The system also logs all access attempts and changes to user data.

## Installation

Python, including the tkinter library is required to run this application. Python can be downloaded from [here](https://www.python.org/downloads/). Tkinter is usually included in the standard library, so no additional installation should be required.

To install the application:
1. Clone this repository
2. Setup a virtual environment using `python3 -m venv .venv`
3. Install the requirements using `pip install -r requirements.txt`

## Usage

After installing the required libraries, the program can be run from the root directory of the project. Running the project from a different location will cause errors when accessing data files.

To run the program:
1. Activate the virtual environment
2. Run the project using `python3 app.py`

After the program has started, the user is presented with a screen with an option to login, or an option to exit. Upon selecting the login option, the user will be prompted to enter a username and password. Incorrect credentials will be indicated by a message to the screen. Correct credentials will direct the user to a main menu.

If this is the first time the user has logged in, the user will only be presented with the option to go back to the login screen or to change their password. If the user successfully changes their password, they will be presented with the options to change it again or to go back to the main menu. Upon returning to the main menu, they will be presented with all options available to their role.

### Options

#### Administration

The Administration option presents the user with an Admin menu with a 'Manage Users' option and a 'View Calculations' option. The 'Manage Users' option shows a filterable list of all HR and Admin users in the system. The user can then choose a user to view more details. HR users can be edited while Admin users cannot. When editing a user's job title, valid options are ["hr", "ja", "sa", "je", "se", "math"]. These are abbreviations of the roles available in the system. 

The 'View Calculations' option shows a list of all calculations made by any user in the system. This list can be filtered by operation.

#### HR

The Human Resources option allows the user to view and edit users in the system. All users can be viewed, and all users aside from admin or hr can be edited. Again, when editing a user's job title, valid options are ["hr", "ja", "sa", "je", "se", "math"], however "hr" is not available for hr users to assign. New users can be added, and to do so requires the current user to enter details about the new user. Upon creating a new user, a temporary password is generated and displayed to the user. The new user will be prompted to change their password upon logging in for the first time.

#### Add, Subtract, Multiply, Divide

All mathematical operations are very similar. In each case the user is prompted to enter 2 inputs. Upon submiting the numbers, the result will be printed to the screen as long as the calculation was successful.

#### Personal

Selecting the Personal option presents the user with a screen containing their information and the ability to edit some of those details.

## User Information

The following users are already added to the system and can be accessed via these credentials:
- Admin Man
    - Username : admin
    - Password : b@dp@55w0rd
- Hr Man
    - Username : hr
    - Password : 4EnLxyg(zLPt 
- Ja Man
    - Username : ja
    - Password : b1%RDpDvSaqkx
- Sa Man
    - Username : sa
    - Password : nOncRAzdsZ4w)
- Je Man
    - Username : je
    - Password : nuUhZ!!*$s0tY
- Se Man
    - Username : se
    - Password : UhiMQ@SS5vCOA
- Math Man
    - Username : math
    - Password : 5wviHprsN&CMg

## Logged events
The events logged by the system are as follows:
- Login
- Change Password
- Add User
- Edit User
- Delete User
- Calculation
- Retrieve Calculations
- Retrieve Users


## File structure

The following are example entries to each of the data files in server/data
- access.txt
    - role,actions*
        - there may be any number of actions after the role, depending on which role
    - EX: sa,add,sub
- calcs.txt
    - timestamp,user_id,input1,input2,operation,result
    - EX: 1677107290066,cfb8f318-a9a8-4cf2-8302-f85080e6758e,3,5,div,0.6
- logs.txt
    - time || user_id performed action: action || Status: status 
    - EX: 2023-09-01 16:53:09.965504 || cbeb71e8-f820-4b50-813b-5a392a620168 performed action: get users || Status: success
- passwd.txt
    - user_id,username,password_hash
    - EX: cfb8f318-a9a8-4cf2-8302-f85080e6758e,math,$2b$12$M2gzpFFFc5n.Xs2dCIUfXuo13baxjFJ/ilKqyVtAKZF06/yCbM47G
- users.txt
    - user_id,user_name,first_name,last_name,email,role,new,last_login
    - EX: 1a2e1741-b621-4dad-8bd0-3faf86990c00,ja,ja,man,ja@man.com,ja,false,1677121590319