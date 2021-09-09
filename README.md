# IServ.py <img src="https://iserv.de/downloads/logo/IServ_Logo_klein_RGB_clean.svg" alt="" height="35" align="right">

`Made by RoRo160` `v.0.01.0-beta`

This module provides an easy way to communicate with your IServ account.
I reverse-engineered parts of the internal IServ api and recreated some http requests your browser would do in the 
background.

> 🔴 **WARNING:** <br/> 
> This module does **NOT** use an official api!
> 
> Extensive usage might lead to problems with your IServ account.
> 
> **USE AT YOUR OWN RISK!!!**

### Features:

- Login/Logout with your IServ account
- Plan changes, by week, day, filtered by course
- Get all tasks

### Coming soon:

- Read all your emails
- Notifications

## Usage:

> ⚠ **Note:**
> To run you might need to install some dependencies.
> 
> Do that by running the following command: 
> ````shell 
> pip install -r requirements.txt 
> ````

### Login/Logout:
````python
from iserv import *

# create IServ object, link your IServ server 
# (please add "https://" before domain name and don't add a "/" at the end!)
iserv = IServ("https://your.iserv.example")

# login to your account
iserv.login("your.username", "password")

# >>> do what ever you want here <<<

# do NOT forget to logout
iserv.logout()
````

> #### 💡 **Advise:** Time delay between requests
> Many requests in a short time period may seem suspicious to the server.
> 
> To prevent any issues with your account add a **random time delay** between requests.
> 
> You can do this as shown here:
> 
> ````python
> import time
> import random
> 
> # first request
> 
> # random break between two requests
> time.sleep(random.uniform(0.5, 10.0))
> 
> # second request
> ````
> 


### How to use all the features?

#### Plan changes:
````python
changes = iserv.plan_changes(
    courses=["7c", "10b"], 
    days=["monday", "thursday"]
)

# do something with plan changes dictionary
````
#### Tasks:
````python
tasks = iserv.tasks(
    status="current",
    sort_by="enddate",
    sort_dir="DESC"
)

# do something with task list
````

#

> By RoRo160  `v.0.01.0-beta`
> 
> [My GitHub](https://github.com/RoRo160)
