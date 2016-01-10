# NJACK: Capture The Flag 

This repository holds the capture the flag framework used by NJACK, IIT Patna.

Should we allow each individual user to login or should we stick to one team per session login ?
if inidividual user logges in, should we
## TODO :

- [X] Modify `user_registration` to incorporate team registration
- [X]   Change field names, and error messages
- [X] Change UserTable names throughout to Team
- [X] Figure our models structure for team play and points allocation
- [X] validate Team name, anwesha ID
- [X] Registraion 
- [X] Questiong Loading
- [X] Point System
- [X] Leader Board
- [ ] How to : user scripts and fixtures
- [X] Add Favicon
- [ ] Validate Answers
- [X] Deploying static files https://docs.djangoproject.com/en/1.9/howto/static-files/
- [ ] Answering
- [ ] Has Context
- [X] Add rules page
- [ ] Update Rules page Content
- [X] CSS Question Heighlight
- [X] If answered, change color at home
- [X] CSS on messages
- [ ] Add link to team at footes
- [ ] User part of multiple teams
- [X] Make sure anwesha IDs are different
- [X] Test duplicate teamname(Already Username)
- [ ] Test duplicate teamname
- [X] Add footer to registation form
- [ ] Adding timestamp to question answering time
- [ ] Convert all anwesha id to small case before saving in database
- [ ] Anwesha ID -> Team Name (After SMPT, Plug and Play)
- [X] TeamMembers -> TeamDetails
- [X] Validate COllege_name., Phone_number
- [X] Add Team Name in place of user name in registration form
- [X] Validate usernames
- [X] Change error messages 
- [ ] Run deployment as daemon
- [ ] Use nigix to serve staticop

## Deployement

This is a pain

>It is highly recommended that you use Apache 2.4. Older versions of Apache have architectural design problems and sub optimal configuration defaults, that can result in excessive memory usage in certain circumstances. More recent mod_wsgi versions attempt to protect against these problems in Apache 2.0 and 2.2, however it is still better to use Apache 2.4.

>oth Python 2 and 3 are supported. The minimum recommended versions of each being Python 2.6 and 3.3 respectively. The Python installation must have been installed in a way that shared libraries for Python are provided such that embedding of Python in another application is possible.

STEP 1 : Build and install mod_wsgi from source
**python 2.7**
**apache 2.4.12**
**mod_wsgi 4.4.21**
You can view if your apache2 is threaded by runnin `apache2ctl -V`.

Instalation instructions can be found [here](2). The following are the steps we followed. **This is only for reference**
- [Download source code](1)
- Extract 
- Configure : If you face ` apxs: command not found`, download the apache dev package as discribed in the instructions.
- Install `apache2-dev`
- Build the package using `make`
- Install apache module `sudo make install`
- Find the `httpd.conf` file. This is actually your `apache2.conf` file. You can find this by running `apache2ctl -V` and looking at `HTTPD_ROOT` and `SERVER_CONFIG_FILE`
`sudo make install` will output where it installed the libraries. You will need this as a parameter for loadking.
- Restart `apache2ctl`
If configured correctly, this will be reflected in the apache error logs as
`mod_wsgi/4.4.21 Python/2.7.6 configured `

Now you need to follow the [django documentation][3] on deployment to configure your virtual host and other files. This was the actually painful part.

First make sure that the user and group set in apache conf has access to your project files. The user and group settings are found in `/etc/apache2/envvars`.
Find and edit the following lines:
    
    export APACHE_RUN_USER=<username>
    export APACHE_RUN_GROUP=<username>

Temporarly you can set the username as your own.
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



[1]: "http://code.google.com/p/modwsgi/downloads/list" "Source code"
[2]: "https://code.google.com/p/modwsgi/wiki/QuickInstallationGuide" "Mod_Wsgi installation instructions"
[3]: "https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/modwsgi/" "Deployiin django on mod_wsgi"

