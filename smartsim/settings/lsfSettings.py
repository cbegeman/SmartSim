# BSD 2-Clause License
#
# Copyright (c) 2021, Hewlett Packard Enterprise
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from ..error import SSConfigError
from ..utils.helpers import init_default
from .settings import BatchSettings, RunSettings


class JsrunSettings(RunSettings):
    def __init__(self, exe, exe_args=None, run_args=None, env_vars=None):
        """Settings to run job with ``jsrun`` command

        ``JsrunSettings`` can be used for both the `lsf` launcher.

        :param exe: executable
        :type exe: str
        :param exe_args: executable arguments, defaults to None
        :type exe_args: str | list[str], optional
        :param run_args: arguments for run command, defaults to None
        :type run_args: dict[str, str], optional
        :param env_vars: environment vars to launch job with, defaults to None
        :type env_vars: dict[str, str], optional
        """
        super().__init__(
            exe, exe_args, run_command="jsrun", run_args=run_args, env_vars=env_vars
        )

    def set_num_rs(self, num_rs):
        """Set the number of resource sets to use

        This sets ``--nrs``. 

        :param num_rs: Number of resource sets or `ALL_HOSTS`
        :type num_rs: int or str
        """

        if isinstance(num_rs, str):
            self.run_args["nrs"] = num_rs
        else:
            self.run_args["nrs"] = int(num_rs)

    def set_cpus_per_rs(self, num_cpus):
        """Set the number of cpus to use per resource set

        This sets ``--cpu_per_rs``

        :param num_cpus: number of cpus to use per resource set or ALL_CPUS
        :type num_cpus: int
        """
        if isinstance(num_cpus, str):
            self.run_args["cpu_per_rs"] = num_cpus
        self.run_args["cpu_per_rs"] = int(num_cpus)

    def set_gpus_per_rs(self, num_gpus):
        """Set the number of gpus to use per resource set

        This sets ``--gpu_per_rs``

        :param num_cpus: number of gpus to use per resource set or ALL_GPUS
        :type num_gpus: int
        """
        if isinstance(num_gpus, str):
            self.run_args["gpu_per_rs"] = num_gpus
        self.run_args["gpu_per_rs"] = int(num_gpus)

    def set_rs_per_host(self, num_rs):
        """Set the number of resource sets to use per host

        This sets ``--rs_per_host``

        :param num_rs: number of resource sets to use per host
        :type num_rs: int
        """
        self.run_args["rs_per_host"] = int(num_rs)

    def set_tasks(self, num_tasks):
        """Set the number of tasks for this job

        This sets ``--np``

        :param num_tasks: number of tasks
        :type num_tasks: int
        """
        self.run_args["np"] = int(num_tasks)

    def set_tasks_per_rs(self, num_tprs):
        """Set the number of tasks per resource set

        This sets ``--tasks_per_rs``

        :param num_tpn: number of tasks per resource set
        :type num_tpn: int
        """
        self.run_args["tasks_per_rs"] = int(num_tprs)

    def format_run_args(self):
        """Return a list of LSF formatted run arguments

        :return: list LSF arguments for these settings
        :rtype: list[str]
        """
        # args launcher uses
        args = []
        restricted = ["chdir"]

        for opt, value in self.run_args.items():
            if opt not in restricted:
                short_arg = bool(len(str(opt)) == 1)
                prefix = "-" if short_arg else "--"
                if not value:
                    args += [prefix + opt]
                else:
                    if short_arg:
                        args += [prefix + opt, str(value)]
                    else:
                        args += ["=".join((prefix + opt, str(value)))]
        return args

class BsubBatchSettings(BatchSettings):
    def __init__(
        self,
        nodes=None,
        time=None,
        project=None,
        batch_args=None,
        **kwargs,
    ):
        """Specify ``bsub`` batch parameters for a job

        :param nodes: number of nodes for batch
        :type nodes: int, optional
        :param time: walltime for batch job in format hh:mm
        :type time: str, optional
        :param project: project for batch launch
        :type project: str, optional
        :param batch_args: overrides for LSF batch arguments
        :type batch_args: dict[str, str], optional
        """
        super().__init__("bsub", batch_args=batch_args)
        if nodes:
            self.set_nodes(nodes)
        self.set_walltime(time)
        self.set_project(project)

    def set_walltime(self, time):
        """Set the walltime

        This sets ``-W``.

        :param time: Time in hh:mm format
        :type time: str
        """
        if time:
            self.walltime = time
        else:
            # If not supplied, batch submission fails,
            # but the user will know from the error
            self.walltime = None

    def set_project(self, project):
        """Set the project

        This sets ``-P``.

        :param time: project name
        :type time: str
        """
        if project:
            self.project = project
        else:
            # If not supplied, batch submission fails,
            # but the user will know from the error
            self.project = None

    def set_nodes(self, num_nodes):
        """Set the number of nodes for this batch job

        This sets ``--nnodes``.

        :param num_nodes: number of nodes
        :type num_nodes: int
        """
        self.batch_args["nnodes"] = int(num_nodes)

    def set_hostlist(self, host_list):
        """Specify the hostlist for this job

        :param host_list: hosts to launch on
        :type host_list: list[str]
        :raises TypeError:
        """
        if isinstance(host_list, str):
            host_list = [host_list.strip()]
        if not isinstance(host_list, list):
            raise TypeError("host_list argument must be a list of strings")
        if not all([isinstance(host, str) for host in host_list]):
            raise TypeError("host_list argument must be list of strings")
        self.batch_args["m"] = "\"" + ",".join(host_list) + "\""

    def set_tasks(self, num_tasks):
        """Set the number of tasks for this job

        This sets ``--np``

        :param num_tasks: number of tasks
        :type num_tasks: int
        """
        self.run_args["np"] = int(num_tasks)

    def set_tasks_per_rs(self, num_tprs):
        """Set the number of tasks per resource set

        This sets ``--tasks_per_rs``

        :param num_tpn: number of tasks per resource set
        :type num_tpn: int
        """
        self.run_args["tasks_per_rs"] = int(num_tprs)

    def format_batch_args(self):
        """Get the formatted batch arguments for a preview

        :return: batch arguments for Qsub
        :rtype: list[str]
        """
        opts = []
        for opt, value in self.batch_args.items():
            prefix = "-" # LSF only uses single dashses

            if not value:
                opts += [prefix + opt]
            else:
                opts += [" ".join((prefix + opt, str(value)))]

        return opts
