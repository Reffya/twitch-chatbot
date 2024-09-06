from abc import abstractmethod

"""Common interface for defining an activity, an activity can be started using a command and will listen to every message received during its lifetime. To function properly it needs
to be hooked to the event_message event and the start()"""
class Activity:
    @abstractmethod
    def start():
        pass


    @abstractmethod
    def on_message(message):
        pass

    @abstractmethod
    def kill():
        pass

    @abstractmethod
    def is_finished():
        pass