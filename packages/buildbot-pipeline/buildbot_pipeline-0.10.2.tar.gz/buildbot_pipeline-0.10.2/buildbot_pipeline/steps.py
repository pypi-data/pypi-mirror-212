import os.path
import itertools
import json
import yaml
import re
from pathlib import Path

from buildbot.process import buildstep, logobserver, results, properties
from buildbot.steps.transfer import MultipleFileUpload
from buildbot.steps.trigger import Trigger
from buildbot.steps.source import git

from twisted.internet import defer
from twisted.python.failure import Failure

from buildbot_pipeline import junit, utils, filters, file_store, build

DEFAULT_STEPSDIR = 'buildbot'
HIDDEN = 'hidden'


def process_interpolate(value):
    if type(value) is str:
        if value.startswith('!'):
            return properties.Interpolate(value[1:])
        elif value.startswith(r'@'):
            return value[1:]
        elif '%(' in value:
            return properties.Interpolate(value)
        else:
            return value
    elif type(value) is list:
        return [process_interpolate(v) for v in value]
    elif type(value) is dict:
        return {k: process_interpolate(v) for k, v in value.items()}
    else:
        return value


def gen_steps(step, data):
    if type(data) is list:
        return [gen_steps(step, it) for it in data]

    if 'shell-fail' in data:
        data['shell'] = data.pop('shell-fail')
        data['haltOnFailure'] = True

    if 'shell' in data:
        data['command'] = data.pop('shell')
        step_env = data.get('env', {})
        data['env'] = step.build.pipeline_env.copy()
        data['env'].update(step_env)
        data = process_interpolate(data)
        data['env']['BUILD_ID'] = properties.Interpolate('%(prop:pipeline_buildnumber:-%(prop:buildnumber)s)s')
        data['env']['WORKSPACE'] = properties.Interpolate('%(prop:builddir)s')
        return DynamicStep(**data)
    elif 'steps' in data:
        return [gen_steps(step, it) for it in data['steps']]
    elif 'parallel' in data:
        info = data['parallel']
        if type(info) is list:
            info = {'steps': info}

        matrix = info.pop('matrix', None)
        steps = info.pop('steps', [])
        if matrix:
            steps.insert(0, {'matrix': matrix})

        info.pop('inner', None)
        return Parallel(list(matrix_steps(steps)), **info)
    elif 'git' in data:
        data = process_interpolate(data)
        data.pop('git')
        data.update(_vcs_opts)
        return git.Git(**data)

    raise Exception(f'Unknown step {data}')


def matrix_steps(steps):
    for info in steps:
        if 'matrix' in info:
            step_desc = info['matrix']
            name = step_desc.pop('name', None)
            all_params = step_desc.pop('params', [])
            for params in utils.ensure_list(all_params):
                params.pop('workername', None)
                params = list(params.items())
                params_keys = [it[0] for it in params]
                params_values = [utils.ensure_list(it[1]) for it in params]
                for pvals in itertools.product(*params_values):
                    props = dict(zip(params_keys, pvals))
                    s = step_desc.copy()
                    s['properties'] = s.get('properties', {}).copy()
                    s['properties'].update(props)
                    s['name'] = name.format(**props) if name else '-'.join(map(str, pvals))
                    yield s
        else:
            yield info


class Parallel(Trigger):
    def __init__(self, steps_info, inner=True, **kwargs):
        kwargs.setdefault('waitForFinish', True)
        super().__init__('trig-prop-builder', **kwargs)
        self.steps_info = steps_info
        self.correct_names = [it['name'] for it in steps_info]
        self.inner = inner

    def getAllGotRevisions(self):
        # annotated tags can skew revision so we need to get original revision
        # instead of got_revision property
        revisions = self.getProperty('revision', {})
        if not isinstance(revisions, dict):
            revisions = {'': revisions}
        return revisions

    @defer.inlineCallbacks
    def getSchedulersAndProperties(self):
        if self.inner:
            builder_name = self.getProperty('parent_builder_name') or self.getProperty('virtual_builder_name') or self.getProperty('buildername')
            worker_name = self.getProperty('workername')
            builddir = self.getProperty('builddir')
            root_buildnumber = self.getProperty('pipeline_buildnumber') or self.getProperty('buildnumber')

        result = []
        for it in self.steps_info:
            s = {
                'sched_name': 'trig-prop-builder',
                'props_to_set': {
                    'steps_info': json.dumps(it),
                },
                'unimportant': False
            }

            passthrough_propnames = self.getProperty('pipeline_passthrough_props') or []
            props = {k: self.getProperty(k) for k in passthrough_propnames}
            props.update(it.get('properties', {}))
            props = yield self.render(process_interpolate(props))
            s['props_to_set'].update(props)

            if self.inner:
                s['props_to_set'].update(
                    virtual_builder_name=f"{builder_name}/{it['name']}",
                    virtual_builder_title=it['name'],
                    virtual_builder_tags=[HIDDEN],
                    workername=worker_name,
                    parent_builder_name=builder_name,
                    pipeline_builddir=builddir,
                    pipeline_builder_prefix='~prop-inner-builder',
                    pipeline_buildnumber=root_buildnumber,
                )
            else:
                s['props_to_set'].update(
                   virtual_builder_name=it['name'],
                   virtual_builder_tags=[],
                   pipeline_builder_prefix='~prop-builder',
                   reporters='gerrit',
                   pipeline_concurrency=str(it.get('concurrency', 1)),
                )

            result.append(s)
        return result

    def getCurrentSummary(self):
        if self.triggeredNames:
            self.triggeredNames = self.correct_names
        return super().getCurrentSummary()


class PropStep(buildstep.BuildStep):
    hideStepIf = staticmethod(utils.hide_if_success)
    name = 'init'

    @defer.inlineCallbacks
    def checkAlreadyPassed(self):
        ss = self.build.getSourceStamp()
        if not ss:
            return None

        bid = yield self.build.getBuilderId()
        build = yield utils.get_last_successful_build_for_sourcestamp(self.master, bid, ss.ssid)
        if build:
            self.addURL('Last successful build', f'#/builders/{build.builderid}/builds/{build.number}')
            self.descriptionDone = ['Already passed']
            self.build.results = results.SKIPPED
            return True

    @defer.inlineCallbacks
    def run(self):
        steps_info = json.loads(self.getProperty('steps_info', '{}'))

        if type(steps_info) is dict and steps_info.get('skip_passed'):
            already_passed = yield self.checkAlreadyPassed()
            if already_passed:
                return results.SKIPPED

        self.build.pipeline_env = {}
        if type(steps_info) is dict:
            self.build.pipeline_env = steps_info.get('env', {})

        self.build.addStepsAfterCurrentStep(utils.ensure_list(gen_steps(self, steps_info)))
        return results.SUCCESS


class GatherBuilders(buildstep.BuildStep):
    haltOnFailure = True
    name = 'parse builders'

    @defer.inlineCallbacks
    def run(self):
        workdir = os.path.join(self.getProperty('builddir'), self.workdir)

        build_props = self.getProperty('pipeline_build_props', {})
        forced_builders = build_props.get('builders')
        common_props = build_props.get('common_props', {})
        builder_props = build_props.get('builder_props', {})

        result = results.SUCCESS
        step_info = []
        repo_path = Path(workdir)
        buildbot_path = repo_path / self.getProperty('pipeline_stepsdir', DEFAULT_STEPSDIR)
        changes = list(self.build.allChanges())
        for it in buildbot_path.glob('**/*.yaml'):
            it_repo_path = str(it.relative_to(repo_path))
            name, _, _ = str(it.relative_to(buildbot_path)).rpartition('.')
            try:
                with open(it) as f:
                    step = yaml.safe_load(f)
            except Exception as e:
                result = results.WARNINGS
                yield self.addCompleteLog(name, Failure(e).getTraceback())
            else:
                repo = self.getProperty('repository')
                step['name'] = name
                if 'steps' in step:
                    step['steps'].insert(0, {'git': True, 'repourl': repo})

                skip_reason = 'unknown'
                start_build = None
                if forced_builders and name in forced_builders:
                    start_build = True

                if step.get('disabled'):
                    start_build = False
                    skip_reason = 'disabled'

                if changes:
                    if start_build is None and it_repo_path in changes[0].files:
                        start_build = True

                    if start_build is None and 'filter' in step:
                        if 'status' not in step['filter']:
                            step['filter']['status'] = 'new'

                        try:
                            flt = filters.make_filters(step['filter'])
                        except Exception as e:
                            result = results.WARNINGS
                            skip_reason = str(e)
                            yield self.addCompleteLog(name, str(e))
                        else:
                            changes[0].props = self.getProperties()
                            if flt and flt(changes[0]):
                                start_build = True
                            else:
                                skip_reason = 'filter'

                if start_build:
                    props = step.get('properties', {}).copy()
                    props.update(common_props)
                    props.update(builder_props.get(name, {}))
                    props['pipeline_passthrough_props'] = list(props) + ['pipeline_passthrough_props']
                    step['properties'] = props
                    step_info.append(step)
                else:
                    yield self.addCompleteLog(name, f'skipped by: {skip_reason}')

        if step_info:
            self.build.addStepsAfterCurrentStep([Parallel(step_info, inner=False, waitForFinish=False)])
            return result

        self.descriptionDone = ['There are no suitable jobs']
        self.build.results = results.SKIPPED
        return results.SKIPPED


class DistributeStep(buildstep.BuildStep):
    def run(self):
        repo = self.getProperty('repository')
        _, _, self.build.workdir = repo.rpartition('/')
        self.build.addStepsAfterCurrentStep([git.Git(repourl=repo, **_vcs_opts), GatherBuilders()])
        return results.SUCCESS


class DynamicStep(buildstep.ShellMixin, buildstep.BuildStep):
    logEnviron = False

    def __init__(self, **kwargs):
        self.junit = kwargs.pop('junit', None)
        self.upload = kwargs.pop('upload', None)
        kwargs = self.setupShellMixin(kwargs)
        super().__init__(**kwargs)
        self.observer = logobserver.BufferLogObserver()
        self.addLogObserver('stdio', self.observer)

    def extract_steps(self, stdout):
        m = re.search('(?s)__PIPELINE_' + 'START__(.*)__PIPELINE_' + 'END__', stdout)
        if not m:
            return []

        data = yaml.safe_load(m[1])
        return utils.ensure_list(gen_steps(self, data))

    @defer.inlineCallbacks
    def run(self):
        cmd = yield self.makeRemoteShellCommand()
        yield self.runCommand(cmd)
        result = cmd.results()
        if result == results.SUCCESS:
            self.build.addStepsAfterCurrentStep(self.extract_steps(self.observer.getStdout()))

        if self.junit:
            for desc in utils.ensure_list(self.junit):
                yield self.handleJUnit(desc)

        if self.upload:
            for desc in utils.ensure_list(self.upload):
                yield self.handleUpload(desc)

        return result

    @defer.inlineCallbacks
    def handleJUnit(self, desc):
        desc = yield self.render(desc)
        if type(desc) is dict:
            label = desc.get('label')
            src = desc.get('src')
        else:
            label = None
            src = desc

        if not src:
            return

        wd = utils.get_workdir(self)
        rv = yield utils.silent_remote_command(self, 'glob', path=os.path.join(wd, src))
        for fname in rv.updates['files'][0]:
            writer = utils.BufWriter()

            rv = yield utils.silent_remote_command(
                self, 'uploadFile', workdir='/', workersrc=fname, writer=writer,
                blocksize=16384, maxsize=1 << 20, keepstamp=False)

            if rv.rc == results.SUCCESS:
                writer.buf.seek(0)
                suites = junit.parse(writer.buf)
                writer.buf.close()
                h = junit.gen_html(suites, embed=True)
                n = label or (suites and suites[0]['name'] or 'tests')
                yield self.addHTMLLog(n, h)

    @defer.inlineCallbacks
    def handleUpload(self, desc):
        desc = yield self.render(desc)
        bname = build.builder_name_to_path(self.getProperty('virtual_builder_name') or self.getProperty('buildername'))
        bnum = self.getProperty('pipeline_buildnumber') or self.getProperty('buildnumber')

        build_storage_path = os.path.realpath(os.path.join(file_store.ep.path, bname, str(bnum)))
        if desc.get('dest'):
            dest = os.path.realpath(os.path.join(build_storage_path, desc['dest']))
            if len(os.path.commonpath([dest, build_storage_path])) < len(build_storage_path):
                raise Exception('Upload destination path should be relative to build storage path')
        else:
            dest = build_storage_path

        cmd = MultipleFileUpload(
            workersrcs=utils.ensure_list(desc['src']),
            glob=True,
            url=f'/file-store/{bname}/{bnum}/' + desc.get('link', ''),
            urlText=desc.get('label'),
            masterdest=dest)

        cmd.setBuild(self.build)
        cmd.setWorker(self.worker)
        cmd.stepid = self.stepid
        cmd._running = True
        cmd.remote = self.remote
        cmd.addLog = lambda name: defer.succeed(self.getLog(name))
        yield cmd.run()


_vcs_opts = {'logEnviron': False, 'mode': 'full', 'method': 'fresh'}
