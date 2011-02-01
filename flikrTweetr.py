#!/usr/bin/python
# -*- encoding: utf-8 -*-

# flikrTweetr.py a tool to update a twitter status on flickr photoset
# updates
# Copyright (C) 2010 Dirk Husemann <dr_who@xyzzyxyzzy.net>

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301 USA.

import anydbm
import ConfigParser
import xml.etree.ElementTree as ET
import flickrapi
import flickrapi.shorturl
import os
import twitter
import optparse

def tweetrUpdate(msg, title, url, dryrun):
    if not dryrun:
        status = tweetr.PostUpdate(msg % dict(title = title, url = url))
    else:
        print msg % dict(title = title, url = url)
    

def getPhotoSetIdForName(targetSet):
    for s in flikr.photosets_getList().findall(".//photoset"):
        if s.findtext("title") == targetSet:
            return s.attrib["id"]
    return None

def initSettings(path):
    if not os.path.exists(settingsDir):
        os.mkdir(settingsDir)
        # --- write config


if __name__ == "__main__":

    # TODO: turn into getopt:
    # --photoset PHOTOSET --message UPDATETEMPLATE --dryrun --catchup

    optParser = optparse.OptionParser()
    optParser.add_option('-p', '--photoset', dest = 'photoset', help = 'name of the flickr photoset', metavar = 'PHOTOSET')
    optParser.add_option('-m', '--message', dest = 'message', 
                         help = 'update message, %(title)s and %(url)s will be substituted for title and short flickr URL',
                         metavar = 'MESSAGE')
    optParser.add_option('-n', '--dry-run', action = 'store_true', dest = 'dryRun', default = False,
                         help = "don't actually update twitter status")
    optParser.add_option('-c', '--catch-up', action = 'store_true', dest = 'catchUp', default = False,
                         help = "catch-up with existing photos in photoset (and don't update twitter status)")
    (options, args) = optParser.parse_args()

    if not options.photoset:
        optParser.error('missing photoset argument')
    if not options.message:
        optParser.error('missing message argument')

    settingsDir = os.path.expanduser('~/.flikrTweetr')
    initSettings(settingsDir)
    cfg = ConfigParser.RawConfigParser()
    cfg.read(['%s/config' % (settingsDir)])

    # --- settings/memory
    if not os.path.exists(settingsDir):
        os.mkdir(settingsDir)
    memory = anydbm.open('%s/%s.db' % (settingsDir, options.photoset), 'c')


    # --- authenticate with flickr    
    flikr = flickrapi.FlickrAPI(cfg.get('flickr', 'apiKey'), cfg.get('flickr', 'apiSecret'))
    flikr.token.path = settingsDir
    (token, frob) = flikr.get_token_part_one(perms='read')
    if not token: raw_input("Press ENTER after you authorized this program")
    flikr.get_token_part_two((token, frob))

    # --- authenticate with twitter
    tweetr = twitter.Api(consumer_key = cfg.get('twitter', 'consumerKey'), consumer_secret = cfg.get('twitter', 'consumerSecret'),
                         access_token_key = cfg.get('twitter', 'accessTokenKey'),
                         access_token_secret = cfg.get('twitter', 'accessTokenSecret'))

    setId = getPhotoSetIdForName(options.photoset)
    setPhotos = flikr.photosets_getPhotos(photoset_id = setId)

    for p in setPhotos.findall(".//photo"):
        id = p.attrib["id"]
        if not id in memory: 
            if not options.dryRun:
                title = p.attrib["title"]
                print 'title: %s' % (title)
                memory[id] = str(title.lower.replace(u'ö', 'oe').replace(u'ü', 'ue').replace(u'ä', 'ae').replace(u'ß', 'ss'))

            tweetrUpdate(options.message, p.attrib["title"], flickrapi.shorturl.url(id), options.dryRun or options.catchUp)

    memory.close()
    

