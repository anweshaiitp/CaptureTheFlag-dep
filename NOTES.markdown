# NJACK: Capture The Flag 

This repository holds the capture the flag framework used by NJACK, IIT Patna.

## TODO :

- [X] Modify `user_registration` to incorporate team registration
- [X]   Change field names, and error messages
- [X] Change UserTable names throughout to Team
- [X] Figure our models structure for team play and points allocation
- [X] validate Team name, anwesha ID
- [X] Registration 
- [X] Question Loading
- [X] Point System
- [X] Leader Board
- [X] Add Favicon
- [ ] Validate Answers
- [X] Deploying static files https://docs.djangoproject.com/en/1.9/howto/static-files/
- [ ] Answering
- [ ] Has Context
- [X] Add rules page
- [ ] Update Rules page Content
- [X] CSS Question Highlight
- [X] If answered, change color at home
- [X] CSS on messages
- [ ] Add link to team at footer
- [ ] User part of multiple teams
- [X] Make sure anwesha IDs are different
- [X] Test duplicate teamname(Already Username)
- [ ] Test duplicate teamname
- [X] Add footer to registration form
- [ ] Adding timestamps to question answering time
- [ ] Convert all anwesha id to small case before saving in database
- [ ] Anwesha ID -> Team Name (After SMPT, Plug and Play)
- [X] TeamMembers -> TeamDetails
- [X] Validate COllege_name., Phone_number
- [X] Add Team Name in place of user name in registration form
- [X] Validate usernames
- [X] Change error messages 
- [ ] Run deployment as daemon
- [ ] Use nigix to serve static
- [X] Do not allow multiple sessions par user.
- [X] MIT License for `django-preventconcurrentlogins
- [X] Fix login page CSS
- [ ] Fix terminal CSS
- [ ] Document on how to allow concurrent logins
- [ ] concurrent login while javascript
- [ ] Color Change Answered questions and do not let it to be opened
        - opened /closed and color change
        - JS color change on question answering
        - Submitted questions not to be opened again
- [ ] License
- [X] [Ignored] Return button on terminal because mobile forms dont have return key
- [ ] To change or reset password, contact us
- [ ] Define has context view
### For future release
- [ ] create a separate branch which allows
        - Users register separately and agree on a team
        - All members of team can login on different machines
- [ ] How to : user scripts and fixtures
- [ ] Finishing time - opening time
- [ ] Cheatsheet
- [ ] Change title of pages
- [ ] Change password form
- [ ] Testing and veryfying models, views and other code


## Work Flow From Now
- Test locally and work out flaws 
    + This will ignore validating anweshaID to DB
    + also will ignore validating email
- Code review
- **QUESTIONS**
- Deploy and connect to officialDB
- Setup three way userlogin wit SMTP

## Deployement

This is a pain

>It is highly recommended that you use Apache 2.4. Older versions of Apache have architectural design problems and sub optimal configuration defaults, that can result in excessive memory usage in certain circumstances. More recent mod_wsgi versions attempt to protect against these problems in Apache 2.0 and 2.2, however it is still better to use Apache 2.4.

>oth Python 2 and 3 are supported. The minimum recommended versions of each being Python 2.6 and 3.3 respectively. The Python installation must have been installed in a way that shared libraries for Python are provided such that embedding of Python in another application is possible.

STEP 1 : Build and install mod_wsgi from source
**python 2.7**
**apache 2.4.12**
**mod_wsgi 4.4.21**
You can view if your apache2 is threaded by running `apache2ctl -V`.

Installation instructions can be found [here](2). The following are the steps we followed. **This is only for reference**
- [Download source code](1)
- Extract 
- Configure : If you face ` apxs: command not found`, download the apache dev package as described in the instructions.
- Install `apache2-dev`
- Build the package using `make`
- Install apache module `sudo make install`
- Find the `httpd.conf` file. This is actually your `apache2.conf` file. You can find this by running `apache2ctl -V` and looking at `HTTPD_ROOT` and `SERVER_CONFIG_FILE`
`sudo make install` will output where it installed the libraries. You will need this as a parameter for loading.
- Restart `apache2ctl`
If configured correctly, this will be reflected in the apache error logs as
`mod_wsgi/4.4.21 Python/2.7.6 configured `

Now you need to follow the [django documentation][3] on deployment to configure your virtual host and other files. This was the actually painful part.

First make sure that the user and group set in apache conf has access to your project files. The user and group settings are found in `/etc/apache2/envvars`.
Find and edit the following lines:
    
    export APACHE_RUN_USER=<username>
    export APACHE_RUN_GROUP=<username>

Temporary you can set the username as your own.
The in the `/etc/apache2/apache.conf` add the following lines making the necessary edits.

    WSGIScriptAlias /CFG /path/to/CaptureTheFlag/CaptureTheFlag/wsgi.py WSGIPythonPath /path/to/CaptureTheFlag:/path/to/virtualenc/lib/site-packages
    
    <Directory /path/CaptureTheFlag/CaptureTheFlag>
        <Files wsgi.py>
                AllowOverride all
                Allow from all
                Require all granted
        </Files>
    </Directory>

For serving static media, we currently use the apache server itself. For it, add the following lines to the `apache.conf` file.
   
     Alias /static/ /path/to/CaptureTheFlag/static/
    <Directory /path/to/CaptureTheFlag/static>
        Require all granted
    </Directory>

Do not forget to serve admin static files. A simple simlink to `django/contrib/admin/static/admin` will do. 

## Deployment vs testing:
I've tried my utmost to keep the deployment and testing versions separate. To that end, I've maintained the testing copy on `dev` branch and deployment versions on other branches.
Specifically the mysql_port branch contains port to mysql.

MySQL version 5.5

## Connecting to mysql
Connecting to mysql is very easy. 
To connect to an existing database we require two things from dajngo. First we require that django creates its tables in that database and secondly we require the model classes for the tables that were previously in the database so that we can interact with them as well.

#### Connecting to MySQL database
In your global settings.py file edit the following,

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'OPTIONS': {
                'read_default_file': '/path/to/my.cnf',
            },
        }
    }

You also need to create the /path/to/my.cnf file with similar settings from above

    [client]
    database = DB_NAME
    host = localhost
    user = DB_USER
    password = DB_PASSWORD
    default-character-set = utf8

The order of connection resolution is

1. OPTIONS.
2. NAME, USER, PASSWORD, HOST, PORT
3. MySQL option files.

This will connect django to the MySQL database. You may have to install `mysql-python` package if you dont have it already. 

If you migrate now, all your model tables will be created in the database. But don't migrate just yet.

#### Obtaining model definitions for pre-existing tables
Once connected, obtaining model definitions for preexisting tables is as simple as 
    
    python manage.py inspectdb

After you have obtained the models, you can use them as you like. Migrate now to create the models defined my you and start your server to test.


[1]: "http://code.google.com/p/modwsgi/downloads/list" "Source code"
[2]: "https://code.google.com/p/modwsgi/wiki/QuickInstallationGuide" "Mod_Wsgi installation instructions"
[3]: "https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/modwsgi/" "Deployiin django on mod_wsgi"

