# ##############################################################################
#  Author: echel0n <echel0n@sickrage.ca>
#  URL: https://sickrage.ca/
#  Git: https://git.sickrage.ca/SiCKRAGE/sickrage.git
#  -
#  This file is part of SiCKRAGE.
#  -
#  SiCKRAGE is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#  -
#  SiCKRAGE is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  -
#  You should have received a copy of the GNU General Public License
#  along with SiCKRAGE.  If not, see <http://www.gnu.org/licenses/>.
# ##############################################################################
import ssl

import pika
from pika.adapters.tornado_connection import TornadoConnection
from pika.adapters.utils.connection_workflow import AMQPConnectorException
from pika.exceptions import StreamLostError, AMQPConnectionError, ChannelWrongStateError
from tornado.ioloop import IOLoop

import sickrage


class AMQPBase(object):
    def __init__(self):
        self._name = 'AMQP'
        self._amqp_host = 'rmq.sickrage.ca'
        self._amqp_port = 5671
        self._amqp_vhost = 'sickrage-app'
        self._connection = None
        self._channel = None
        self._closing = False
        self._consumer_tag = None
        self._prefetch_count = 100

        IOLoop.current().add_callback(self.connect)

    def connect(self):
        # check for api token
        if not sickrage.app.api.token or not sickrage.app.config.general.server_id:
            IOLoop.current().call_later(5, self.reconnect)
            return

        # declare server amqp queue
        if not sickrage.app.api.server.declare_amqp_queue(sickrage.app.config.general.server_id):
            IOLoop.current().call_later(5, self.reconnect)
            return

        # connect to amqp server
        try:
            credentials = pika.credentials.PlainCredentials(username='sickrage', password=sickrage.app.api.token["access_token"])

            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE

            parameters = pika.ConnectionParameters(
                host=self._amqp_host,
                port=self._amqp_port,
                virtual_host=self._amqp_vhost,
                credentials=credentials,
                socket_timeout=300,
                ssl_options=pika.SSLOptions(context)
            )

            TornadoConnection(
                parameters,
                on_open_callback=self.on_connection_open,
                on_close_callback=self.on_connection_close,
                on_open_error_callback=self.on_connection_open_error
            )
        except (AMQPConnectorException, AMQPConnectionError):
            sickrage.app.log.debug("AMQP connection error, attempting to reconnect")
            IOLoop.current().call_later(5, self.reconnect)

    def disconnect(self):
        if self._channel and not self._channel.is_closed:
            try:
                self._channel.close()
            except (ChannelWrongStateError, StreamLostError):
                pass

        if self._connection and not self._connection.is_closed:
            try:
                self._connection.close()
            except (ChannelWrongStateError, StreamLostError):
                pass

        self._channel = None
        self._connection = None

    def on_connection_close(self, connection, reason):
        if not self._closing:
            sickrage.app.log.debug("AMQP connection closed, attempting to reconnect")
            IOLoop.current().call_later(5, self.reconnect)

    def on_connection_open(self, connection):
        self._connection = connection
        self._connection.channel(on_open_callback=self.on_channel_open)

    def on_connection_open_error(self, connection, reason):
        sickrage.app.log.debug("AMQP connection open failed, attempting to reconnect")
        IOLoop.current().call_later(5, self.reconnect)

    def reconnect(self):
        if not self._closing:
            self.connect()

    def on_channel_open(self, channel):
        self._channel = channel

    def stop(self):
        self._closing = True
        self.disconnect()
