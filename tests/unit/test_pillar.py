# -*- coding: utf-8 -*-
'''
    :codeauthor: :email:`Pedro Algarvio (pedro@algarvio.me)`
    :codeauthor: :email:`Alexandru Bleotu (alexandru.bleotu@morganstanley.com)`


    tests.unit.pillar_test
    ~~~~~~~~~~~~~~~~~~~~~~
'''

# Import python libs
from __future__ import absolute_import
import tempfile

# Import Salt Testing libs
from tests.support.unit import skipIf, TestCase
from tests.support.mock import NO_MOCK, NO_MOCK_REASON, MagicMock, patch
from tests.support.paths import TMP

# Import salt libs
import salt.pillar
import salt.utils.stringutils
import salt.exceptions


@skipIf(NO_MOCK, NO_MOCK_REASON)
class PillarTestCase(TestCase):

    def tearDown(self):
        for attrname in ('generic_file', 'generic_minion_file', 'ssh_file', 'ssh_minion_file', 'top_file'):
            try:
                delattr(self, attrname)
            except AttributeError:
                continue

    def test_pillarenv_from_saltenv(self):
        with patch('salt.pillar.compile_template') as compile_template:
            opts = {
                'renderer': 'json',
                'renderer_blacklist': [],
                'renderer_whitelist': [],
                'state_top': '',
                'pillar_roots': {
                    'dev': [],
                    'base': []
                },
                'file_roots': {
                    'dev': [],
                    'base': []
                },
                'extension_modules': '',
                'pillarenv_from_saltenv': True
            }
            grains = {
                'os': 'Ubuntu',
            }
            pillar = salt.pillar.Pillar(opts, grains, 'mocked-minion', 'dev')
            self.assertEqual(pillar.opts['saltenv'], 'dev')
            self.assertEqual(pillar.opts['pillarenv'], 'dev')

    def test_ext_pillar_no_extra_minion_data_val_dict(self):
        opts = {
            'renderer': 'json',
            'renderer_blacklist': [],
            'renderer_whitelist': [],
            'state_top': '',
            'pillar_roots': {
                'dev': [],
                'base': []
            },
            'file_roots': {
                'dev': [],
                'base': []
            },
            'extension_modules': '',
            'pillarenv_from_saltenv': True
        }
        mock_ext_pillar_func = MagicMock()
        with patch('salt.loader.pillars',
                   MagicMock(return_value={'fake_ext_pillar':
                                           mock_ext_pillar_func})):
            pillar = salt.pillar.Pillar(opts, {}, 'mocked-minion', 'dev')
        # ext pillar function doesn't have the extra_minion_data arg
        with patch('salt.utils.args.get_function_argspec',
                   MagicMock(return_value=MagicMock(args=[]))):
            pillar._external_pillar_data('fake_pillar', {'arg': 'foo'},
                                         'fake_ext_pillar')
        mock_ext_pillar_func.assert_called_once_with('mocked-minion',
                                                     'fake_pillar',
                                                     arg='foo')
        # ext pillar function has the extra_minion_data arg
        mock_ext_pillar_func.reset_mock()
        with patch('salt.utils.args.get_function_argspec',
                   MagicMock(return_value=MagicMock(args=['extra_minion_data']))):
            pillar._external_pillar_data('fake_pillar', {'arg': 'foo'},
                                         'fake_ext_pillar')
        mock_ext_pillar_func.assert_called_once_with('mocked-minion',
                                                     'fake_pillar',
                                                     arg='foo')

    def test_ext_pillar_no_extra_minion_data_val_list(self):
        opts = {
            'renderer': 'json',
            'renderer_blacklist': [],
            'renderer_whitelist': [],
            'state_top': '',
            'pillar_roots': {
                'dev': [],
                'base': []
            },
            'file_roots': {
                'dev': [],
                'base': []
            },
            'extension_modules': '',
            'pillarenv_from_saltenv': True
        }
        mock_ext_pillar_func = MagicMock()
        with patch('salt.loader.pillars',
                   MagicMock(return_value={'fake_ext_pillar':
                                           mock_ext_pillar_func})):
            pillar = salt.pillar.Pillar(opts, {}, 'mocked-minion', 'dev')
        # ext pillar function doesn't have the extra_minion_data arg
        with patch('salt.utils.args.get_function_argspec',
                   MagicMock(return_value=MagicMock(args=[]))):
            pillar._external_pillar_data('fake_pillar', ['foo'],
                                         'fake_ext_pillar')
        mock_ext_pillar_func.assert_called_once_with('mocked-minion',
                                                     'fake_pillar',
                                                     'foo')
        # ext pillar function has the extra_minion_data arg
        mock_ext_pillar_func.reset_mock()
        with patch('salt.utils.args.get_function_argspec',
                   MagicMock(return_value=MagicMock(args=['extra_minion_data']))):
            pillar._external_pillar_data('fake_pillar', ['foo'],
                                         'fake_ext_pillar')
        mock_ext_pillar_func.assert_called_once_with('mocked-minion',
                                                     'fake_pillar',
                                                     'foo')

    def test_ext_pillar_no_extra_minion_data_val_elem(self):
        opts = {
            'renderer': 'json',
            'renderer_blacklist': [],
            'renderer_whitelist': [],
            'state_top': '',
            'pillar_roots': {
                'dev': [],
                'base': []
            },
            'file_roots': {
                'dev': [],
                'base': []
            },
            'extension_modules': '',
            'pillarenv_from_saltenv': True
        }
        mock_ext_pillar_func = MagicMock()
        with patch('salt.loader.pillars',
                   MagicMock(return_value={'fake_ext_pillar':
                                           mock_ext_pillar_func})):
            pillar = salt.pillar.Pillar(opts, {}, 'mocked-minion', 'dev')
        # ext pillar function doesn't have the extra_minion_data arg
        with patch('salt.utils.args.get_function_argspec',
                   MagicMock(return_value=MagicMock(args=[]))):
            pillar._external_pillar_data('fake_pillar', 'fake_val',
                                         'fake_ext_pillar')
        mock_ext_pillar_func.assert_called_once_with('mocked-minion',
                                                     'fake_pillar', 'fake_val')
        # ext pillar function has the extra_minion_data arg
        mock_ext_pillar_func.reset_mock()
        with patch('salt.utils.args.get_function_argspec',
                   MagicMock(return_value=MagicMock(args=['extra_minion_data']))):
            pillar._external_pillar_data('fake_pillar', 'fake_val',
                                         'fake_ext_pillar')
        mock_ext_pillar_func.assert_called_once_with('mocked-minion',
                                                     'fake_pillar', 'fake_val')

    def test_ext_pillar_with_extra_minion_data_val_dict(self):
        opts = {
            'renderer': 'json',
            'renderer_blacklist': [],
            'renderer_whitelist': [],
            'state_top': '',
            'pillar_roots': {
                'dev': [],
                'base': []
            },
            'file_roots': {
                'dev': [],
                'base': []
            },
            'extension_modules': '',
            'pillarenv_from_saltenv': True
        }
        mock_ext_pillar_func = MagicMock()
        with patch('salt.loader.pillars',
                   MagicMock(return_value={'fake_ext_pillar':
                                           mock_ext_pillar_func})):
            pillar = salt.pillar.Pillar(opts, {}, 'mocked-minion', 'dev',
                                        extra_minion_data={'fake_key': 'foo'})
        # ext pillar function doesn't have the extra_minion_data arg
        with patch('salt.utils.args.get_function_argspec',
                   MagicMock(return_value=MagicMock(args=[]))):
            pillar._external_pillar_data('fake_pillar', {'arg': 'foo'},
                                         'fake_ext_pillar')
        mock_ext_pillar_func.assert_called_once_with(
            'mocked-minion', 'fake_pillar', arg='foo')
        # ext pillar function has the extra_minion_data arg
        mock_ext_pillar_func.reset_mock()
        with patch('salt.utils.args.get_function_argspec',
                   MagicMock(return_value=MagicMock(args=['extra_minion_data']))):
            pillar._external_pillar_data('fake_pillar', {'arg': 'foo'},
                                         'fake_ext_pillar')
        mock_ext_pillar_func.assert_called_once_with(
            'mocked-minion', 'fake_pillar', arg='foo',
            extra_minion_data={'fake_key': 'foo'})

    def test_ext_pillar_with_extra_minion_data_val_list(self):
        opts = {
            'renderer': 'json',
            'renderer_blacklist': [],
            'renderer_whitelist': [],
            'state_top': '',
            'pillar_roots': {
                'dev': [],
                'base': []
            },
            'file_roots': {
                'dev': [],
                'base': []
            },
            'extension_modules': '',
            'pillarenv_from_saltenv': True
        }
        mock_ext_pillar_func = MagicMock()
        with patch('salt.loader.pillars',
                   MagicMock(return_value={'fake_ext_pillar':
                                           mock_ext_pillar_func})):
            pillar = salt.pillar.Pillar(opts, {}, 'mocked-minion', 'dev',
                                        extra_minion_data={'fake_key': 'foo'})
        # ext pillar function doesn't have the extra_minion_data arg
        with patch('salt.utils.args.get_function_argspec',
                   MagicMock(return_value=MagicMock(args=[]))):
            pillar._external_pillar_data('fake_pillar', ['bar'],
                                         'fake_ext_pillar')
        mock_ext_pillar_func.assert_called_once_with(
            'mocked-minion', 'fake_pillar', 'bar')
        # ext pillar function has the extra_minion_data arg
        mock_ext_pillar_func.reset_mock()
        with patch('salt.utils.args.get_function_argspec',
                   MagicMock(return_value=MagicMock(args=['extra_minion_data']))):
            pillar._external_pillar_data('fake_pillar', ['bar'],
                                         'fake_ext_pillar')
        mock_ext_pillar_func.assert_called_once_with(
            'mocked-minion', 'fake_pillar', 'bar',
            extra_minion_data={'fake_key': 'foo'})

    def test_ext_pillar_with_extra_minion_data_val_elem(self):
        opts = {
            'renderer': 'json',
            'renderer_blacklist': [],
            'renderer_whitelist': [],
            'state_top': '',
            'pillar_roots': {
                'dev': [],
                'base': []
            },
            'file_roots': {
                'dev': [],
                'base': []
            },
            'extension_modules': '',
            'pillarenv_from_saltenv': True
        }
        mock_ext_pillar_func = MagicMock()
        with patch('salt.loader.pillars',
                   MagicMock(return_value={'fake_ext_pillar':
                                           mock_ext_pillar_func})):
            pillar = salt.pillar.Pillar(opts, {}, 'mocked-minion', 'dev',
                                        extra_minion_data={'fake_key': 'foo'})
        # ext pillar function doesn't have the extra_minion_data arg
        with patch('salt.utils.args.get_function_argspec',
                   MagicMock(return_value=MagicMock(args=[]))):
            pillar._external_pillar_data('fake_pillar', 'bar',
                                         'fake_ext_pillar')
        mock_ext_pillar_func.assert_called_once_with(
            'mocked-minion', 'fake_pillar', 'bar')
        # ext pillar function has the extra_minion_data arg
        mock_ext_pillar_func.reset_mock()
        with patch('salt.utils.args.get_function_argspec',
                   MagicMock(return_value=MagicMock(args=['extra_minion_data']))):
            pillar._external_pillar_data('fake_pillar', 'bar',
                                         'fake_ext_pillar')
        mock_ext_pillar_func.assert_called_once_with(
            'mocked-minion', 'fake_pillar', 'bar',
            extra_minion_data={'fake_key': 'foo'})

    def test_dynamic_pillarenv(self):
        opts = {
            'renderer': 'json',
            'renderer_blacklist': [],
            'renderer_whitelist': [],
            'state_top': '',
            'pillar_roots': {'__env__': ['/srv/pillar/__env__'], 'base': ['/srv/pillar/base']},
            'file_roots': {'base': ['/srv/salt/base'], 'dev': ['/svr/salt/dev']},
            'extension_modules': '',
        }
        pillar = salt.pillar.Pillar(opts, {}, 'mocked-minion', 'base', pillarenv='dev')
        self.assertEqual(pillar.opts['file_roots'],
                         {'base': ['/srv/pillar/base'], 'dev': ['/srv/pillar/__env__']})

    def test_ignored_dynamic_pillarenv(self):
        opts = {
            'renderer': 'json',
            'renderer_blacklist': [],
            'renderer_whitelist': [],
            'state_top': '',
            'pillar_roots': {'__env__': ['/srv/pillar/__env__'], 'base': ['/srv/pillar/base']},
            'file_roots': {'base': ['/srv/salt/base'], 'dev': ['/svr/salt/dev']},
            'extension_modules': '',
        }
        pillar = salt.pillar.Pillar(opts, {}, 'mocked-minion', 'base', pillarenv='base')
        self.assertEqual(pillar.opts['file_roots'], {'base': ['/srv/pillar/base']})

    @patch('salt.fileclient.Client.list_states')
    def test_malformed_pillar_sls(self, mock_list_states):
        with patch('salt.pillar.compile_template') as compile_template:
            opts = {
                'renderer': 'json',
                'renderer_blacklist': [],
                'renderer_whitelist': [],
                'state_top': '',
                'pillar_roots': [],
                'file_roots': [],
                'extension_modules': ''
            }
            grains = {
                'os': 'Ubuntu',
                'os_family': 'Debian',
                'oscodename': 'raring',
                'osfullname': 'Ubuntu',
                'osrelease': '13.04',
                'kernel': 'Linux'
            }

            mock_list_states.return_value = ['foo', 'blah']
            pillar = salt.pillar.Pillar(opts, grains, 'mocked-minion', 'base')
            # Mock getting the proper template files
            pillar.client.get_state = MagicMock(
                return_value={
                    'dest': '/path/to/pillar/files/foo.sls',
                    'source': 'salt://foo.sls'
                }
            )

            # Template compilation returned a string
            compile_template.return_value = 'BAHHH'
            self.assertEqual(
                pillar.render_pillar({'base': ['foo.sls']}),
                ({}, ['SLS \'foo.sls\' does not render to a dictionary'])
            )

            # Template compilation returned a list
            compile_template.return_value = ['BAHHH']
            self.assertEqual(
                pillar.render_pillar({'base': ['foo.sls']}),
                ({}, ['SLS \'foo.sls\' does not render to a dictionary'])
            )

            # Template compilation returned a dictionary, which is what's expected
            compile_template.return_value = {'foo': 'bar'}
            self.assertEqual(
                pillar.render_pillar({'base': ['foo.sls']}),
                ({'foo': 'bar'}, [])
            )

            # Test improper includes
            compile_template.side_effect = [
                {'foo': 'bar', 'include': 'blah'},
                {'foo2': 'bar2'}
            ]
            self.assertEqual(
                pillar.render_pillar({'base': ['foo.sls']}),
                ({'foo': 'bar', 'include': 'blah'},
                 ["Include Declaration in SLS 'foo.sls' is not formed as a list"])
            )

            # Test includes as a list, which is what's expected
            compile_template.side_effect = [
                {'foo': 'bar', 'include': ['blah']},
                {'foo2': 'bar2'}
            ]
            self.assertEqual(
                pillar.render_pillar({'base': ['foo.sls']}),
                ({'foo': 'bar', 'foo2': 'bar2'}, [])
            )

            # Test includes as a list overriding data
            compile_template.side_effect = [
                {'foo': 'bar', 'include': ['blah']},
                {'foo': 'bar2'}
            ]
            self.assertEqual(
                pillar.render_pillar({'base': ['foo.sls']}),
                ({'foo': 'bar'}, [])
            )

            # Test includes using empty key directive
            compile_template.side_effect = [
                {'foo': 'bar', 'include': [{'blah': {'key': ''}}]},
                {'foo': 'bar2'}
            ]
            self.assertEqual(
                pillar.render_pillar({'base': ['foo.sls']}),
                ({'foo': 'bar'}, [])
            )

            # Test includes using simple non-nested key
            compile_template.side_effect = [
                {'foo': 'bar', 'include': [{'blah': {'key': 'nested'}}]},
                {'foo': 'bar2'}
            ]
            self.assertEqual(
                pillar.render_pillar({'base': ['foo.sls']}),
                ({'foo': 'bar', 'nested': {'foo': 'bar2'}}, [])
            )

            # Test includes using nested key
            compile_template.side_effect = [
                {'foo': 'bar', 'include': [{'blah': {'key': 'nested:level'}}]},
                {'foo': 'bar2'}
            ]
            self.assertEqual(
                pillar.render_pillar({'base': ['foo.sls']}),
                ({'foo': 'bar', 'nested': {'level': {'foo': 'bar2'}}}, [])
            )

    def test_includes_override_sls(self):
        opts = {
            'renderer': 'json',
            'renderer_blacklist': [],
            'renderer_whitelist': [],
            'state_top': '',
            'pillar_roots': {},
            'file_roots': {},
            'extension_modules': ''
        }
        grains = {
            'os': 'Ubuntu',
            'os_family': 'Debian',
            'oscodename': 'raring',
            'osfullname': 'Ubuntu',
            'osrelease': '13.04',
            'kernel': 'Linux'
        }
        with patch('salt.pillar.compile_template') as compile_template, \
                patch.object(salt.pillar.Pillar, '_Pillar__gather_avail',
                             MagicMock(return_value={'base': ['blah', 'foo']})):

            # Test with option set to True
            opts['pillar_includes_override_sls'] = True
            pillar = salt.pillar.Pillar(opts, grains, 'mocked-minion', 'base')
            # Mock getting the proper template files
            pillar.client.get_state = MagicMock(
                return_value={
                    'dest': '/path/to/pillar/files/foo.sls',
                    'source': 'salt://foo.sls'
                }
            )

            compile_template.side_effect = [
                {'foo': 'bar', 'include': ['blah']},
                {'foo': 'bar2'}
            ]
            self.assertEqual(
                pillar.render_pillar({'base': ['foo.sls']}),
                ({'foo': 'bar2'}, [])
            )

            # Test with option set to False
            opts['pillar_includes_override_sls'] = False
            pillar = salt.pillar.Pillar(opts, grains, 'mocked-minion', 'base')
            # Mock getting the proper template files
            pillar.client.get_state = MagicMock(
                return_value={
                    'dest': '/path/to/pillar/files/foo.sls',
                    'source': 'salt://foo.sls'
                }
            )

            compile_template.side_effect = [
                {'foo': 'bar', 'include': ['blah']},
                {'foo': 'bar2'}
            ]
            self.assertEqual(
                pillar.render_pillar({'base': ['foo.sls']}),
                ({'foo': 'bar'}, [])
            )

    def test_topfile_order(self):
        with patch('salt.pillar.salt.fileclient.get_file_client', autospec=True) as get_file_client, \
                patch('salt.pillar.salt.minion.Matcher') as Matcher:  # autospec=True disabled due to py3 mock bug
            opts = {
                'renderer': 'yaml',
                'renderer_blacklist': [],
                'renderer_whitelist': [],
                'state_top': '',
                'pillar_roots': [],
                'extension_modules': '',
                'saltenv': 'base',
                'file_roots': [],
            }
            grains = {
                'os': 'Ubuntu',
                'os_family': 'Debian',
                'oscodename': 'raring',
                'osfullname': 'Ubuntu',
                'osrelease': '13.04',
                'kernel': 'Linux'
            }
            # glob match takes precedence
            self._setup_test_topfile_mocks(Matcher, get_file_client, 1, 2)
            pillar = salt.pillar.Pillar(opts, grains, 'mocked-minion', 'base')
            self.assertEqual(pillar.compile_pillar()['ssh'], 'bar')
            # nodegroup match takes precedence
            self._setup_test_topfile_mocks(Matcher, get_file_client, 2, 1)
            pillar = salt.pillar.Pillar(opts, grains, 'mocked-minion', 'base')
            self.assertEqual(pillar.compile_pillar()['ssh'], 'foo')

    def _setup_test_topfile_mocks(self, Matcher, get_file_client,
                                  nodegroup_order, glob_order):
        # Write a simple topfile and two pillar state files
        self.top_file = tempfile.NamedTemporaryFile(dir=TMP, delete=False)
        s = '''
base:
    group:
        - match: nodegroup
        - order: {nodegroup_order}
        - ssh
        - generic
    '*':
        - generic
    minion:
        - order: {glob_order}
        - ssh.minion
        - generic.minion
'''.format(nodegroup_order=nodegroup_order, glob_order=glob_order)
        self.top_file.write(salt.utils.stringutils.to_bytes(s))
        self.top_file.flush()
        self.ssh_file = tempfile.NamedTemporaryFile(dir=TMP, delete=False)
        self.ssh_file.write(b'''
ssh:
    foo
''')
        self.ssh_file.flush()
        self.ssh_minion_file = tempfile.NamedTemporaryFile(dir=TMP, delete=False)
        self.ssh_minion_file.write(b'''
ssh:
    bar
''')
        self.ssh_minion_file.flush()
        self.generic_file = tempfile.NamedTemporaryFile(dir=TMP, delete=False)
        self.generic_file.write(b'''
generic:
    key1:
      - value1
      - value2
    key2:
        sub_key1: []
''')
        self.generic_file.flush()
        self.generic_minion_file = tempfile.NamedTemporaryFile(dir=TMP, delete=False)
        self.generic_minion_file.write(b'''
generic:
    key1:
      - value3
    key2:
        sub_key2: []
''')
        self.generic_minion_file.flush()

        # Setup Matcher mock
        matcher = Matcher.return_value
        matcher.confirm_top.return_value = True

        # Setup fileclient mock
        client = get_file_client.return_value
        client.cache_file.return_value = self.top_file.name

        def get_state(sls, env):
            return {
                'ssh': {'path': '', 'dest': self.ssh_file.name},
                'ssh.minion': {'path': '', 'dest': self.ssh_minion_file.name},
                'generic': {'path': '', 'dest': self.generic_file.name},
                'generic.minion': {'path': '', 'dest': self.generic_minion_file.name},
            }[sls]

        client.get_state.side_effect = get_state

    def test_include(self):
        with patch('salt.pillar.salt.fileclient.get_file_client', autospec=True) as get_file_client, \
            patch('salt.pillar.salt.minion.Matcher') as Matcher:  # autospec=True disabled due to py3 mock bug
            opts = {
                'renderer': 'yaml',
                'renderer_blacklist': [],
                'renderer_whitelist': [],
                'state_top': '',
                'pillar_roots': [],
                'extension_modules': '',
                'saltenv': 'base',
                'file_roots': [],
            }
            grains = {
                'os': 'Ubuntu',
                'os_family': 'Debian',
                'oscodename': 'raring',
                'osfullname': 'Ubuntu',
                'osrelease': '13.04',
                'kernel': 'Linux'
            }

            self._setup_test_include_mocks(Matcher, get_file_client)
            pillar = salt.pillar.Pillar(opts, grains, 'minion', 'base')
            compiled_pillar = pillar.compile_pillar()
            self.assertEqual(compiled_pillar['foo_wildcard'], 'bar_wildcard')
            self.assertEqual(compiled_pillar['foo1'], 'bar1')
            self.assertEqual(compiled_pillar['foo2'], 'bar2')

    def _setup_test_include_mocks(self, Matcher, get_file_client):
        self.top_file = top_file = tempfile.NamedTemporaryFile(dir=TMP, delete=False)
        top_file.write(b'''
base:
    '*':
        - order: 1
        - test.sub2
    minion:
        - order: 2
        - test
''')
        top_file.flush()
        self.init_sls = init_sls = tempfile.NamedTemporaryFile(dir=TMP, delete=False)
        init_sls.write(b'''
include:
   - test.sub1
   - test.sub_wildcard*
''')
        init_sls.flush()
        self.sub1_sls = sub1_sls = tempfile.NamedTemporaryFile(dir=TMP, delete=False)
        sub1_sls.write(b'''
foo1:
  bar1
''')
        sub1_sls.flush()
        self.sub2_sls = sub2_sls = tempfile.NamedTemporaryFile(dir=TMP, delete=False)
        sub2_sls.write(b'''
foo2:
  bar2
''')
        sub2_sls.flush()

        self.sub_wildcard_1_sls = sub_wildcard_1_sls = tempfile.NamedTemporaryFile(dir=TMP, delete=False)
        sub_wildcard_1_sls.write(b'''
foo_wildcard:
   bar_wildcard
''')
        sub_wildcard_1_sls.flush()
        # Setup Matcher mock
        matcher = Matcher.return_value
        matcher.confirm_top.return_value = True

        # Setup fileclient mock
        client = get_file_client.return_value
        client.cache_file.return_value = self.top_file.name
        client.list_states.return_value = ['top', 'test.init', 'test.sub1', 'test.sub2', 'test.sub_wildcard_1']

        def get_state(sls, env):
            return {
                'test': {'path': '', 'dest': init_sls.name},
                'test.sub1': {'path': '', 'dest': sub1_sls.name},
                'test.sub2': {'path': '', 'dest': sub2_sls.name},
                'test.sub_wildcard_1': {'path': '', 'dest': sub_wildcard_1_sls.name},
            }[sls]

        client.get_state.side_effect = get_state


@skipIf(NO_MOCK, NO_MOCK_REASON)
@patch('salt.transport.Channel.factory', MagicMock())
class RemotePillarTestCase(TestCase):
    '''
    Tests for instantiating a RemotePillar in salt.pillar
    '''
    def setUp(self):
        self.grains = {}

    def tearDown(self):
        for attr in ('grains',):
            try:
                delattr(self, attr)
            except AttributeError:
                continue

    def test_get_opts_in_pillar_override_call(self):
        mock_get_extra_minion_data = MagicMock(return_value={})
        with patch(
            'salt.pillar.RemotePillarMixin.get_ext_pillar_extra_minion_data',
            mock_get_extra_minion_data):

            salt.pillar.RemotePillar({}, self.grains, 'mocked-minion', 'dev')
        mock_get_extra_minion_data.assert_called_once_with(
            {'saltenv': 'dev'})

    def test_multiple_keys_in_opts_added_to_pillar(self):
        opts = {
            'renderer': 'json',
            'path_to_add': 'fake_data',
            'path_to_add2': {'fake_data2': ['fake_data3', 'fake_data4']},
            'pass_to_ext_pillars': ['path_to_add', 'path_to_add2']
        }
        pillar = salt.pillar.RemotePillar(opts, self.grains,
                                          'mocked-minion', 'dev')
        self.assertEqual(pillar.extra_minion_data,
                         {'path_to_add': 'fake_data',
                          'path_to_add2': {'fake_data2': ['fake_data3',
                                                          'fake_data4']}})

    def test_subkey_in_opts_added_to_pillar(self):
        opts = {
            'renderer': 'json',
            'path_to_add': 'fake_data',
            'path_to_add2': {'fake_data5': 'fake_data6',
                             'fake_data2': ['fake_data3', 'fake_data4']},
            'pass_to_ext_pillars': ['path_to_add2:fake_data5']
        }
        pillar = salt.pillar.RemotePillar(opts, self.grains,
                                          'mocked-minion', 'dev')
        self.assertEqual(pillar.extra_minion_data,
                         {'path_to_add2': {'fake_data5': 'fake_data6'}})

    def test_non_existent_leaf_opt_in_add_to_pillar(self):
        opts = {
            'renderer': 'json',
            'path_to_add': 'fake_data',
            'path_to_add2': {'fake_data5': 'fake_data6',
                             'fake_data2': ['fake_data3', 'fake_data4']},
            'pass_to_ext_pillars': ['path_to_add2:fake_data_non_exist']
        }
        pillar = salt.pillar.RemotePillar(opts, self.grains,
                                          'mocked-minion', 'dev')
        self.assertEqual(pillar.pillar_override, {})

    def test_non_existent_intermediate_opt_in_add_to_pillar(self):
        opts = {
            'renderer': 'json',
            'path_to_add': 'fake_data',
            'path_to_add2': {'fake_data5': 'fake_data6',
                             'fake_data2': ['fake_data3', 'fake_data4']},
            'pass_to_ext_pillars': ['path_to_add_no_exist']
        }
        pillar = salt.pillar.RemotePillar(opts, self.grains,
                                          'mocked-minion', 'dev')
        self.assertEqual(pillar.pillar_override, {})

    def test_malformed_add_to_pillar(self):
        opts = {
            'renderer': 'json',
            'path_to_add': 'fake_data',
            'path_to_add2': {'fake_data5': 'fake_data6',
                             'fake_data2': ['fake_data3', 'fake_data4']},
            'pass_to_ext_pillars': MagicMock()
        }
        with self.assertRaises(salt.exceptions.SaltClientError) as excinfo:
            salt.pillar.RemotePillar(opts, self.grains, 'mocked-minion', 'dev')
        self.assertEqual(excinfo.exception.strerror,
                         '\'pass_to_ext_pillars\' config is malformed.')

    def test_pillar_send_extra_minion_data_from_config(self):
        opts = {
            'renderer': 'json',
            'pillarenv': 'fake_pillar_env',
            'path_to_add': 'fake_data',
            'path_to_add2': {'fake_data5': 'fake_data6',
                             'fake_data2': ['fake_data3', 'fake_data4']},
            'pass_to_ext_pillars': ['path_to_add']}
        mock_channel = MagicMock(
            crypted_transfer_decode_dictentry=MagicMock(return_value={}))
        with patch('salt.transport.Channel.factory',
                   MagicMock(return_value=mock_channel)):
            pillar = salt.pillar.RemotePillar(opts, self.grains,
                                              'mocked_minion', 'fake_env')

        ret = pillar.compile_pillar()
        self.assertEqual(pillar.channel, mock_channel)
        mock_channel.crypted_transfer_decode_dictentry.assert_called_once_with(
            {'cmd': '_pillar', 'ver': '2',
             'id': 'mocked_minion',
             'grains': {},
             'saltenv': 'fake_env',
             'pillarenv': 'fake_pillar_env',
             'pillar_override': {},
             'extra_minion_data': {'path_to_add': 'fake_data'}},
            dictkey='pillar')


@skipIf(NO_MOCK, NO_MOCK_REASON)
@patch('salt.transport.client.AsyncReqChannel.factory', MagicMock())
class AsyncRemotePillarTestCase(TestCase):
    '''
    Tests for instantiating a AsyncRemotePillar in salt.pillar
    '''
    def setUp(self):
        self.grains = {}

    def tearDown(self):
        for attr in ('grains',):
            try:
                delattr(self, attr)
            except AttributeError:
                continue

    def test_get_opts_in_pillar_override_call(self):
        mock_get_extra_minion_data = MagicMock(return_value={})
        with patch(
            'salt.pillar.RemotePillarMixin.get_ext_pillar_extra_minion_data',
            mock_get_extra_minion_data):

            salt.pillar.RemotePillar({}, self.grains, 'mocked-minion', 'dev')
        mock_get_extra_minion_data.assert_called_once_with(
            {'saltenv': 'dev'})

    def test_pillar_send_extra_minion_data_from_config(self):
        opts = {
            'renderer': 'json',
            'pillarenv': 'fake_pillar_env',
            'path_to_add': 'fake_data',
            'path_to_add2': {'fake_data5': 'fake_data6',
                             'fake_data2': ['fake_data3', 'fake_data4']},
            'pass_to_ext_pillars': ['path_to_add']}
        mock_channel = MagicMock(
            crypted_transfer_decode_dictentry=MagicMock(return_value={}))
        with patch('salt.transport.client.AsyncReqChannel.factory',
                   MagicMock(return_value=mock_channel)):
            pillar = salt.pillar.RemotePillar(opts, self.grains,
                                              'mocked_minion', 'fake_env')

        ret = pillar.compile_pillar()
        mock_channel.crypted_transfer_decode_dictentry.assert_called_once_with(
            {'cmd': '_pillar', 'ver': '2',
             'id': 'mocked_minion',
             'grains': {},
             'saltenv': 'fake_env',
             'pillarenv': 'fake_pillar_env',
             'pillar_override': {},
             'extra_minion_data': {'path_to_add': 'fake_data'}},
            dictkey='pillar')
