import random

from emulators.Device import Device
from emulators.Medium import Medium
from emulators.MessageStub import MessageStub


class GossipMessage(MessageStub):

    def __init__(self, sender: int, destination: int, secrets):
        super().__init__(sender, destination)
        # we use a set to keep the "secrets" here
        self.secrets = secrets

    def __str__(self):
        return f'{self.source} -> {self.destination} : {self.secrets}'


class Gossip(Device):

    def __init__(self, index: int, number_of_devices: int, medium: Medium):
        super().__init__(index, number_of_devices, medium)
        # for this exercise we use the index as the "secret", but it could have been a new routing-table (for instance)
        # or sharing of all the public keys in a cryptographic system
        self._secrets = set([index])

    def run(self):
        # the following is your termination condition, but where should it be placed?
        # if len(self._secrets) == self.number_of_devices():
        #    return
        return

    def print_result(self):
        print(f'\tDevice {self.index()} got secrets: {self._secrets}')

class GossipTotalNaive(Device):

    def __init__(self, index: int, number_of_devices: int, medium: Medium):
        super().__init__(index, number_of_devices, medium)
        # for this exercise we use the index as the "secret", but it could have been a new routing-table (for instance)
        # or sharing of all the public keys in a cryptographic system
        self._secrets = set([index])

    def run(self):
        for i in range(self.number_of_devices()):
            if i != self.index():
                self.medium().send(GossipMessage(self.index(), i, self._secrets))

        while True:
            ingoing = self.medium().receive()
            if ingoing is None:
                continue

            self._secrets = self._secrets.union(ingoing.secrets)

            # the following is your termination condition, but where should it be placed?
            if len(self._secrets) == self.number_of_devices():
                return

    def print_result(self):
        print(f'\tDevice {self.index()} got secrets: {self._secrets}')

class GossipTotalOptimal(Device):

    def __init__(self, index: int, number_of_devices: int, medium: Medium):
        super().__init__(index, number_of_devices, medium)
        # for this exercise we use the index as the "secret", but it could have been a new routing-table (for instance)
        # or sharing of all the public keys in a cryptographic system
        self._secrets = set([index])

    def run(self):
        if self.index() != 0:
            self.medium().send(GossipMessage(self.index(), 0, self._secrets))
            
        while True:
            ingoing = self.medium().receive()
            if ingoing is None:
                continue
            
            self._secrets = self._secrets.union(ingoing.secrets)
            
            if len(self._secrets) == self.number_of_devices():
                break
        
        if self.index() == 0:
            for i in range (1, self.number_of_devices()):
                self.medium().send(GossipMessage(self.index(), i, self._secrets))
        
        return

    def print_result(self):
        print(f'\tDevice {self.index()} got secrets: {self._secrets}')


class GossipCircleOptimal(Device):

    def __init__(self, index: int, number_of_devices: int, medium: Medium):
        super().__init__(index, number_of_devices, medium)
        # for this exercise we use the index as the "secret", but it could have been a new routing-table (for instance)
        # or sharing of all the public keys in a cryptographic system
        self._secrets = set([index])

    def run(self):
        if self.index() == 0:
            self.medium().send(GossipMessage(self.index(), 1, self._secrets))
        
        while True:
            ingoing = self.medium().receive()
            if ingoing is None:
                continue
            
            self._secrets = self._secrets.union(ingoing.secrets)
            
            if self.index() == self.number_of_devices() - 2 and len(self._secrets) == self.number_of_devices():
                return
            
            self.medium().send(GossipMessage(self.index(), (self.index() + 1) % self.number_of_devices(), self._secrets))
            
            if len(self._secrets) == self.number_of_devices():
                return

    def print_result(self):
        print(f'\tDevice {self.index()} got secrets: {self._secrets}')
