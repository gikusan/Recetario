from google.appengine.api import users
from google.appengine.ext import blobstore
from google.appengine.ext import ndb
from google.appengine.ext.webapp import blobstore_handlers
import webapp2


# This datastore model keeps track of which users uploaded which photos.
class UserPhoto(ndb.Model):
    user = ndb.StringProperty()
    blob_key = ndb.BlobKeyProperty()


class PhotoUploadFormHandler(webapp2.RequestHandler):
    def get(self):
        upload_url = blobstore.create_upload_url('/upload_photo')
        # To upload files to the blobstore, the request method must be "POST"
        # and enctype must be set to "multipart/form-data".
        self.response.out.write("""
<html><body>
<form action="{0}" method="POST" enctype="multipart/form-data">
  Upload File: <input type="file" name="file"><br>
  <input type="submit" name="submit" value="Submit">
</form>
</body></html>""".format(upload_url))


class PhotoUploadHandler(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        try:
            upload = self.get_uploads()[0]
            user_photo = UserPhoto(
                user=users.get_current_user().user_id(),
                blob_key=upload.key())
            user_photo.put()

            self.redirect('/view_photo/%s' % upload.key())

        except:
            self.error(500)


class ViewPhotoHandler(blobstore_handlers.BlobstoreDownloadHandler):
    def get(self):
        # Para obtener la imagen /view_photo?id=[key]
        #image_key = "LHYPafajwvN46YNi2fBE3w=="
        image_key = self.request.get('id')

        if image_key:
            if not blobstore.get(image_key):
                self.error(404)
            else:
                self.send_blob(image_key)
        else:
            self.error(404)


app = webapp2.WSGIApplication([
    ('/photo', PhotoUploadFormHandler),
    ('/upload_photo', PhotoUploadHandler),
    ('/view_photo', ViewPhotoHandler),
], debug=True)