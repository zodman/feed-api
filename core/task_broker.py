from dramatiq.brokers.redis import RedisBroker
import dramatiq

broker = RedisBroker(host="redis")
dramatiq.set_broker(broker)
