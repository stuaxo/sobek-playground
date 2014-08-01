import json
import urllib.request
import urllib.error


# This global variable MUST be set before any of the subsequent
# code will work. I won't put my own in here because it'd just
# get abused.
# TODO: This is a stupid way to handle this. But then again, this
# entire file is quick hack.
CLIENT_ID = None


# API Reference: http://api.imgur.com/endpoints/gallery
# API Reference: http://api.imgur.com/endpoints/gallery#subreddit
# https://api.imgur.com/3/gallery/{section}/{sort}/{page}
# https://api.imgur.com/3/gallery/r/{subreddit}/{sort}/{page}
class Gallery(object):
    BASE_URL = "https://api.imgur.com/3/gallery"

    def __init__(self):
        object.__init__(self)

    # X-RateLimit-UserLimit       Total credits that can be allocated.
    # X-RateLimit-UserRemaining   Total credits available.
    # X-RateLimit-UserReset       Timestamp (unix epoch) for when the credits
    #                             will be reset.
    # X-RateLimit-ClientLimit     Total credits that can be allocated for the
    #                             application in a day.
    # X-RateLimit-ClientRemaining Total credits remaining for the application
    #                             in a day.
    def get_json_from_url(self, url):
        data = ""
        req = urllib.request.Request(url, None, {
            "Authorization": "Client-ID %s" % CLIENT_ID
        })

        res = urllib.request.urlopen(req)

        # A handy bit of data. :)
        # print(res.info().get("X-RateLimit-UserRemaining"))

        data = res.read().decode()

        return json.loads(data)

    # section: hot, top, user
    # sort: viral, time
    # page: integer
    def load(self, section="hot", sort="viral", page=0):
        url = self.BASE_URL + "".join("/%s" % i for i in (section, sort, page))
        data = self.get_json_from_url("%s.json" % url)

        self.images = [i for i in data["data"] if not i["is_album"]]
        self.albums = [a for a in data["data"] if a["is_album"]]


class RedditGallery(Gallery):
    BASE_URL = "https://api.imgur.com/3/gallery/r"

    def __init__(self):
        Gallery.__init__(self)

    def load(self, subreddit, sort="hot", page=0):
        url = self.BASE_URL + "".join("/%s" % i for i in (
            subreddit,
            sort,
            page
        ))

        data = self.get_json_from_url("%s.json" % url)

        self.images = [i for i in data["data"]]

# API Reference: http://api.imgur.com/models/gallery_image
# class GalleryImage

# API Reference: http://api.imgur.com/models/gallery_album
# class GalleryAlbum

# API Reference: http://api.imgur.com/models/image
# https://api.imgur.com/3/image/{id}/
# class Image
