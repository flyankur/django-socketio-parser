from socketio.namespace import BaseNamespace
from socketio.mixins import RoomsMixin, BroadcastMixin
from gevent_scraper_parser.views import scrapeData
import jsbeautifier


class Namespace(BaseNamespace, RoomsMixin, BroadcastMixin):

    def emit_to_me(self, event, *args):
        pkt = dict(
             type="event",
             name=event,
             args=args,
             endpoint=self.ns_name)
        self.socket.send_packet(pkt)

    def on_url(self,data):
        print data
        print data['url']
        result_json = scrapeData(data['url'],data['webpage'])
        res = jsbeautifier.beautify(result_json)
        self.emit_to_me('msg_to_user', res)