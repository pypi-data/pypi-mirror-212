import struct
import copy
import uuid
from typing import Union, List, Tuple, Dict
from enum import IntEnum
from dataclasses import dataclass, field
from itertools import chain
from collections import ChainMap

import numpy as np
import waveforms as wf

__all__ = [
    'AssemblyError', 'GenTagMixin', 'Assembler', 'NSQCommand',
    'QInsWait', 'QInsWaitTrig', 'QInsEnd', 'QInsFrame', 'QInsEnvelop',
    'QInsJumpWithJudge', 'QInsJump', 'QInsJumpWithReg', 'QInsCapture',
    'QInsMov', 'QInsIncPhase', 'QInsPlayZero', 'QInsPlayWave', 'QInsResetF',
]

global_config = {
    'play_zero_step': 4e-9,
    'OUTSrate': 8e9,
    'envelope_dtype': np.int16,  # 描述包络每个点的数据类型
    'envelope_step': 64,  # 包络步进粒度，单位为bytes
    'envelope_quant': 16383,  # 包络量化范围
    'envelope_cache': 204800,  # 包络缓存大小，单位bytes
    'envelope_head': np.array([2, 0, 0, 512, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=np.int16),   # 包络更新包头
}


class AssemblyError(RuntimeError):
    ...


class GenTagMixin:
    @property
    def generate_tag(self):
        return uuid.uuid4().hex[:10]


@dataclass
class NSQCommand:
    """!
    所有参数化波形指令队列的基类
    """
    tag: str = field(kw_only=True)

    def _check_attr(self):
        ...

    def __bytes__(self):
        self._check_attr()
        cmd = self._pack_cmd()
        return self.list2bytes(cmd)

    def _pack_cmd(self) -> list:
        return [0x00, 0, 0, 0x00000000, 0x0000, 0x0000, 0x0000, 0x00000000, 0x00000000]

    @property
    def overhead(self):
        return 16e-9

    @staticmethod
    def list2bytes(cmd: list):
        cmd += [0x00] * 8
        cmd_raw = struct.pack('=BBIIHHHII' + 'B' * 8, *cmd)
        return cmd_raw

    @staticmethod
    def frequency_normalization32(freq) -> np.uint32:
        return np.uint32(round(freq / global_config['OUTSrate'] * (1 << 32)))

    @staticmethod
    def phase_normalization32(phase) -> np.uint32:
        return np.uint32(round(np.fmod(np.fmod(phase / np.pi / 2, 1) + 1, 1) * (1 << 32)))


@dataclass
class _ProbeCommand:
    tag: str = field(kw_only=True)

    def _check_attr(self):
        ...

    def __bytes__(self):
        self._check_attr()
        cmd = self._pack_cmd()
        return self.list2bytes(cmd)

    def _pack_cmd(self) -> list:
        return [0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000]

    @property
    def overhead(self):
        return 16e-9

    @staticmethod
    def list2bytes(cmd: list):
        cmd_raw = struct.pack('=HHHHHHHH', *cmd[::-1])
        return cmd_raw


@dataclass
class QInsEnvelop(NSQCommand):
    envelop: Union[np.ndarray, wf.Waveform]

    def __post_init__(self):
        self.envelop_slice = slice(0, None, 1)

    def __bytes__(self):
        if isinstance(self.envelop, wf.Waveform):
            if self.envelop.start is None or self.envelop.stop is None:
                raise AssemblyError(f'When the type of {self.__class__.__name__}.envelop is wf.Waveform, '
                                    f'it must have start and stop attributes')
            wave = self.envelop.sample(global_config['OUTSrate'])
        elif isinstance(self.envelop, np.ndarray):
            wave = self.envelop
        else:
            raise AssemblyError(f'The type of {self.__class__.__name__}.envelop must be one of np.ndarray or wf.Waveform')
        wave *= global_config['envelope_quant']
        return wave.astype(global_config['envelope_dtype']).tobytes()


@dataclass
class QInsFrame(NSQCommand):
    freq: float

    def __post_init__(self):
        self.frame_idx = 0

    def _pack_cmd(self) -> list:
        return [0x11, self.frame_idx * 4 + 0, self.frequency_normalization32(self.freq),
                0x00000000, 0x0000, 0x0000, 0x0000, 0x00000000, 0x00000000]


@dataclass
class QInsResetF(NSQCommand):
    type: str
    frame: str = ''

    def __post_init__(self):
        self.frame_idx = 0
        self.type2head = {'all': 0x51, 'single': 0x41, 'phase': 0x31}

    def _pack_cmd(self) -> list:
        head = self.type2head.get(self.type.lower(), None)
        if head is None:
            raise AssemblyError(f'{self.__class__.__name__}.type can only be one of {self.type2head.keys()}')
        return [head, self.frame_idx * 4, 0, 0x00000000, 0x0000, 0x0000, 0x0000, 0x00000000, 0x00000000]


@dataclass
class QInsMov(NSQCommand):
    reg: int
    value: int
    type: str = '='

    def __post_init__(self):
        self.type2head = {'=': 0x38, '+': 0x48}

    def _pack_cmd(self) -> list:
        head = self.type2head.get(self.type, None)
        if head is None:
            raise AssemblyError(f'{self.__class__.__name__}.type can only be one of {self.type2head.keys()}')
        return [head, self.reg, self.value, 0x00000000, 0x0000, 0x0000, 0x0000, 0x00000000, 0x00000000]


@dataclass
class QInsWaitTrig(NSQCommand):
    def _pack_cmd(self) -> list:
        return [0xF4, 0, 0, 0x00000000, 0x0000, 0x0000, 0x0000, 0x00000000, 0x00000000]


@dataclass
class QInsIncPhase(NSQCommand):
    phase: float
    frame: str

    def __post_init__(self):
        self.frame_idx = 0

    def _pack_cmd(self) -> list:
        return [0x21, self.frame_idx * 4 + 1, self.phase_normalization32(self.phase),
                0x00000000, 0x0000, 0x0000, 0x0000, 0x00000000, 0x00000000]


@dataclass
class QInsPlayZero(NSQCommand):
    width: float

    @property
    def overhead(self):
        return self.width

    def _pack_cmd(self) -> list:
        frames = round(self.width / global_config['play_zero_step'])
        return [0x44, 0, 0, frames, 0, 0x0000, 0x0000, 0, 0]


@dataclass
class QInsPlayWave(NSQCommand):
    frame: str
    envelop: str
    amp: float
    attach_freq: float
    attach_phase: float

    @property
    def overhead(self):
        return self.envelop_slice.step/global_config['OUTSrate']

    def __post_init__(self):
        self.frame_idx = 0
        self.envelop_slice = slice(0, None, 1)

    def _pack_cmd(self) -> list:
        return [
            0x04, self.frame_idx * 4,
            np.uint32(self.envelop_slice.start / global_config['envelope_step']),
            np.uint32(self.envelop_slice.step / global_config['envelope_step']),
            np.int32(self.amp * (1 << 15)), 0x0000, 0x0000,
            self.frequency_normalization32(self.attach_freq),
            self.phase_normalization32(self.attach_phase)
        ]


@dataclass
class QInsWait(NSQCommand):
    def _pack_cmd(self) -> list:
        return [0x00, 0, 0, 0x00000000, 0x0000, 0x0000, 0x0000, 0x00000000, 0x00000000]


@dataclass
class QInsJump(NSQCommand):
    target: str

    def __post_init__(self):
        self.ins_idx = 0

    def _pack_cmd(self) -> list:
        return [0x18, 0, 0, self.ins_idx, 0, 0x0000, 0x0000, 0, 0]


@dataclass
class QInsJumpWithReg(NSQCommand):
    reg: int
    value: int
    target: str

    def __post_init__(self):
        self.ins_idx = 0

    def _pack_cmd(self) -> list:
        return [0x28, self.reg, self.value, self.ins_idx, 0, 0x0000, 0x0000, 0, 0]


@dataclass
class QInsJumpWithJudge(NSQCommand):
    value: int
    mask: int
    target: str

    def __post_init__(self):
        self.ins_idx = 0

    def _pack_cmd(self) -> list:
        return [0x28, 0x10, self.mask << 16 | self.value, self.ins_idx, 0, 0x0000, 0x0000, 0, 0]


@dataclass
class QInsEnd(NSQCommand):
    def _pack_cmd(self) -> list:
        return [0xF8, 0, 0, 0x00000000, 0x0000, 0x0000, 0x0000, 0x00000000, 0x00000000]


@dataclass
class QInsCapture(NSQCommand):
    width: float
    probe_delay: float = 0

    def __post_init__(self):
        self.ch_flag = {'all': 3, 'ad': 2, 'da': 1}

    def __bytes__(self):
        delay_length = int(round(self.probe_delay/16e-9))
        length = int(round(self.width/16e-9))
        cmds = [
            [0x0002, self.ch_flag['da'], 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, delay_length],
            [0x0002, self.ch_flag['all'], 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, length],
        ]
        return b''.join(self.list2bytes(cmd) for cmd in cmds)

    @staticmethod
    def list2bytes(cmd: list):
        cmd_raw = struct.pack('=HHHHHHHH', *cmd[::-1])
        return cmd_raw


@dataclass
class _QInsPTrigDelay(_ProbeCommand):
    tag: str = field(kw_only=True)
    delay: float

    def __post_init__(self):
        self.ch_flag = {'all': 3, 'ad': 2, 'da': 1}

    def _pack_cmd(self) -> list:
        length = int(round(self.delay / 16e-9))
        return [0x0002, self.ch_flag['all'], 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, length]


@dataclass
class _QInsPWaitTrig(_ProbeCommand):
    def _pack_cmd(self) -> list:
        return [0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000]


@dataclass
class _QInsPJump(_ProbeCommand):
    target: str

    def __post_init__(self):
        self.ins_idx = 0

    def _pack_cmd(self) -> list:
        return [0x0003, 0x0000, 0x0000, self.ins_idx, 0x0000, 0x0000, 0x0000, 0x0000]


class Assembler(GenTagMixin):
    def __init__(self, ch_map=None):
        if ch_map is None:
            ch_map = {
                1: [3, 4, 5, 6, 7, 8],
                2: [11, 12, 13, 14, 15, 16]
            }
        self.ch_map = ch_map
        self.drive2probe = {j: i for i in ch_map.keys() for j in ch_map[i]}
        self.raw_cmdq = {j: [] for i in ch_map.values() for j in i}
        self.probe_cmdq = {i: [] for i in ch_map.keys()}
        self.drive_cmdq = {j: [] for i in ch_map.values() for j in i}

        self.envelop_cache = {
            j: np.zeros((global_config['envelope_cache'] // 2,), dtype=np.int16) for i in ch_map.values() for j in i
        }

        self.frame_symbol = {j: {} for i in ch_map.values() for j in i}
        self.envelop_symbol = {j: {} for i in ch_map.values() for j in i}
        self.drive_symbol = {j: {} for i in ch_map.values() for j in i}
        self.probe_symbol = {i: {} for i in ch_map.keys()}

    def set_chnl_cmdq(self, ch_id, cmdq):
        if ch_id not in self.drive2probe:
            raise AssemblyError(f'OUT channel {ch_id} does not exist')
        self.raw_cmdq[ch_id] = cmdq
        self.envelop_symbol[ch_id], cmdq = self.extract_envelop(ch_id, cmdq)
        self.frame_symbol[ch_id] = self.extract_frame(cmdq)
        (self.drive_cmdq[ch_id], self.probe_cmdq[self.drive2probe[ch_id]],
         self.drive_symbol[ch_id], self.probe_symbol[self.drive2probe[ch_id]]) = self.divide_cmd(ch_id, cmdq)

    def extract_envelop(self, ch_id, cmdq: List[NSQCommand]) -> "Tuple[dict, List[NSQCommand]]":
        """!
        在指令队列中提取包络指令，并建立符号表

        @param ch_id:
        @param cmdq:
        @return:
        """
        res_cmdq, envelops = [], []
        for cmd in cmdq:
            if not isinstance(cmd, QInsEnvelop):
                res_cmdq.append(copy.copy(cmd))
            else:
                envelops.append(cmd)

        cache = self.envelop_cache[ch_id]
        # 给cache头部打上包络更新指令包头
        cache[:16] = global_config['envelope_head']
        data_cache = cache[16:]
        data_cache[:] = 0

        start = 0
        symbol_map = {}
        for env in envelops:
            wave = bytes(env)
            length = len(wave)
            end = start + length
            data_cache[start//2:end//2] = np.frombuffer(wave, dtype=global_config['envelope_dtype'])
            env.envelop_slice = slice(start, end, length)
            start += length
            symbol_map[env.tag] = env
        return symbol_map, res_cmdq

    @staticmethod
    def extract_frame(cmdq: List[NSQCommand]) -> "dict":
        """!
        在指令队列中提取包络配置指令，并且建立包络符号表

        @param cmdq:
        @return:
        """
        frames = []
        for cmd in cmdq:
            if not isinstance(cmd, QInsFrame):
                continue
            frames.append(cmd)

        symbol_map = {}
        for idx, frame in enumerate(frames):
            frame.frame_idx = idx
            symbol_map[frame.tag] = frame
        return symbol_map

    def divide_cmd(self, ch_id, cmdq) -> "Tuple[list, list, dict, dict]":
        """!

        @param ch_id:
        @param cmdq:
        @return:
        """
        drive_queue, probe_queue, drive_symbol, probe_symbol = self._link_wave(ch_id, cmdq)
        drive_queue, drive_symbol = self._optimize_drive_q(drive_queue, drive_symbol)
        probe_queue, probe_symbol = self._optimize_probe_q(probe_queue)
        drive_queue, probe_queue = self._link_jump(drive_queue, probe_queue, drive_symbol, probe_symbol)
        return drive_queue, probe_queue, drive_symbol, probe_symbol

    def _link_wave(self, ch_id, cmdq):
        """!
        建立frame和envelop到指令的关联，并生成基础的指令符号表，初步分割drive与probe的指令

        @param ch_id:
        @param cmdq:
        @return:
        """
        symbols = ChainMap(self.frame_symbol[ch_id], self.envelop_symbol[ch_id])
        drive_queue, probe_queue, drive_symbol, probe_symbol = [], [], {}, {}
        probe_queue.append(_QInsPWaitTrig(tag=self.generate_tag))
        probe_symbol[probe_queue[-1].tag] = 0

        for cmd in cmdq:
            if hasattr(cmd, 'frame_idx') and hasattr(cmd, 'frame'):
                frame: QInsFrame = symbols.get(cmd.frame, None)
                if frame is None:
                    raise AssemblyError(f'The frame tag required by instruction {cmd} '
                                        f'does not exist in the instruction queue of channel {ch_id}')
                cmd.frame_idx = frame.frame_idx
            if hasattr(cmd, 'envelop_slice') and hasattr(cmd, 'envelop'):
                envelop: QInsEnvelop = symbols.get(cmd.envelop, None)
                if envelop is None:
                    raise AssemblyError(f'The envelop tag required by instruction {cmd} '
                                        f'does not exist in the instruction queue of channel {ch_id}')
                cmd.envelop_slice = envelop.envelop_slice
            if isinstance(cmd, QInsCapture):
                # 这里要保证占capture位置的playzero指令依然能被跳转
                wait = QInsPlayZero(tag=cmd.tag, width=cmd.width + cmd.probe_delay)
                cmd.tag = self.generate_tag
                drive_queue.append(wait)
                probe_queue.append(cmd)
            else:
                wait = _QInsPTrigDelay(tag=self.generate_tag, delay=cmd.overhead)
                drive_queue.append(cmd)
                probe_queue.append(wait)
            drive_symbol[drive_queue[-1].tag] = len(drive_queue)-1
            probe_symbol[probe_queue[-1].tag] = len(probe_queue)-1
        probe_queue.append(_QInsPJump(target=probe_queue[0].tag, tag=self.generate_tag))
        probe_symbol[probe_queue[-1].tag] = len(probe_queue)-1
        return drive_queue, probe_queue, drive_symbol, probe_symbol

    def _link_jump(self, drive_queue: List[NSQCommand], probe_queue, drive_symbol, probe_symbol):
        """!
        连接指令队列中的跳转指令

        @param drive_queue:
        @param probe_queue:
        @return:
        """
        for cmd in drive_queue:
            if hasattr(cmd, 'ins_idx') and hasattr(cmd, 'target'):
                cmd.ins_idx = drive_symbol[cmd.target]

        for cmd in probe_queue:
            if hasattr(cmd, 'ins_idx') and hasattr(cmd, 'target'):
                cmd.ins_idx = probe_symbol[cmd.target]
        return drive_queue, probe_queue

    def _optimize_probe_q(self, queue):
        """!
        优化probe指令队列

        @param queue:
        @param symbol:
        @return:
        """
        symbol, idx = {}, 0
        cache = []
        res_q = []
        # 合并所有相邻的_QInsProbeDelay，减少指令队列长度
        for cmd in queue:
            if isinstance(cmd, _QInsPTrigDelay):
                cache.append(cmd)
            else:
                delay = _QInsPTrigDelay(tag=self.generate_tag, delay=sum(i.delay for i in cache))
                if delay.delay != 0:
                    res_q.append(delay)
                    symbol[delay.tag] = idx
                    idx += 1
                res_q.append(cmd)
                symbol[cmd.tag] = idx
                idx += 1
                cache = []
        return res_q, symbol

    def _optimize_drive_q(self, queue, symbol):
        """!
        优化drive指令队列

        @param queue:
        @param symbol:
        @return:
        """
        return queue, symbol

    def assemble(self) -> "Tuple[dict, dict, dict]":
        envelop_cache = {}
        drive_cache = {}
        for pch, dch_list in self.ch_map.items():
            memory = np.zeros((10240 * 8 * len(dch_list), ), dtype=np.uint32).reshape((len(dch_list), 8*10240))
            for idx, ch in enumerate(dch_list):
                _data = np.frombuffer(b''.join(bytes(i) for i in self.drive_cmdq[ch]), dtype=np.int32)
                memory[idx, :_data.size] = _data
            drive_cache[pch] = memory
            envelop_cache[pch] = np.array([self.envelop_cache[ch] for ch in dch_list], dtype=np.int16)

        probe_cache = {}
        for pch, queue in self.probe_cmdq.items():
            memory = np.frombuffer(b''.join(bytes(i) for i in queue), dtype=np.int32)
            probe_cache[pch] = memory

        return envelop_cache, drive_cache, probe_cache
