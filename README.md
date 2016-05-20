<h1>panoramic_falcons</h1>
<p>Working with Ms. Mahoney to make a peer tutoring managament system for ARISTA</p>

<br>

<h2>What Does the Site Do?</h2>
<h3>Necessary Features</h3>
<ul>
	<li>Allow for tutees to sign up for an account if they need help</li>
	<li>Allow for tutors to sign up for an account if they need to earn credits</li>
	<li>Ensure all accounts are from the same school based on initial school information inputted (email domain, school name, etc.)</li>
	<li>Pair tutors and tutees RANDOMLY based on availability, classes, and teachers (in order to ensure there are no biased pairs and that the sessions are as helpful as possible)</li>
	<li>Allow for tutors to check their credits for previous, current, and future crediting periods</li>
	<li>Allow for administrators to edit the list of tutors, list of committee members (optional), credit requirements, and crediting periods</li>
	<li>Allow for administrators to oversee unpaired tutee/tutor accounts, paired tutors/tutees, completed sessions, sessions with discrepancies, and user credits</li>
</ul>

<br>

<h3>Ideas</h3>
<ul>
	<li>Put limit of amount of tutees a tutor can handle (3)</li>
	<li>Automatic unpairing when tutees/tutors flake after a certain amount of times</li>
	<li>Automatic emailing of tutees after a certain amount of time if they're still unapired</li>
	<li>FAQ about peer tutoring, guidance counselor information, etc.</li>
	<li>Automatically not credit a session if it's submitted more than a week, two weeks after the session</li>
	<li>Check location of session</li>
	<li>Facial recognition of selfie after completing session (each account would require a photo)</li>
	<li>Get rid of grade-checking system for tutors</li>
	<li>Tutee has to rank sessions (1-5) in order to ensure tutors are of high quality (only show this to school staff)</li>
	<li>Leadership board for tutors with best ranking, most sessions, most committed, etc.</li>
	<li>Incentives for tutoring in more-requested classes (geometry, biology, physics)</li>
	<li>Internal notification system, phone contact information, display preferred method of communication</li>
</ul>

<br>

<h3>Optional Goals</h3>
<ul>
	<li>
		<i>Setting up a school</i>
		<br>
		<p>First account made would establish the precedent for the rest of the accounts/functionality</p>
		<ul>
			<li>Type of email for Google authentication</li>
			<li>Name of school</li>
			<li>Initial list of approved tutors and their emails</li>
			<li>Initial credit requirements, number of crediting periods (ARISTA uses trimesters, but other schools may not), etc.</li>
			<li><i>OPTIONAL: </i>List of committee members and their emails, because they may have different credit requirements from general tutors</li>
		</ul>
	</li>
	<li>
		<i>Connect to Naviance or other grading system</i>
		<br>
		<p>This could be used to:</p>
		<ul>
			<li>Verify tutor grades to ensure that they are able to tutor in certain subjects</li>
			<li>Verify tutor's teachers that they had for certain classes to ensure that they can be effectively paired up with a tutee in that teacher's class</li>
			<li>Check tutee grades to automatically notify them if they need help in a class and automatically update their settings to request a tutor in that subject -- UPDATE: NOT VIABLE</li>
		</ul>
	</li>
	<li>
		<i>Connect to school mailing list</i>
		<br>
		<p>This could be used to sign every student up automatically for an account, if they ever need help in a class</p>
	</li>
</ul>

<br>

<h2>Signing In</h2>
<ul>
	<li>Google authentication to ensure every user signs in with their stuy.edu emails</li>
	<li>User inputs their personal/account information, including:
		<ul>
			<li>Name</li>
			<li>Password</li>
			<li>Additional email (optional)</li>
			<li>Free periods/times</li>
			<li>Classes (that they need help in, can tutor in)</li>
			<li><i>ONLY IF A TUTOR: </i>Grades in the classes that they wish to tutor in</li>
			<li>Teachers for the classes they inputted</li>
		</ul>
	</li>
	<li>Every user is automatically programmed to be a tutee, because everyone needs help at some point!</li>
	<li>A user account will only have tutor functionality if their email can be found on the inputted list of tutors</li>
	<li>Account dashboard will allow for a smooth transition between tutee and tutor account functions (most likely done through a button/checkbox and D3 transitions)</li>
</ul>

<br>

<h2>Account Functions</h2>
<h3>General</h3>
<ul>
	<li>Update account information</li>
	<li>Update availability to tutor/be tutored</li>
	<li>Update classes</li>
	<li>Update teachers</li>
	<li>Update grades (unless that can be pulled from Naviance--perhaps there can be a way to automatically sign everyone in a school up for an account, and then prompt them to get tutored for a class if their grade goes below a certain point [this would require automatic retrieval of data])</li>
</ul>
<h3>Tutee</h3>
<ul>
	<li>Select a tutor (RANDOMLY, based on availability and classes)</li>
	<li>Submit form at the complete of a session</li>
	<li>Submit a form if there is a discrepancy between the information for a submitted session (time, date, etc.)</li>
</ul>
<h3>Tutor</h3>
<ul>
	<li>Select a tutee (RANDOMLY, based on availability and classes)</li>
	<li>Submit form at the complete of a session</li>
	<li>Submit a form if there is a discrepancy between the information for a submitted session (time, date, etc.)</li>
	<li><i>OPTIONAL: </i>Notify tutee's teacher that sessions are occuring and update the teacher on their progress</li>
</ul>
<h3>Administrator</h3>
<ul>
	<li>Add/remove members to/from the list of approved tutors</li>
	<li>Add/remove members to/from the committees</li>
	<li>Update the name/number of committees</li>
	<li>Update the credit requirements (specific to each committee) and number of crediting periods</li>
	<li>Check list of completed sessions (coloring of sessions could indicate if there is a discrepancy, etc.)</li>
	<li>Check list of unpaired tutees/tutors and manually pair up people (not recommended, but a necessary function)</li>
	<li>Send emails/notifications (to specific people, only tutors, only tutees)</li>
</ul>
<h3>School Staff</h3>
<ul>
	<li>Be able to check which students have signed up for tutee accounts</li>
	<li>See a list of paired and unpaired students</li>
	<li>See a log of completed sessions</li>
</ul>

<br>

<h2>Flow of Site</h2>
<ul>
	<li>Select tutor, tutee, administrator/school account, or to create a new account</li>
	<li>Sign up/create account using Google 
</ul>