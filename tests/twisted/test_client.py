import mock
from twisted.trial import unittest
from twisted.internet import defer, reactor
from simplegeo import Record, APIError
from simplegeo.twisted import Client

MY_OAUTH_KEY = 'MY_OAUTH_KEY'
MY_OAUTH_SECRET = 'MY_SECRET_KEY'
TESTING_LAYER = 'TESTING_LAYER'

API_VERSION = '0.1'
API_HOST = 'api.simplegeo.com'
API_PORT = 80

class ClientTest(unittest.TestCase):

    def setUp(self):
        self.client = Client(MY_OAUTH_KEY, MY_OAUTH_SECRET, API_VERSION, API_HOST, API_PORT)

    def fake_request(self, *args, **kwargs):
        d = defer.Deferred()
        reactor.callLater(0, d.callback, mock.sentinel.retval)
        return d
    
    @defer.inlineCallbacks
    def test_add_record_returns_deferred(self):
        self.client._request = mock.Mock(wraps=self.fake_request)
        record = Record(layer=TESTING_LAYER, id=69, lat=34.5, lon=-122.8)
        deferred = self.client.add_record(record)
        self.assertTrue(isinstance(deferred, defer.Deferred))
        retval = yield deferred
        self.assertEquals(mock.sentinel.retval, retval)

    @defer.inlineCallbacks
    def test_add_records_returns_deferred(self):
        self.client._request = mock.Mock(wraps=self.fake_request)
        records = [Record(layer=TESTING_LAYER, id=69, lat=34.5, lon=-122.8), Record(layer=TESTING_LAYER, id=70, lat=34.5, lon=-122.8)]
        deferred = self.client.add_records(TESTING_LAYER, records)
        self.assertTrue(isinstance(deferred, defer.Deferred))
        retval = yield deferred
        self.assertEquals(mock.sentinel.retval, retval)

    @defer.inlineCallbacks
    def test_delete_record_returns_deferred(self):
        self.client._request = mock.Mock(wraps=self.fake_request)
        deferred = self.client.delete_record(TESTING_LAYER, 4)
        self.assertTrue(isinstance(deferred, defer.Deferred))
        retval = yield deferred
        self.assertEquals(mock.sentinel.retval, retval)
        
if __name__ == '__main__':
    import sys
    from twisted.scripts import trial
    sys.argv.extend([sys.argv[0]])
    trial.run()
