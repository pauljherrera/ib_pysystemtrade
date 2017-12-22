class Subscriber:
    def __init__(self, name, *args, **kwargs):
        super().__init__()
        self.name = name

    def update(self, message):
        # start new Thread in here to handle any task
#        print('\n\n {} got message "{}"'.format(self.name, message))
        pass
        
class Publisher:
    def __init__(self, events, *args, **kwargs):
        # maps event names to subscribers
        # str -> dict
        super().__init__()
        self.events = { event : dict()
                          for event in events }
                          
    def get_subscribers(self, event):
        return self.events[event]

    def get_events(self):
        return self.events
                
    def register(self, event, channel):
        self.get_subscribers(event)[channel] = channel.update

    def unregister(self, event, channel):
        del self.get_subscribers(event)[channel]

    def dispatch(self, event, message):
        for subscriber, callback in self.get_subscribers(event).items():
            callback(message)

