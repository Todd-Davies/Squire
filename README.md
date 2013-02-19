Squire
==========

Today, I made a neat little python script to automatically do *stuff* in my Dropbox based on 
changes to my Schooltraq account. I decided to call it squire.

What it does
----------------

At the moment, it does 
the following:

	1. It first polls Schooltraq.com via the api (http://help.schooltraq.com/kb/schooltraq-api/) and gets all of my active (i.e. not archived) assignments.

	2. It iterates through the assignments, looking for specific triggers.

	3. If a trigger is found for an assignment, then something happens.

There are two triggers at the moment, the first looks for assignments beginning with 'Essay on ' and creates a new .tex file in the following place:

`/Apps/Squire/Homework/<Class name>/Essays/<Essay title>/<Essay title>.tex` 

The <Essay title> is simply the text after 'Essay on ' in the assignment title. The .tex file contains a template with some commonly used packages imported, a page header, and an essay plan.

The essay title and author (the dropbox user display name) automatically filled in too. I have a cron job running the script every hour on my Raspberry Pi, which should strike the balance between keeping things up to date and pestering the Schooltraq and Dropbox servers.

The second trigger looks for assignments beginning with 'Research ' and does a google search for the assignment name (without the 'Research') which it then gets links from and places them in the notes section of the assignment on Schooltraq.

In the future
------------------ 
There is a lot of scope for more triggers. For example, if the user was taking a module in, say Java programming, Squire could automatically set up template .java files and initialise a git repo in a new folder inside that course folder. There are lots of possibilities.

On the subject of triggers, it'd be nice if the triggers weren't just from Schooltraqq either, but could come from any API. 

I may implement a bloom filter to keep track of what assignments I've already processed so I don't end up wasting CPU cycles, API requests or accidentally overwriting files (though since bloom filters return false positives, this shouldn't be relied upon).

I'll open source the tool soon, hopefully I'll remember to abstract my app secret and API keys into another file behind gitignore. This will have the added benifit of making it easier to change the tool to work with multiple users.
