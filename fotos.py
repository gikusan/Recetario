from google.appengine.api import users
from google.appengine.ext import blobstore
from google.appengine.ext import ndb
from google.appengine.ext.webapp import blobstore_handlers
from Estructuras.Recetas import Receta
import webapp2


class ViewPhotoHandler(blobstore_handlers.BlobstoreDownloadHandler):
    def get(self):
        receta_key = self.request.get('id')
        r = Receta.get_by_id(int(receta_key))
        if not r:
            return abort(404)
        else:
            if not blobstore.get(r.blob_key):
                return abort(404)
            else:
                self.send_blob(r.blob_key)


app = webapp2.WSGIApplication([
    ('/view_photo', ViewPhotoHandler)
], debug=True)