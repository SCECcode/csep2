"""
Job classes represent computational units.
"""
import os
import uuid
from csep.utils.file import mkdirs, copy_file
from csep.utils.constants import JobStatus
from csep.core.config import machine_config
from csep.core.system import system_builder, file_builder, JsonFile, TextFile
from csep.core.exceptions import CSEPSchedulerException
from csep.core.factories import ObjectFactory

class BaseTask:

    """
    Represents the base class for any job needed to run on the system.

    """

    def __init__(self, run_id=None, system='default', max_run_time=None, command=None, args=(), status=None,
                       inputs=(), outputs=(), work_dir=None):

        # primary index for simulation components
        self.run_id = run_id or uuid.uuid4().hex
        self.status = status or JobStatus.UNPREPARED
        self.add_system(system)
        self.command = command
        self.args = args
        self.work_dir = work_dir
        if self.work_dir is not None:
            self.work_dir = os.path.expandvars(os.path.expanduser(work_dir))
        self.max_run_time = max_run_time
        self._inputs = inputs or []
        self._outputs = outputs or []
        self._prepared = False
        # flag to warn user if trying to run in existing directory.
        self._force = False

    def __str__(self):
        return self.to_dict()

    def __eq__(self, other):
        return self.to_dict() == other.to_dict()

    def add_output(self, path, format):
        """
        Register outputs with the Job.

        Args:
            iterable (File): iterable of File objects

        Returns:

        """
        output = file_builder.create(format, path)
        self._outputs.append(output)

    def add_input(self, path, format):
        """
        Registers Inputs with the Job.

        Args:
            iterable:

        Returns:

        """
        input = file_builder.create(format, path)
        self._inputs.append(input)

    def add_system(self, name):
        config = machine_config[name]
        self._system = system_builder.create(config['type'], config)
        print(f"Created {name} system to use for {self.run_id}.")

    def prepare(self):
        """
        Generates run-time environment necessary to execute the Job. Should be overwritten
        in subclasses.

        Args:
            None

        Return:
            None
        """
        self._prepared = True

    def run(self):
        """
        This function executes the job on the system specified by the scheduler.

        Call is blocking and will stream the output from stdout in real-time. We assume
        that all jobs are going to be running as command line processes.

        Returns:
            rc: Return code from running process.
        """
        raise NotImplementedError

    def archive(self):
        """
        Archive results to storage directory (or db) that allows for easy rerunning of
        a model as it existed in the past.

        Utilizes the repository layer.

        Returns:

        """

    def to_dict(self):
        """ Returns class state as JSON serializable dict. """
        excluded = ['inputs','outputs']
        out = {}
        for k, v in self.__dict__.items():
            if not callable(v) and v not in excluded:
                if hasattr(v, 'to_dict'):
                    new_v=v.to_dict()
                else:
                    new_v=str(v)

                if k.startswith('_'):
                    out[k[1:]] = new_v
                else:
                    out[k] = new_v
        # custom serializing for inputs and outputs
        out['inputs'] = []
        for inp in self._inputs:
            out['inputs'].append(os.path.expandvars(os.path.expanduser(inp)))
        out['outputs'] = []
        for outf in self._outputs:
            if not os.path.isabs(outf):
                out['outputs'].append(os.path.join(self.work_dir,str(outf)))
        return out

    @classmethod
    def from_dict(cls, adict):
        return cls(**adict)

    def _stage_inputs(self, copy=False):
        """
        Stages Model inputs according to the user-defined plan.

        Returns:
            None

        Throws:
            FileNotFoundError
        """
        """
        Make sure that input files are in the correct locations.

        Note: Could use File Objects in the future, right now just assuming
        they are strings.

        Returns:

        """
        n_inputs = len(self._inputs)
        if copy:
            print(f"Staging {n_inputs} inputs to {self.work_dir}.")
            for inp in self._inputs:
                print(f"Copying {inp} to {self.work_dir}.")
                copy_file(inp, self.work_dir)
        else:
            print(f"Found {n_inputs} listed, but not copying. Maintaining for archival.")

    def _create_environment(self):
        """
        Creates compute environment to run the job.

        Args:
            force (bool): overwrites directory if True

        Returns:

        Throws:
            FileNotFoundError

        """
        """
        Create run-time environment needed to run UCERF3-ETAS

        Returns:

        """
        if os.path.isdir(self.work_dir):
            if self._force:
                print(f'Warning: Found directory at {self.work_dir}. Forcing overwrite.')
            else:
                raise CSEPSchedulerException("Working directory already exists. Set force = True to overwrite.")
        try:
            mkdirs(self.work_dir, 0o0755)
        except OSError:
            print(f'Unable to create working directory at {self.work_dir}. Ignoring forecast.')


class UCERF3Forecast(BaseTask):
    def __init__(self, name=None, model_dir=None, config_templ=None,
                       script_templ=None, output_dir=None, archive_dir=None, nnodes=None, force=False,
                       **kwargs):

        super().__init__(**kwargs)

        self.name = name
        self.model_dir =model_dir
        self.nnodes = nnodes
        self._config_templ = config_templ
        self._script_templ = script_templ
        self._force = force

        # these variables could be used for archiving purposes.
        # we could write the config or the run_script to a db or file
        # to rerun model as it existed.
        self._config = None
        self._run_script = None
        self.archive_dir = archive_dir

        # runtime output directory
        self.output_dir = output_dir

    def prepare(self):
        """
        Create necessary environment for running the job.

        Returns:

        """
        print(f"Preparing UCERF3-ETAS forecast {self.name} in dir {self.work_dir}.")
        # make sure it can be prepared
        if self._config_templ is None:
            raise CSEPSchedulerException("Cannot create forecast without configuration.")

        if self._script_templ is None:
            raise CSEPSchedulerException("Cannot create forecast without run-script.")

        if self._system is None:
            raise CSEPSchedulerException("Cannot create forecast without system information.")

        # creates working directory
        self._create_environment()

        # write configuration file to working directory
        new = self._config_templ_file.config
        self._config=self._config_templ_file.template(new)
        self._config.write(os.path.join(self.work_dir, self.run_id + "-config.json"))
        self._inputs.append(self.config_file)

        # generate run-script, system dependent
        runtime_config = self._system_runtime_config()
        self._update_run_script(runtime_config)

        # write run-script to working directory
        self._run_script.write(os.path.join(self.work_dir, self.run_id + ".run"))
        self._inputs.append(self.run_script)

        # update command, so job can actually run.
        self.command = self.run_script

        # stage input files
        self._stage_inputs()
        self._prepared = True
        self.status = JobStatus.PREPARED

    def run(self):
        if not self._prepared:
            self.prepare()
        print(f"Executing {self.command} with arguments {self.args}")
        rc = self._system.execute(' '.join([self.command, self.args]))
        return rc

    @property
    def run_script(self):
        if self._run_script is None:
            return None
        return self._run_script.path

    @property
    def config_file(self):
        if self._config is None:
            return None
        return self._config.path

    def update_configuration(self, adict={}):
        """ Updates UCERF3 configuration file with correct inputs. """
        self._config_templ_file = JsonFile(self._config_templ)

        # just bind adict to template file object for now,
        # want to perform this lazily in case there is an error
        self._config_templ_file.config = adict

    def _update_run_script(self, adict={}):
        """
        Updates run script with parameters needed to run the job.

        Returns:

        """
        if self._script_templ is None:
            raise CSEPSchedulerException("Cannot generate run-script without knowing the location"
                                         " of the template.")
        run_script = TextFile(self._script_templ)
        self._run_script = run_script.template(adict)

    def _system_runtime_config(self):
        """
    Returns dict of configuration parameters necessary to update run-script.

    Returns:
        new (dict): new params that are needed to run UCERF3 on particular system
    """

        if self._system is None:
            raise CSEPSchedulerException("Cannot generate configuration information for system"
                                         " with no system bound.")
        out = {}
        if self._system.name == "hpc-usc":
            out['partition'] = self._system.partition
            out['email'] = self._system.email
            out['nodes'] = self.nnodes
            out['time'] = self.max_run_time
            out['config'] = self.config_file
            out['mpj_home'] = self._system.mpj_home
        return out

class Evaluation(BaseTask):
    pass


job_builder = ObjectFactory()
job_builder.register_builder('base', BaseTask.from_dict)
job_builder.register_builder('ucerf3-etas', UCERF3Forecast.from_dict)