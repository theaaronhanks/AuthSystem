# Authentication System

## Requirements

This program depends on the basic python libraries, as well as the bcrypt library. Python must be installed, and then bcrypt can be installed with 'pip install bcrypt'

## Usage

After installing the required library, the program can be run from the root directory of the project. Running the project from a different location will cause errors when accessing data files.

After the program has started, the user is presented with a screen with an option to login, or an option to exit. Upon selecting the login option, the user will be prompted to enter a username and password. Incorrect credentials will be indicated by a message to the screen. Correct credentials will direct the user to a main menu.

If this is the first time the user has logged in, the user will only be presented with the option to go back to the login screen or to change their password. If the user successfully changes their password, they will be presented with the options to change it again or to go back to the main menu. Upon returning to the main menu, they will be presented with all options available to their role.

### Options

#### Administration

The Administration option presents the user with an Admin menu with a Manage Users option and a View Calculations option. The Manage Users option shows a filterable list of all HR and Admin users in the system. The user can then choose a user to view more details. HR users can be edited while Admin users cannot. When editing a user's job title, valid options are ["hr", "ja", "sa", "je", "se", "math"]. These are abbreviations of the roles available in the system. 

The View Calculations option shows a list of all calculations made by any user in the system. This list can be filtered by operation.

#### HR

The Human Resources option allows the user to view and edit users in the system. All users can be viewed, and all users aside from admin or hr can be edited. Again, when editing a user's job title, valid options are ["hr", "ja", "sa", "je", "se", "math"], however "hr" is not available for hr users to assign. New users can be added, and to do so requires the user to enter details about the new user. 

#### Add, Subtract, Multiply, Divide

All mathematical operations are very similar. In each case the user is prompted to enter 2 inputs. Upon submiting the numbers, if the calculation was successful, the result will be printed to the screen.

#### Personal

Upon selecting the Personal option, the user is presented with a screen containing their information and the ability to edit some of those details.

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

## File structure

The following are example entries to each of the data files in server/data
- access.txt
    - role,actions*
    - there may be any number of actions after the role, depending on which role
- calcs.txt
    - timestamp,user_id,input1,input2,operation,result
- logs.txt
    - time || user_id performed action: action || Status: status 
- passwd.txt
    - user_id,username,password_hash
- users.txt
    - user_id,user_name,first_name,last_name,email,role,new,last_login