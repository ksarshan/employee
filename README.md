# employee

## Setup

The first thing to do is to clone the repository:
```sh
$ git clone https://github.com/ksarshan/employee.git
$ cd employee
```

Create a virtual environment to install dependencies in and activate it:

```sh
$ virtualenv2 --no-site-packages env
$ source env/bin/activate
```

Then install the dependencies:

```sh
(env)$ pip install -r requirements.txt
```
Note the `(env)` in front of the prompt. This indicates that this terminal
session operates in a virtual environment set up by `virtualenv2`.


Once `pip` has finished downloading the dependencies:


`Creating an admin user`
First we’ll need to create a user who can login to the admin site. Run the following command:
```sh
$ python manage.py createsuperuser
```
Enter your desired username and press enter.
`Username:` enter user name here
You will then be prompted for your desired email address:
`Email address:` enter email here
The final step is to enter your password. You will be asked to enter your password twice, the second time as a confirmation of the first.


```sh
(env)$ cd project
(env)$ python manage.py runserver
```
And navigate to `http://127.0.0.1:8000/`.

###### Email ID is required to login
