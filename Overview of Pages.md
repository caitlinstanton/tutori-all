Overview of Pages

base.html --> landing page
	- Displays basic information about ARISTA and peer tutoring

login.html --> login/register page
	- Allows users to create basic account or log into existing account

verify.html --> verify page
	- Allows users to verify email (through pasting code that was emailed to them in a text box) for their newly created account

tuttee.html --> tuttee dashboard

match.html --> match with a tutor page
	- Only available for tuttees
	- Dropdown for classes, teachers, frees
	- Button to match with corresponding tutor

tutor.html --> tutor dashboard
	- Contains added info about classes, teachers, and frees
	- Displays credits for that trimester

pairings.html --> list of pairings
	- Shows list of tutors or tuttees the user is paired with
	- Displays contact information

sessions.html --> list of sessions
	- Shows list of all submitted session forms
	- Ues colors to show which have discrepancies (red) and which are incomplete, meaning the other person hasn't submitted it yet (yellow?)

submit.html --> form to submit completed session


TO DO:

Admin dashboard --> all lists can be sorted by guidance counselor
	- list of all requests
	- list of pairings
	- list of sessions	
	- credits per users

Change href links from html docs to routes
Make /user return tuttee or tutor dashboard depending on isTutor
Update images