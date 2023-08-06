from pdb import set_trace as T

from abc import ABC, abstractmethod

import torch
import torch.nn as nn


class Policy(torch.nn.Module, ABC):
    def __init__(self, binding):
        '''Pure PyTorch base policy
        
        This spec allows PufferLib to repackage your policy
        for compatibility with RL frameworks

        encode_observations -> decode_actions is PufferLib's equivalent of PyTorch forward
        This structure provides additional flexibility for us to include an LSTM
        between the encoder and decoder.

        To port a policy to PufferLib, simply put everything from forward() before the
        recurrent cell (or, if no recurrent cell, everything before the action head)
        into encode_observations and put everything after into decode_actions.

        You can delete the recurrent cell from forward(). PufferLib handles this for you
        with its framework-specific wrappers. Since each frameworks treats temporal data a bit
        differently, this approach lets you write a single PyTorch network for multiple frameworks.

        Specify the value function in critic(). This is a single value for each batch element.
        It is called on the output of the recurrent cell (or, if no recurrent cell,
        the output of encode_observations)

        Args:
            binding: A pufferlib.emulation.Binding object
        '''
        super().__init__()
        self.binding = binding

    @abstractmethod
    def critic(self, hidden):
        '''Computes the value function from the hidden state
        
        Returns a single value for each batch element'''
        raise NotImplementedError

    @abstractmethod
    def encode_observations(self, flat_observations):
        '''Encodes a batch of observations into hidden states

        Call pufferlib.emulation.unpack_batched_obs at the start of this
        function to unflatten observations to their original structured form:

        observations = pufferlib.emulation.unpack_batched_obs(
            self.binding.raw_single_observation_space, env_outputs)
 
        Args:
            flat_observations: A tensor of shape (batch, ..., obs_size)

        Returns:
            hidden: Tensor of (batch, ..., hidden_size)
            lookup: Tensor of (batch, ...) that can be used to return additional embeddings
        '''
        raise NotImplementedError

    @abstractmethod
    def decode_actions(self, flat_hidden, lookup):
        '''Decodes a batch of hidden states into multidiscrete actions

        Args:
            flat_hidden: Tensor of (batch, ..., hidden_size)
            lookup: Tensor of (batch, ...), if returned by encode_observations

        Returns:
            actions: Tensor of (batch, ..., action_size)

        actions is a concatenated tensor of logits for each action space dimension.
        It should be of shape (batch, ..., sum(action_space.nvec))'''
        raise NotImplementedError

class Default(Policy):
    def __init__(self, binding, input_size=256, hidden_size=256):
        '''Default PyTorch policy, meant for debugging.
        This should run with any environment but is unlikely to learn anything.
        
        Uses a single linear layer to encode observations and a list of
        linear layers to decode actions. The value function is a single linear layer.
        '''
        super().__init__(binding)
        self.encoder = nn.Linear(self.binding.single_observation_space.shape[0], hidden_size)
        self.decoders = nn.ModuleList([nn.Linear(hidden_size, n)
                for n in self.binding.single_action_space.nvec])
        self.value_head = nn.Linear(hidden_size, 1)

    def critic(self, hidden):
        '''Linear value function'''
        return self.value_head(hidden)

    def encode_observations(self, env_outputs):
        '''Linear encoder function'''
        return self.encoder(env_outputs), None

    def decode_actions(self, hidden, lookup, concat=True):
        '''Concatenated linear decoder function'''
        actions = [dec(hidden) for dec in self.decoders]
        if concat:
            return torch.cat(actions, dim=-1)
        return actions
