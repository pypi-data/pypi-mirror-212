from inspect import isclass
from typing import Any, Callable, MutableMapping, Optional, Union

import pygame

from .schedule import Schedule, Stopwatch


class SpriteSheet:
    def __init__(self, filename):
        self.image = pygame.image.load(filename)

    def image_by_area(self, x, y, width, height) -> pygame.surface.Surface:
        image = pygame.Surface((width, height))
        image.blit(self.image, (0, 0), (x, y, width, height))
        image.set_colorkey((0, 0, 0))
        return image


class AnimationImage:
    """アニメーションのある画像を設定・描写するためのクラス

        In this class, update() is
        auto-registered to the Schedule class and executed automatically.


    Attributes:
        anim_frame_id (int): 現在のフレームを示すインデックス
        anim_interval (int): アニメーションの更新間隔（ミリ秒）
        image (pygame.surface.Surface): 現在のフレームの画像
        is_playing (bool): アニメーションが再生中かどうかを示すフラグ
        loop_count (int): アニメーションのループ回数。-1で無限ループ指定
        loop_counter (int): 現在のループ回数
    """

    def __init__(self):
        self._anim_frames: list[pygame.surface.Surface] = [
            pygame.surface.Surface((0, 0)),
        ]
        self.anim_frame_id = 0
        self.anim_interval = 1
        self.image = self.anim_frames[self.anim_frame_id]
        self.is_playing = False
        self.loop_count = -1
        self.loop_counter = 0

    @property
    def anim_frames(self):
        return self._anim_frames

    @anim_frames.setter
    def anim_frames(self, value):
        self._anim_frames = value
        self.image = self.anim_frames[self.anim_frame_id]

    @property
    def frame_num(self):
        return len(self.anim_frames)

    @property
    def anim_interval(self):
        return self._anim_interval

    @anim_interval.setter
    def anim_interval(self, value):
        self._anim_interval = value
        if Schedule.is_func_scheduled(self.update_animation):
            Schedule.change_interval(self.update_animation, self.anim_interval)
        else:
            Schedule.add(self.update_animation, self.anim_interval)

    def is_all_loop_finished(self):
        return self.loop_count > 0 and self.loop_counter >= self.loop_count

    def let_play(self):
        if not self.is_playing:
            Schedule.activate_schedule(self.update_animation)
        self.is_playing = True
        if self.is_all_loop_finished():
            self.loop_counter = 0

    def let_stop(self):
        if self.is_playing:
            Schedule.deactivate_schedule(self.update_animation)
        self.is_playing = False

    def seek(self, frame_id: int):
        self.anim_frame_id = frame_id
        self.image = self.anim_frames[self.anim_frame_id]

    def reset_current_loop(self):
        self.anim_frame_id = 0
        self.image = self._anim_frames[self.anim_frame_id]

    def reset_animation(self):
        self.anim_frame_id = 0
        self.image = self._anim_frames[self.anim_frame_id]
        self.loop_counter = 0
        Schedule.reset_interval_clock(self.update_animation)

    def update_animation(self):
        if self.is_playing and (
            self.loop_counter < self.loop_count or self.loop_count < 0
        ):
            self.anim_frame_id = (self.anim_frame_id + 1) % len(self._anim_frames)
            self.image = self._anim_frames[self.anim_frame_id]
            if self.anim_frame_id == 0:
                self.loop_counter += 1
                if self.is_all_loop_finished():
                    self.is_playing = False
                    Schedule.deactivate_schedule(self.update_animation)


class AnimationImageFactory(MutableMapping):
    """For AnimationImage

    Examples:
        class ExampleAnimation(AnimationImage):
            pass
        a = AnimationFactory()
        a["animation_a"] = ExampleAnimation
        animation = a["jump_animation"]
        animation.let_play_animation()
    """

    def __init__(self, *args, **kwargs):
        self.__dict__: dict[Any, AnimationImage]
        self.__dict__.update(*args, **kwargs)

    def __getitem__(self, key) -> AnimationImage:
        return self.__dict__[key]()

    def __setitem__(self, key, value: AnimationImage):
        if isclass(value):
            self.__dict__[key] = value
        else:
            raise ValueError("The value must not be instance.")

    def __delitem__(self, key):
        del self.__dict__[key]

    def __iter__(self):
        return iter(self.__dict__)

    def __len__(self):
        return len(self.__dict__)


class AnimationImageDict(MutableMapping):
    """For AnimationImage

    Examples:
        class ExampleAnimation(AnimationImage):
            pass
        a = AnimationFactory()
        a["animation_a"] = ExampleAnimation()
        animation = a["jump_animation"]
        animation.let_play_animation()
    """

    def __init__(self, *args, **kwargs):
        self.__dict__: dict[Any, AnimationImage]
        self.__dict__.update(*args, **kwargs)

    def __getitem__(self, key) -> AnimationImage:
        return self.__dict__[key]

    def __setitem__(self, key, value: AnimationImage):
        if not isclass(value):
            self.__dict__[key] = value
        else:
            raise ValueError("The value must be instance.")

    def __delitem__(self, key):
        del self.__dict__[key]

    def __iter__(self):
        return iter(self.__dict__)

    def __len__(self):
        return len(self.__dict__)


# Keyframe = list[int, list[int, ]]


class Keyframe(list):
    """
    This is subclass of list type.
    Args of __init__ is stricted to play keyframe role.
    """

    def __init__(
        self,
        frame_milliseconds_on_timeline: int,
        args_for_script: list[Union[int, float]],
    ):
        if not isinstance(frame_milliseconds_on_timeline, int):
            raise ValueError('Argument "frame_milliseconds_on_timeline" must be int')
        args_for_script_error_msg = (
            'Argument "args_for_script" must be list of integers'
        )
        if isinstance(args_for_script, list):
            if (
                len([arg for arg in args_for_script if isinstance(arg, (int, float))])
                == 0
            ):
                raise ValueError(args_for_script_error_msg)
        else:
            raise ValueError(args_for_script_error_msg)
        super().__init__((frame_milliseconds_on_timeline, args_for_script))


class KeyframeAnimation:
    """
    Examples:
        def script_on_everyframe(given_args_on_frameupdates):
            print(given_args_on_frameupdates)

        self.instance = KeyframeAnimation(
            script_on_everyframe,
            [Keyframe((0, [0])),
             Keyframe((1000, [100])),
                Keyframe((2000, [200]))]))

        self.instance.let_play()

        while True:
            # engine do this automatically:
            dt = clock.tick(fps) # clock is pygame.time.Clock

            Stopwatch.update_all_stopwatch(dt)

            self.instance.update(dt)
    output 0 if time is at 0 milliseconds
    ...\n
    output about 100 if time is at 1000
    ...\n
    output about 120 if time is at 1200
    ...\n
    output about 2000 if time is at 2000
    """

    def __init__(
        self,
        script_on_everyframe: Callable,
        frames: list[Keyframe],
        script_on_finished: Optional[Callable] = None,
        loop_count: Optional[int] = 1,
    ):
        self._frames: list[Keyframe] = frames
        self.id_current_frame: int = 0

        self.loop_count = loop_count
        self._loop_counter = 0
        self._finished_loop_counter = 0  # counter to display

        self.is_playing = False

        self.is_reverse = False

        self.__timer = Stopwatch()

        self.script_on_everyframe = script_on_everyframe
        self.script_on_finished = script_on_finished

    @property
    def frames(self):
        return self._frames

    @property
    def current_frame(self) -> Keyframe:
        return self.frames[self.id_current_frame]

    @property
    def frame_count(self) -> int:
        return len(self.frames)

    @property
    def id_final_frame(self) -> int:
        return self.frame_count - 1

    @property
    def next_frame(self) -> Keyframe:
        if self.id_current_frame < self.id_final_frame:
            id = self.id_current_frame + 1
        else:
            id = self.id_current_frame
        return self.frames[id]

    @property
    def loop_counter(self) -> int:
        return self._loop_counter

    @property
    def finished_loop_counter(self) -> int:
        return self._finished_loop_counter

    @frames.setter
    def frames(self, value):
        self._frames = value

    def let_play(self):
        self.is_playing = True
        if self._finished_loop_counter > self._loop_counter:
            self._finished_loop_counter = 0

    def let_stop(self):
        self.is_playing = False
        self.__timer.stop()

    def reset_animation(self):
        self.id_current_frame = 0
        self._loop_counter = 0
        self.__timer.reset()

    def __is_all_loop_finished(self):
        return self.loop_count > 0 and self.loop_counter >= self.loop_count

    def is_finished(self):
        """
        Use this method to know if all loops of the animation have
        finished.
        (For developers of this class: DO NOT USE this method for
        frame updates).
        """
        return self.loop_count > 0 and self.finished_loop_counter >= self.loop_count

    def update(self, dt):
        """Update the frame and do script on current frame."""

        if self.is_playing:
            go_to_next_keyframe = False
            if not self.__timer.is_playing():
                self.__timer.start()
            time = self.__timer.read()
            between_current_and_next = self.next_frame[0] - self.current_frame[0]
            if time >= between_current_and_next:
                weight = 1
                go_to_next_keyframe = True
            else:
                weight = time / (between_current_and_next)
            args = [
                pygame.math.lerp(
                    self.current_frame[1][i], self.next_frame[1][i], weight
                )
                for i in range(len(self.current_frame[1]))
            ]
            self.script_on_everyframe(*args)
            if go_to_next_keyframe:
                self.id_current_frame = (self.id_current_frame + 1) % self.frame_count
                self.__timer.reset()
                if self.id_current_frame == 0:
                    self._loop_counter += 1
                    self._finished_loop_counter += 1
                    if self.__is_all_loop_finished():
                        if self.script_on_finished:
                            self.script_on_finished()
                        self.is_playing = False
                        self.__timer.stop()
                        self._loop_counter = 0

    def read_current_frame_progress(self) -> int:
        return self.__timer.read()
