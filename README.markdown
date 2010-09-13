# flikrTweetr.py

flikrTweetr.py is a simple python script to check a flickr photoset
for new photos and update a twitter status when a new photo is found.

## dependencies

flikrTweetr.py depends on 
* flickrapi
* python-twitter (0.8-dev and later)

## setup

flikrTweetr.py currently requires a crontab entry to be regularly
invoked:

<pre>
*/5 * * * *	flikrTweetr.py -p droidpix -m "new droidpix: %(title)s %(url)s"
</pre>

flikrTweetr.py needs to authenticate through OAuth with both twitter and flickr.
