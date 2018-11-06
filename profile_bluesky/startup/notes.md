
# normal start of Bluesky (from any shell)

	use_bluesky.sh

This is your typical scan command in python

    RE(user_plan(2, 3, 1, 5, 0.5, "this is a test sample"), mca_writer_callback.receiver)


===============================================================

or --- use bash shell when running Bluesky

	dy% bash

make sure the Bluesky python is the default by activating its conda environment

	bash-4.2$ source /APSshare/anaconda3/BlueSky/bin/activate base
	(base) bash-4.2$ which python
	/APSshare/anaconda3/x86_64/bin/python

IPython configuration files are in `~/.ipython/profile_bluesky/startup`


===============================================================

## saving / pushing to GitHub

1. **before** you make any changes, sync with github using:  `git pull`
1. make changes in files in this directory
1. run this command: `gitk &`
1. in *gitk*, select menu `File`, then `Start git gui`
1. write a comment about the commit you will make
1. stage the file(s) to be committed - click on them one by one
1. press the **commit** button
1. repeat for any remaining files with different comments
1. press the **push** button
1. press the **push** button again -- ignore all the content on this screen, we won't change it
1. type GitHub user name (if asked)
1. type GitHub password (if asked)
1. if all goes well, you will see green in the next screen, otherwise red and time to ask for help


================================================================

## To generate EPICS PVs for signaling to Bluesky

See https://github.com/APS-3ID-IXN/ipython-s3blue/issues/5


