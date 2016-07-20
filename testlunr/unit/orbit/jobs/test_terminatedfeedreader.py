# Copyright (c) 2011-2016 Rackspace US, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import unittest

from lunr.common.config import LunrConfig
from lunr.db.models import Error, Audit, Event, Marker
from lunr.common import cloudfeedclient
from lunr.cinder import cinderclient
from lunr import db
from lunr.orbit.jobs import terminatedfeedreader
from lunr.orbit.jobs.terminatedfeedreader import TerminatedFeedReader

# Test the cloud feed client connection
# Test the cinder client connection
# Test logger to db

class TestTerminatedFeedReader(unittest.TestCase):
    def setUp(self):
        self.conf = LunrConfig({'db': {'auto_create': True,
                                       'url': 'sqlite://'}})
        self.sess = db.configure(self.conf)
        self.reader = TerminatedFeedReader(self.conf, self.sess)

    #def test_run(self):
    #    self.reader.run()

    def test_log_to_db_empty_event(self):
        error_msg = "Test Exception"
        self.reader.log_error_to_db(Exception(error_msg))
        obj = self.sess.query(Error).filter(Error.message == error_msg).first()
        self.assertEqual(obj.message, error_msg)
        self.assertEqual(obj.event_id, None)
        self.assertEqual(obj.tenant_id, None)

    def test_log_to_db_with_event(self):
        error_msg = "Test Exception"
        event = Event({
            'tenant_id': '123',
            'id': '345',
        })
        self.reader.log_error_to_db(Exception(error_msg), event)
        obj = self.sess.query(Error).filter(Error.message == error_msg).first()
        self.assertEqual(obj.message, error_msg)
        self.assertEqual(obj.tenant_id, event['tenantId'])
        self.assertEqual(obj.event_id, event['id'])


if __name__ == '__main__':
    unittest.main()