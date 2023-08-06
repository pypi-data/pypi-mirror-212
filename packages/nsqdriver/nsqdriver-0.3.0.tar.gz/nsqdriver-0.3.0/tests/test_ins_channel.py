import pytest

import numpy as np

from nsqdriver import InsChannel
from nsqdriver.compiler.py_wave_asm import Assembler


def test_ins_if():
    ch = InsChannel()
    frame_65e9 = ch.ins_frame(6.5e9)  # 生成一个frame
    gaussian = ch.evlp_gaussian(31e-9)  # 生成一个高斯包络
    wave1 = gaussian * frame_65e9  # 生成一段高斯包络的波形

    print('\n测试if基本功能')
    ch.wait_for_trigger()
    with ch.ins_if('FREQ_1==1') as _if:  # 条件分支，若成立
        _if.inc_phase(frame_65e9, np.pi)  # 相位旋转180°
        _if.play_wave(wave1, 1, 0, np.pi)  # 播放第二个波形
    with ch.ins_else() as _else:  # 条件分支, 若不成立
        _else.play_zero(32e-9)  # 播放32ns的0
        _else.play_wave(wave1)  # 播放一段高斯包络的波形
    ch.lookup()

    ch.clear()
    ch.wait_for_trigger()
    # 不准在没有if的情况下调用ins_else
    with pytest.raises(RuntimeError):
        with ch.ins_else() as _el:
            _el.play_wave(wave1)

    print('\n测试if嵌套功能')
    ch.clear()
    ch.wait_for_trigger()
    ch.ins_variable('a', 10)
    with ch.ins_if('FREQ_1==1') as _if:  # 条件分支，若成立
        _if.inc_phase(frame_65e9, np.pi)  # 相位旋转180°
        _if.play_wave(wave1, 0.5, 0, 0)  # 播放第二个波形
    with ch.ins_else() as _else:  # 条件分支, 若不成立
        _else.play_zero(32e-9)  # 播放32ns的0
        _else.play_wave(wave1)  # 播放一段高斯包络的波形
        with _else.ins_if('a==10') as aa:
            aa.inc_phase(frame_65e9, np.pi / 2)
    ch.lookup()


def test_ins_loop():
    ch = InsChannel()
    frame_65e9 = ch.ins_frame(6.5e9)  # 生成一个frame
    gaussian = ch.evlp_gaussian(31e-9)  # 生成一个高斯包络
    wave1 = gaussian * frame_65e9  # 生成一段高斯包络的波形

    print('\n测试loop基本功能')
    ch.wait_for_trigger()
    with ch.ins_loop(times=10) as _loop:
        _loop.play_zero(32e-6)
        _loop.inc_phase(frame_65e9, np.pi / 2)
        _loop.play_wave(wave1)
    ch.lookup()

    print('测试loop嵌套功能')
    ch.clear()
    # 不能在loop中再次调用ch
    ch.wait_for_trigger()
    with ch.ins_loop(10) as _loop:
        with pytest.raises(RuntimeError):
            with ch.ins_loop(2) as _l2:
                _l2.play_wave(wave1)

    ch.clear()
    with ch.ins_loop(times=10) as _loop:
        _loop.play_zero(32e-6)
        with _loop.ins_loop(times=2) as _loop_1:
            _loop_1.inc_phase(frame_65e9, np.pi / 2)
            _loop_1.play_wave(wave1)

    print('\n')
    ch.lookup()


def test_nesting():
    ch = InsChannel()  # 生成参数化波形通道实例

    frame_65e9 = ch.ins_frame(6.5e9)  # 生成一个frame
    gaussian = ch.evlp_gaussian(31e-9)  # 生成一个高斯包络
    cos_pulse = ch.evlp_cospulse(43e-9)  # 生成一个hanning包络
    wave1 = gaussian * frame_65e9  # 生成一段高斯包络的波形
    wave2 = cos_pulse * frame_65e9  # 生成一段hanning包络的波形

    ch.wait_for_trigger()  # 等待触发到来
    ch.ins_variable('a', 10)

    print('\n测试loop嵌套if/else功能')
    with ch.ins_loop(times=10) as _loop:
        _loop.play_zero(32e-6)
        with _loop.ins_if('a==5') as _if:
            _if.play_wave(wave1)
        with _loop.ins_else() as _el:
            _el.play_wave(wave2)
    print('\n')
    ch.lookup()

    # 不允许在if分支中嵌套capture
    ch.clear()
    with ch.ins_if('FREQ_1==10') as _if:
        with pytest.raises(RuntimeError):
            _if.capture(1e-6)


def test_gen_ins_set():
    ch = InsChannel()  # 生成参数化波形通道实例

    frame_65e9 = ch.ins_frame(6.5e9)  # 生成一个frame
    frame_67e9 = ch.ins_frame(6.7e9)  # 生成一个frame
    gaussian = ch.evlp_gaussian(31e-9)  # 生成一个高斯包络
    cos_pulse = ch.evlp_cospulse(43e-9)  # 生成一个hanning包络
    wave1 = gaussian * frame_65e9  # 生成一段高斯包络的波形
    wave2 = cos_pulse * frame_67e9  # 生成一段hanning包络的波形

    ch.wait_for_trigger()  # 等待触发到来
    ch.ins_variable('a', 10)
    ch.play_wave(wave1)  # 播放高斯包络波形
    ch.play_zero(1e-6)  # 延迟1μs
    ch.play_wave(wave1)  # 播放高斯包络波形
    ch.capture(1e-6)
    with ch.ins_if('FREQ_1==1') as _if:  # 条件分支，若成立
        _if.inc_phase(frame_65e9, np.pi)  # 相位旋转180°
        _if.play_wave(wave2, 0.2, 0, 0)  # 播放第二个波形
    with ch.ins_else() as _else:  # 条件分支, 若不成立
        _else.play_zero(32e-9)  # 播放32ns的0
        _else.play_wave(wave1)  # 播放一段高斯包络的波形
    ch.play_zero(1e-6)
    ch.capture(1e-6)

    with ch.ins_loop(times=10) as _loop:
        _loop.play_zero(32e-6)
        _loop.inc_phase(frame_65e9, np.pi / 2)
        _loop.play_wave(wave2)
    print('\n')
    ch.lookup()
    queue = ch.compile()
    # print('\n', queue)
    asm = Assembler()
    asm.set_chnl_cmdq(3, queue)
    asm.set_chnl_cmdq(15, queue)
    print(asm.assemble())


def test_assemble():
    asm = Assembler()
    # asm.set_chnl_cmdq(1, )
