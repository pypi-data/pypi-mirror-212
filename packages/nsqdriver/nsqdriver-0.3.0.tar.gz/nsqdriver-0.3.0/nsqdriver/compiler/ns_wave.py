import copy
from typing import Union, List, Dict
from itertools import chain, repeat
from enum import IntEnum
from collections import namedtuple

import numpy as np
import waveforms as wf

from .py_wave_asm import *


class QInsPlaceholder(NSQCommand):
    ...


class Wave(GenTagMixin):
    Identity = namedtuple('Relation', ['frame', 'envelop'])

    class Tag(IntEnum):
        none = 0
        frame = 1
        envelope = 2
        signal = 3

    def __init__(self, ins_obj: "InstructionQ", ins_id: dict):
        cls = self.__class__
        self.instruction = ins_obj
        self.id = cls.Identity(**ins_id)
        if ins_id['frame'] != -1 and ins_id['envelop'] != -1:
            self.wtag = cls.Tag.signal
        elif ins_id['frame'] != -1:
            self.wtag = cls.Tag.envelope
        elif ins_id['envelop'] != -1:
            self.wtag = cls.Tag.frame
        else:
            self.wtag = cls.Tag.none

    def __repr__(self):
        return f'<{self.__class__}::{self.id}::{self.wtag}>'


class Frame(Wave):
    def __init__(self, ins_obj: "InstructionQ", ins_id: int, freq: float):
        super().__init__(ins_obj, {'frame': ins_id, 'envelop': -1})
        self.tag = self.generate_tag
        self.freq = freq

    @property
    def freq(self):
        return self._freq

    @freq.setter
    def freq(self, value):
        self._freq = value
        self._ins = QInsFrame(freq=value, tag=self.tag)

    def __mul__(self, other: Wave):
        if isinstance(other, Envelope) or isinstance(other, Signal):
            if other.instruction is not self.instruction:
                raise ValueError(f'隶属于的instruction不同，不能直接相乘')
            res = Signal(self.instruction, {'frame': self.id.frame, 'envelop': other.id.envelop})
            res.frame = self
            res.envelope = other
            return res
        else:
            raise ValueError(f'{self.__class__}不能与{other.__class__}做乘法运算')

    def format(self):
        return self._ins


class Envelope(Wave):
    def __init__(self, ins_obj: "InstructionQ", ins_id: int, content):
        super().__init__(ins_obj, {'frame': -1, 'envelop': ins_id})
        self.tag = self.generate_tag
        self.content = content

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, value):
        self._content = value
        self._ins = QInsEnvelop(envelop=self.content, tag=self.tag)

    def __mul__(self, other: Wave):
        if isinstance(other, Frame) or isinstance(other, Signal):
            if other.instruction is not self.instruction:
                raise ValueError(f'They belong to different instructions and cannot be directly multiplied')
            res = Signal(self.instruction, {'frame': other.id.frame, 'envelop': self.id.envelop})
            res.frame = other
            res.envelope = self
            return res
        else:
            raise ValueError(f'{self.__class__}不能与{other.__class__}做乘法运算')

    def format(self):
        return self._ins


class Signal(Wave):
    def __init__(self, ins_obj: "InstructionQ", ins_id: dict):
        super().__init__(ins_obj, ins_id)
        self.frame = None
        self.envelope = None


class InstructionQ(GenTagMixin):
    """!
    包含各种具体的指令
    """

    def __init__(self, freqs=None, envelopes=None):
        """!

        @param freqs:
        @param envelopes:
        """
        if freqs is None:
            freqs = []
        if envelopes is None:
            envelopes = []
        self.i_set: "List[Union[NSQCommand, InstructionQ]]" = []
        self.f_set: "Dict[int, Frame]" = {}
        self.e_set: "Dict[int, Envelope]" = {}
        self.symbol_set: Dict[str, int] = {}
        self.symbol_idx = -1
        self.is_first_trig = True
        self.last_ins = None

        for i, f in enumerate(freqs):
            self.ins_frame(f)
        for i, e in enumerate(envelopes):
            self.ins_envelope(e)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        ...

    def clear(self):
        self.i_set.clear()
        self.symbol_set: Dict[str, int] = {}
        self.symbol_idx = -1
        self.is_first_trig = True

    @property
    def length(self):
        return len(self.i_set)

    def ins_frame(self, freq, idx=None) -> Frame:
        raise RuntimeError(f'Cannot create a new frame in the branch')

    def ins_envelope(self, envelope: "Union[np.ndarray, wf.Waveform, str]", idx=None) -> Envelope:
        raise RuntimeError(f'Cannot create a new envelope in the branch')

    def evlp_gaussian(self, width) -> Envelope:
        wave = wf.gaussian(width) >> (width/2)
        wave.start = 0
        wave.stop = width
        return self.ins_envelope(wave)

    def evlp_cospulse(self, width) -> Envelope:
        wave = wf.cosPulse(width) >> (width / 2)
        wave.start = 0
        wave.stop = width
        return self.ins_envelope(wave)

    def evlp_square(self, width) -> Envelope:
        wave = wf.square(width) >> (width / 2)
        wave.start = 0
        wave.stop = width
        return self.ins_envelope(wave)

    def _append_ins(self, cmd: "Union[NSQCommand, InstructionQ]"):
        self.last_ins = cmd
        self.i_set.append(cmd)

    def _map_var(self, var):
        if var in self.symbol_set:
            return self.symbol_set[var]
        self.symbol_idx += 1
        if self.symbol_idx >= 16:
            raise RuntimeError(f'Up to 16 variables can be configured')
        self.symbol_set[var] = self.symbol_idx
        return self.symbol_set[var]

    def wait_for_trigger(self):
        if not self.is_first_trig:
            self.wait()
        cmd = QInsWaitTrig(tag=self.generate_tag)
        self._append_ins(cmd)
        return cmd

    def ins_variable(self, reg: str, value: int):
        cmd = QInsMov(self._map_var(reg), value, type='=', tag=self.generate_tag)
        self._append_ins(cmd)
        return cmd

    def ins_add(self, reg: str, value: int):
        cmd = QInsMov(self._map_var(reg), value, type='+', tag=self.generate_tag)
        self._append_ins(cmd)
        return cmd

    def ins_reset_frame(self, flag, frame=''):
        cmd = QInsResetF(flag, frame, tag=self.generate_tag)
        self._append_ins(cmd)
        return cmd

    def inc_phase(self, frame, phase):
        cmd = QInsIncPhase(phase, frame.tag, tag=self.generate_tag)
        self._append_ins(cmd)
        return cmd

    def play_wave(self, wave: Signal, amp=1, freq=0, phase=0):
        if not isinstance(wave, Signal):
            raise RuntimeError(f'The parameter wave should be Signal, not {type(wave)}')
        cmd = QInsPlayWave(wave.frame.tag, wave.envelope.tag, amp, freq, phase, tag=self.generate_tag)
        self._append_ins(cmd)
        return cmd

    def play_zero(self, width):
        cmd = QInsPlayZero(width, tag=self.generate_tag)
        self._append_ins(cmd)
        return cmd

    def wait(self):
        cmd = QInsWait(tag=self.generate_tag)
        self._append_ins(cmd)
        return cmd

    def end(self):
        cmd = QInsEnd(tag=self.generate_tag)
        self._append_ins(cmd)
        return cmd

    def capture(self, width, delay=0):
        cmd = QInsCapture(width=width, probe_delay=delay, tag=self.generate_tag)
        self._append_ins(cmd)
        return cmd

    def _compile(self) -> "List[NSQCommand]":
        res = []
        for ins in self.i_set:
            if isinstance(ins, InstructionQ):
                res.extend(ins._compile())
            else:
                res.append(copy.copy(ins))
        return res

    def compile(self) -> "List[NSQCommand]":
        queue = []
        for idx in sorted(self.f_set.keys()):
            ins = self.f_set[idx]
            queue.append(ins.format())
        for idx in sorted(self.e_set.keys()):
            ins = self.e_set[idx]
            queue.append(ins.format())

        queue.extend(self._compile())
        # 向指令队列中添加End指令
        if not isinstance(queue[-1], QInsEnd):
            queue.append(self.end())

        res = []
        for idx, ins in enumerate(queue):
            if isinstance(ins, QInsPlaceholder):
                f_tag = ins.tag
                t_tag = queue[idx+1].tag
                for _ins in queue:
                    if getattr(_ins, 'target', '') == f_tag:
                        _ins.target = t_tag
                continue
            res.append(ins)
        return res

    def lookup(self):
        import json
        ins_list = [str(ins) for ins in self.compile()]
        print(json.dumps(ins_list, indent=4))


class InsChannel(InstructionQ):
    def __init__(self, freqs=None, envelopes=None):
        super(InsChannel, self).__init__(freqs, envelopes)
        self.if_stack: "List[InsIF]" = []
        self.looping = False

    def clear(self):
        super().clear()
        self.looping = False

    def ins_frame(self, freq, idx=None) -> Frame:
        if idx is None:
            idx = sorted(self.f_set)[-1]+1 if len(self.f_set) != 0 else 0
        if not isinstance(idx, int):
            raise ValueError(f'frame的idx应为整数，而不是{type(idx)}')
        frame = Frame(self, idx, freq)
        self.f_set[idx] = frame
        return frame

    def ins_envelope(self, envelope: "Union[np.ndarray, wf.Waveform, str]", idx=None) -> Envelope:
        if idx is None:
            idx = sorted(self.e_set)[-1] + 1 if len(self.e_set) != 0 else 0
        if not isinstance(idx, int):
            raise ValueError(f'envelop的idx应为整数，而不是{type(idx)}')
        obj = Envelope(self, idx, envelope)
        self.e_set[idx] = obj
        return obj

    def ins_if(self, formula) -> "InsIF":
        channel = self if self.__class__ is InsChannel else self.channel
        if_ins = InsIF.from_channel(channel)
        if_ins.formula = formula
        self._append_ins(if_ins)
        self.if_stack.append(if_ins)
        return if_ins

    def ins_else(self) -> "InsElse":
        # if与else之间不能间隔其它指令
        if not isinstance(self.last_ins, InsIF):
            raise RuntimeError(f'The last call of ins_else must be ins_if, not {type(self.last_ins)}')
        # 不能没有if直接调用else
        if len(self.if_stack) == 0:
            raise RuntimeError(f'Please call if before calling else')
        channel = self if self.__class__ is InsChannel else self.channel
        _if = self.if_stack.pop()
        _else = InsElse.from_channel(channel)
        _else._if = _if
        _if.ins_else = _else
        return _else

    def ins_loop(self, times) -> "InsLoop":
        if self.looping:
            raise RuntimeError(f'The current object is already in the loop')
        channel = self if self.__class__ is InsChannel else self.channel
        loop_ins = InsLoop.from_channel(channel)
        loop_ins.times = times
        self._append_ins(loop_ins)
        return loop_ins


class InsIF(InsChannel):
    ch_judge_name = {f'FREQ_{i}': 1<<i for i in range(6)}

    def __init__(self, freqs=None, envelopes=None):
        """!

        @param freqs:
        @param envelopes:
        """
        super().__init__(freqs, envelopes)
        self.channel: "InsChannel" = None
        self.key_ins = None
        self.ins_else = None

    @classmethod
    def from_channel(cls, channel):
        self = cls()
        self.channel = channel
        return self

    @property
    def formula(self):
        raise RuntimeError(f'{self.__class__.__name__}.formula is a static property')

    @formula.setter
    def formula(self, formula: str):
        formula = formula.replace(' ', '')
        ast = formula.split('==')
        if len(ast) != 2:
            raise RuntimeError(f'The format of formula should be [name] == [value]')
        name, value = ast
        if name in self.channel.symbol_set:
            self.key_ins = QInsJumpWithReg(self.channel.symbol_set[name], int(value), None, tag=self.generate_tag)
        elif name in self.ch_judge_name:
            self.key_ins = QInsJumpWithJudge(int(value), self.ch_judge_name[name], None, tag=self.generate_tag)
        else:
            raise RuntimeError(f'The specified variable {name} does not exist')

    def _compile(self) -> "List[NSQCommand]":
        """!
        递归生成分支结构，支持结构嵌套
        @return:
        """
        res = []
        if_group = super()._compile()
        else_group = self.ins_else._compile() if isinstance(self.ins_else, InsElse) else []
        while len(else_group) < 3:
            else_group.append(QInsWait(tag=self.generate_tag))
        if_group.append(QInsPlaceholder(tag=self.generate_tag))
        jump = QInsJump(None, tag=self.generate_tag)
        self.key_ins.target = if_group[0].tag
        jump.target = if_group[-1].tag

        res.append(self.key_ins)
        res.extend(else_group)
        res.append(jump)
        res.extend(if_group)
        return res

    def capture(self, width, delay=0):
        raise RuntimeError(f'Capture is not allowed to call in a branch structure')


class InsElse(InsChannel):
    def __init__(self, freqs=None, envelopes=None):
        """!

        @param freqs:
        @param envelopes:
        """
        super().__init__(freqs, envelopes)
        self.channel = None
        self._if = None

    @classmethod
    def from_channel(cls, channel):
        self = cls()
        self.channel = channel
        return self

    def capture(self, width, delay=0):
        raise RuntimeError(f'Capture is not allowed to call in a branch structure')


class InsLoop(InsChannel):
    def __init__(self, freqs=None, envelopes=None):
        """!

        @param freqs:
        @param envelopes:
        """
        super().__init__(freqs, envelopes)
        self.channel: "InsChannel" = None
        self.times = None
        self.var = self.generate_tag

    def __enter__(self):
        self.channel.looping = True
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.looping = False

    @classmethod
    def from_channel(cls, channel):
        self = cls()
        self.channel = channel
        return self

    def capture(self, width, delay=0):
        raise RuntimeError(f'Calling capture in a loop construct is not allowed')

    def _compile(self) -> "List[NSQCommand]":
        body = super()._compile()
        res = []
        set_cmd = QInsMov(self.channel._map_var(self.var), 0, type='=', tag=self.generate_tag)
        body.append(QInsMov(self.channel._map_var(self.var), 1, type='+', tag=self.generate_tag))
        placeholder = QInsPlaceholder(tag=self.generate_tag)
        jump = [
            QInsJumpWithReg(self.channel._map_var(self.var), self.times, placeholder.tag, tag=self.generate_tag),
            QInsWait(tag=self.generate_tag),
            QInsWait(tag=self.generate_tag),
            QInsJump(body[0].tag, tag=self.generate_tag),
            placeholder
        ]
        res.append(set_cmd)
        res.extend(body)
        res.extend(jump)
        return res

    # def _compile(self) -> "List[NSQCommand]":
    #     ins_list = super()._compile()
    #     res = []
    #     for ins in chain.from_iterable(repeat(ins_list, self.times)):
    #         _ins: "NSQCommand" = copy.copy(ins)
    #         _ins.tag = self.generate_tag
    #         res.append(_ins)
    #     return res
