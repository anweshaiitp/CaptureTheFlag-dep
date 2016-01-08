# User Session App

This app controls,
- user information
- session information

The intended design is plug and play. Do not add irrelevant information to this model. User the user_id attribute for any cross app links.

We do not allow multiple sessions. We can only allow
for one session per user. [This SO link][3] is to a method to achieve this.

Look [here][1] for authentication information.
[This][2] is a good read on sending session information
across insecure connection. 


# TODO
- [ ] : Enable user groups and permissions
- [ ] : Setup email authentication
- [X] : use `next` to redirect after login
- [ ] : Setup the SMTP server and the local email server
- [ ] : Describe how the plug play is going to work. Document the changes required
- [ ] : Write test cases for modal fields. (SQL injection and similar exploits)
- [ ] : Modify the user_session login page to show a disabled account error when trying to login using a disabled account.
- [ ] : Donot forget to add settings.* and the related docs.
- [ ] : Rewrite test cases


[1]: http://www.djangobook.com/en/2.0/chapter14.html "Authentication in Django"
[2]: http://stackoverflow.com/questions/7562675/proper-way-to-send-username-and-password-from-client-to-server "Sending username and password across an insecure network" 
[3]: http://stackoverflow.com/questions/5470210/django-one-session-per-user "One session per user"