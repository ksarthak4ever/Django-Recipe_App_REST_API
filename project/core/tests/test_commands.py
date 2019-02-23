'''Here testing adding management command to the core app, management command is a helper command that allows us to wait for the database to be available before continuing and wait for other commands.
Gonna use this command in docker-compose file when starting django app. We use this command as sometimes while using postgres with docker-compose in a django app,sometimes the django app fail to start because of an database error.
It is because once the postgres service has started in the docker-compose there are few extra setup tasks that need to be done on the postgres before it is ready to accept connections. So what this means is our django-app will 
try to connect to the database before its ready and therefore it will raise an exception and you will need to restart the app.Adding this helper command to improve reliability of the project,which we can put in front of all the commands
we put in docker-compose file and that will ensure that the database is up and running before we can try to access the database. The helper command is wait_for_db command''' 
'''https://support.circleci.com/hc/en-us/articles/360006773953-Race-Conditions-Wait-For-Database
   
   https://stackoverflow.com/questions/52621819/django-unit-test-wait-for-database'''


# Here using Mocking 

from unittest.mock import patch #it will help mock the behavior of django get database function using which we can simulate the database being available and not being available for when we test our command.

from django.core.management import call_command #allows us to call the command in our source code
from django.db.utils import OperationalError #Operational error django throws when db is unavailable. Using this error to simulate the db being available or not when we run our command
from django.test import TestCase


class CommandTests(TestCase): 

	def test_wait_for_db_ready(self): #Test wait for db when db is available. Here management command is gonna try and retrieve db connection from django, and check when we do so if it retrieves an Operational Error or not.If it does end up retrieving Operational Error then that means db is not available otherwise db is available and command will continue.
		with patch('django.db.utils.ConnectionHandler.__getitem__') as gi: #using patch to mark the connection handler to just return true everytime it's called.Therefore our call command or management command should just continue.Here overriding behavior of ConnectionHandler to do so.
			gi.return_value = True
			call_command('wait_for_db')
			self.assertEqual(gi.call_count, 1)

	@patch('time.sleep', return_value=True) #doing same things as patch fn above but the passes the equivalent of gi as an argument to our fn.This Mock is used to replace the behavior of time.sleep and replaces it with a Mock fn that returns True,So our code wont have to literally wait the seconds or amount specified.Simply to speed up the test.
	def test_wait_for_db(self, ts): #Test waiting for db.This will work like a while loop. It will check to see if ConnectionHandler raises OperationalError and if it does then it will wait a second and then try again. ts time.sleep
		with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
			gi.side_effect = [OperationalError] * 5 + [True]
			call_command('wait_for_db')
			self.assertEqual(gi.call_count, 6)
