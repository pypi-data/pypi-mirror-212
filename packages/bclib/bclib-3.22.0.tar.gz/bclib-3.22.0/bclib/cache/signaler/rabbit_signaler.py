from typing import Callable
import json
import asyncio
from ..signaler.base_signaler import BaseSignaler
from bclib.utility import DictEx

class RabbitSignaller(BaseSignaler):
    """Implement rabbit-mq signaler"""
    def __init__(self, reset_cache_callback:"Callable", options:"DictEx") -> None:
        super().__init__(reset_cache_callback, options)
        import pika
        try:
            param = pika.URLParameters(options.url)
            queue_name = options.queue
            connection = pika.BlockingConnection(param)
            channel = connection.channel()
            channel.queue_declare(queue=queue_name)

            def on_rabbit_message_received(channel, method, properties, body):
                print(
                    f"Message received from {param.host}:{queue_name} ({body})")
                try:
                    cmd = json.loads(body)
                    if cmd and "type" in cmd:
                        cmd_type = cmd["type"]
                        if cmd_type == "clear-cache" and "keys" in cmd:
                            keys = cmd["keys"]
                            self._callback(keys)

                except Exception as ex:
                    print(f"""
                        error in process received message from rabbit in {param.host}:{queue_name} ({ex})
                    """)

            channel.basic_consume(
                queue=queue_name, on_message_callback=on_rabbit_message_received, auto_ack=True)

            print(f'Waiting for messages from {param.host}:{queue_name}.')
            loop = asyncio.get_running_loop()
            loop.run_in_executor(None, channel.start_consuming)
        except Exception as ex:
            print(f"Error in config rabbit-mq ({ex})")
            raise ex
