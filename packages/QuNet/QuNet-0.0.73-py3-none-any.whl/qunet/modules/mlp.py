﻿import math, copy
import torch, torch.nn as nn

from ..utils   import Config
from .total  import get_activation

#========================================================================================

class MLP(nn.Module):
    def __init__(self,  *args, **kvargs) -> None:
        """
        Fully connected network with one or more hidden layers:
        (B,*, input) -> (B,*, output).

        Args
        ------------
            input (int=None):
                number of inputs > 0
            output (int=None):
                number of outputs > 0
            hidden (int or list = None):
                number of neurons in the hidden layer
            stretch (int = 4):
                if there is, then hidden = int(stretch*input)
            fun (str='gelu'):
                activation function: gelu, relu, sigmoid, tanh, relu6, swish, hswish, hsigmoid
            drop  (float:0.0):
                dropout at the output of the hidden layer

        If there is more than one layer - hidden is a list of the number of neurons in each layer
        There may be no hidden layer: hidden == 0 or == [] or stretch == 0,
        then it's a normal input -> output line layer with no activation function

        Example
        ------------
        ```
            mlp = MLP(input=32, stretch=4, output=1)
            y = mlp( torch.randn(1, 32) )
        ```
        Can be created from config:
        ```
            cfg = MLP.default()
            cfg(input = 3, output = 1)
            mlp = MLP(cfg)
        ```
        And also from the config and key-val arguments:
        ```
            mlp = MLP(cfg, hidden=[128, 512])
        ```
        """
        super().__init__()
        self.cfg = MLP.default()
        self.cfg.set(*args, **kvargs)
        self.create()

    #---------------------------------------------------------------------------

    def default():
        return copy.deepcopy(Config(
            input   = None,     # number of inputs > 0
            output  = None,     # number of outputs > 0
            hidden  = None,     # number of neurons in the hidden layer (int or list)
            stretch = 4,        # if hiddem is None, then hidden = int(stretch*input)
            fun     = 'gelu',   # activation function: gelu, relu, sigmoid, tanh
            drop    =  0,       # dropout at the output of the hidden layer
        ))

    #---------------------------------------------------------------------------

    def forward(self, x):
        x = self.layers(x)
        return x

    #---------------------------------------------------------------------------

    def prepare(self):
        cfg=self.cfg
        assert cfg.input is not None  and cfg.output is not None,  f'MLP: wrong input/output: {cfg.get_str()}'

        if type(cfg.hidden) is list:
            self.neurons = [cfg.input] + cfg.hidden + [cfg.output]
        else:
            if (cfg.hidden is None) and (cfg.stretch is not None):
                cfg.hidden = int(cfg.stretch * cfg.input)

            if cfg.hidden is None or cfg.hidden <= 0:
                self.neurons = [cfg.input, cfg.output]
            else:
                self.neurons = [cfg.input, cfg.hidden, cfg.output]

        if cfg.fun not in ['gelu', 'relu', 'sigmoid', 'tanh', 'relu6', 'swish', 'hswish', 'hsigmoid']:
            print(f"MLP warning: unknown activation function {cfg.fun}, set to gelu")
            cfg.fun  = 'gelu'

    #---------------------------------------------------------------------------

    def create(self):
        self.prepare()
        seq = []
        for i in range (1, len(self.neurons)):
            seq += [ nn.Linear(self.neurons[i-1],  self.neurons[i]) ]
            if i+1 < len(self.neurons):
                seq += [get_activation(self.cfg.fun),
                        nn.Dropout(self.cfg.drop)     ]
        self.layers = nn.Sequential(*seq)

    #---------------------------------------------------------------------------

    def unit_test():
        mlp = MLP(input=32, stretch=4, output=1)
        y = mlp( torch.randn(1, 32) )

        cfg = MLP.default()
        cfg(input = 3, output = 1)
        mlp = MLP(cfg)

        mlp = MLP(cfg, hidden=[128, 512])
        print("ok MLP")
        return True

#========================================================================================

