import cStringIO
import logging

from google.appengine.ext.webapp.mail_handlers import InboundMailHandler
from google.appengine.api import urlfetch
from poster.encode import multipart_encode, MultipartParam
import webapp2

class LogSenderHandler(InboundMailHandler):
    def receive(self, mail_message):
        logging.info("Received a message from: " + mail_message.sender)
        plaintext_bodies = mail_message.bodies('text/plain')
        html_bodies = mail_message.bodies('text/html')

        for content_type, body in html_bodies:
            decoded_html = body.decode()
            # ...
            logging.info("Html body of length %d.", len(decoded_html))
        for content_type, body in plaintext_bodies:
            plaintext = body.decode()
            logging.info("Plain text body of length %d.", len(plaintext))

        logging.info("Attachments # %d.", len(mail_message.attachments))
        for attachment in mail_message.attachments:
            logging.info("Attachment filename: %s", attachment.filename)
            logging.info("Attachment payload.size: %s", len(attachment.payload.decode()))
            send_photo(attachment.payload.decode(), attachment.filename, mail_message.subject)

def send_photo(data, filename, caption):
    logging.info("Sending photo: %s", filename)
    payload = {}
    payload['userId'] = 'test'
    payload['caption'] = caption
    payload['photoFile'] = MultipartParam('photoFile', filename=filename, filetype='image/jpeg', fileobj=cStringIO.StringIO(data))

    data, headers = multipart_encode(payload)
    urlfetch.fetch(url='https://friggr.unlessquit.com/inbox', method=urlfetch.POST, payload="".join(data), headers=headers)

app = webapp2.WSGIApplication([LogSenderHandler.mapping()], debug=True)
