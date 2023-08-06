#  Copyright (c) 2023 Jari Van Melckebeke
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, see <https://www.gnu.org/licenses/>.
#
import time
from distutils.util import strtobool
import os

from task_report import TaskReport
from utils.misc import random_task_name, reformat_units, time_to_str


class InternalTimer:
    def __init__(self):
        self.start_time = None
        self.end_time = None

        self.internal_time = 0

    def __enter__(self):
        if self.start_time is not None:
            return self

        self.start_time = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.start_time is None:
            return
        self.internal_time += time.time() - self.start_time
        self.start_time = None


class TimeIt:
    """
    Jari's infamous timeit class for all your performance measuring needs

    Usage:
    with TimeIt("my timer") as timer:
        # do stuff
        with timer("my subtimer"):
            # do stuff
            with timer("my subtimer 2"):
                # do stuff


    or as a decorator:
    @TimeIt.as_decorator("my timer")
    def my_function(*args, timer, **kwargs):
        # do stuff

    """

    def __init__(self, name: str):
        self.internal_timer = InternalTimer()
        self.timer = None
        with self.internal_timer:
            self.name = name
            self.start_time = None
            self.end_time = None

            self.active = bool(strtobool(os.getenv("TIME_IT", "true")))

    def __enter__(self):
        with self.internal_timer:
            self.start_time = time.time()
            if self.timer is None:
                self.timer = self.__Timer(self.name, self.internal_timer, None)
            return self.timer.__enter__()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end_time = time.time()
        self.__print_timeit_report()
        pass

    @property
    def elapsed_time(self):
        return self.end_time - self.start_time if self.end_time is not None else None

    def __call__(self, name, *args, **kwargs):
        if self.timer is None:
            self.timer = self.__Timer(name, self.internal_timer, None)

        return self.timer(name)

    def __print_timeit_report(self):
        def print_report_title_line():
            print(f"================= [{self.name}] TIMEIT REPORT =================")

        def generate_task_report_dict(tasks):

            report = {}

            for task_timer in tasks:
                task_name = task_timer["name"]

                if task_name in report:
                    report[task_name]["count"] += 1
                    report[task_name]["times"].append(task_timer["elapsed_time"])
                    report[task_name]["avg"] = sum(report[task_name]["times"]) / report[task_name]["count"]
                else:
                    report[task_name] = {
                        "name": task_name,
                        "count": 1,
                        "times": [task_timer["elapsed_time"]],
                        "ratio": 0,
                        "avg": task_timer["elapsed_time"],
                    }

                if len(task_timer["task_timers"]) > 0:
                    report[task_name]["subtasks"] = generate_task_report_dict(task_timer["task_timers"])
            total_time = sum([sum(task["times"]) for task in report.values()])

            for task in report.values():
                task["ratio"] = sum(task["times"]) / total_time

            return report

        def print_report(_report, spacing=0):
            task_report = TaskReport.from_dict(
                {
                    "name": self.name,
                    "count": 1,
                    "times": [self.elapsed_time],
                    "ratio": 0,
                    "avg": self.elapsed_time,
                    "subtasks": _report,
                }
            )
            task_report.internal_time = self.internal_timer.internal_time
            task_report.print(spacing=spacing, skip_first=True)

        elapsed_time = self.elapsed_time

        generate_report_start = time.time()

        if len(self.timer.task_timers) < 1:
            print(f"[TIMEIT] {self.name} took {time_to_str(elapsed_time)}")
            return

        print_report_title_line()

        print(f"[TIMEIT] {self.name} took {time_to_str(elapsed_time)}")

        report = generate_task_report_dict(self.timer.task_timers)

        print_report(report, spacing=0)

        # print coverage stats

        time_accounted_for = 0
        total_time = elapsed_time + self.internal_timer.internal_time

        for task in report.values():
            time_accounted_for += sum(task["times"])

        coverage = time_accounted_for / total_time
        time_unaccounted_for = total_time - time_accounted_for
        print(
            f"[{coverage:.2%}% COVERAGE] time accounted for: {time_to_str(time_accounted_for)}, "
            f"time unaccounted for: {time_to_str(time_unaccounted_for)}")

        generate_report_end = time.time()
        generate_report_duration = generate_report_end - generate_report_start

        duration, unit = reformat_units(generate_report_duration)

        print(f"[TIMEIT] report generation took {time_to_str(generate_report_duration)}")

        print_report_title_line()

    class __Timer:
        def __init__(self, name, internal_timer: InternalTimer, parent_timer=None):
            self.internal_timer = internal_timer
            self.start_time = None
            self.end_time = None

            self.name = name
            self.parent_timer = parent_timer
            self.internal_timer = internal_timer

            self.current_task = None
            self.current_task_name = None

            self.task_timers = []

            self.report_object = {}

        def __call__(self, name=None, *args, **kwargs):
            if name is None:
                name = random_task_name()

            with self.internal_timer:
                # oh boy this looks ugly
                if self.current_task is not None:
                    return self.current_task(name, *args, **kwargs)
                else:
                    self.current_task_name = name
                    self.current_task = self.__class__(name, self.internal_timer, self)
                return self.current_task

        def __enter__(self):
            with self.internal_timer:
                if self.current_task_name is not None:
                    self.current_task = self.__class__(self.current_task_name, self.internal_timer, self)
                    self.current_task.start_timer()
                    self.current_task_name = None

                self.start_time = time.time()
                return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            self.end_time = time.time()

            if self.parent_timer is not None:
                self.parent_timer.register_task_end({
                    "name": self.name,
                    "elapsed_time": self.end_time - self.start_time,
                    "task_timers": self.task_timers,
                })
                return

            elapsed_time = self.end_time - self.start_time

            self.elapsed_time = elapsed_time
            self.report_object = {
                "name": self.name,
                "elapsed_time": elapsed_time,
                "task_timers": self.task_timers
            }

        def start_timer(self):
            self.start_time = time.time()

        def register_task_end(self, task_report):
            self.current_task = None
            self.task_timers.append(task_report)

        def __repr__(self):
            return self.__str__()

        def __str__(self):
            return f"Timer(name=[{self.name}], tasks={self.task_timers}, current_task=[{self.current_task}])"
