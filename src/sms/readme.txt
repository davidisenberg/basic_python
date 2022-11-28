


Phase 1	Get app deployed and usable with a hard link
	x Get twilio account
	x Create web server
	x deploy to pythonanywhere
Phase 1.1	
	  add Mom and Eric's numbers [need their help]
	x write an RFB
	x Give more feedback after message is sent
	x Write down deployment instructions
	  Ability to close browser [not possible]
Phase 2
	Create simple UI that has buttons to send messages
	add geographical info
		can do it using https://developer.mozilla.org/en-US/docs/Web/Security/Secure_Contexts
		requires TLS which pythonanywhere gives for free, but only for their free account.
		requires change in workflow. Instead of icon, you need to go to page. 
		This could be better because it's easier for me to control and deploy new changes.
		is this much better than using life360 to track? i would say no...
			but it is a reasonable feature since life360 takes up so much battery?
Phase 3
	Log in and user info
		Logging in with a user/password is incredibly painful for this audience. Could be a 'register device' thing instead. 
		So for a given device you can set up your info 
		It is going to be much better as an app since you'll  be able to select contacts

		Just like whatsapp, all done with only phone number. Verify phone with pin code sent. But this is because it's an app. When it's a website, you don't know who's accessing. 

		Clearly an app is necessary for this to really work well. In the meantime though, you can create a simple website to see if it's useful. Can do with cookies.

	So flow is:
	Check cookie, if not there, allow registration, else just have buttons. use flask session to control. set timedelta to infinite
	Technically can even store phone numbers inside the session instead of in a database?
	I can restrict to certain numbers just for now so a hacker couldn't get me sending millions of messages.



	
	

Backlog	
	Deploy a second endpoint
	
	Clean code to not have authentication embedded
	Database for logging messages
	add authentication
	

	
	
	Database for adding users
		could use mysql hosted on pythonanywhere - 1GB for free or 5GB for 12/month. To be honest, this is the easiest solution.
		atlas is free for 5GB - this would be good for logging?
		cassandra hosted on the cloud is expensive
		elasticsearch also hosted on big 3
		

Other learnings:
	Databricks certification on their website
	Kubernetes certification on pluralsight

Databases:


Login:
	name
	phone or email

	



	Config for messages
	define_message
	create_user
	get_user
	update_user
	delete_user
	UI for configuring a new user



To deploy:
    check changes into git
    go to pythonanywhere.com and open a bash shell
    git pull -v
    davidisenberg
    copy the token that's on your c:
    in pythonanywhere go to 'web' and reload david.isenberg@pythonanywhere
    



