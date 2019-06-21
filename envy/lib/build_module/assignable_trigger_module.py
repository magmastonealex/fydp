from abc import abstractmethod

from envy.lib.triggers import Trigger
from envy.lib.docker_manager import ContainerManager

from .build_module import BuildModule


class AssignableTriggerModule(BuildModule):
    """ A Build Module that allows its trigger to be set
    """

    def __init__(self, name: str, container: ContainerManager):
        super(AssignableTriggerModule, self).__init__(name, container)
        self._trigger = None

    def set_trigger(self, trigger: Trigger):
        """ Sets the trigger for this build module

        Arguments:
            trigger {Trigger} -- The trigger
        """
        self._trigger = trigger

    def should_trigger(self) -> bool:
        """ Returns true if a trigger is configured, and that trigger is triggered.

        Returns:
            bool -- The result
        """
        if self._trigger:
            return self._trigger.should_trigger()

        return False

    def persist_trigger(self):
        if self._trigger:
            self._trigger.persist_trigger()

    @abstractmethod
    def run(self):
        super().run()