import threading
from absl.testing import absltest
from cloud_tpu_diagnostics.src.config import debug_configuration
from cloud_tpu_diagnostics.src.config import stack_trace_configuration
from cloud_tpu_diagnostics.src.debug import start_debugging


class DebugTest(absltest.TestCase):

  def testDaemonThreadRunningWhenCollectStackTraceTrue(self):
    debug_config = debug_configuration.DebugConfig(
        stack_trace_config=stack_trace_configuration.StackTraceConfig(
            collect_stack_trace=True,
            stack_trace_to_cloud=False,
        ),
    )
    start_debugging(debug_config)
    self.assertEqual(threading.active_count(), 2)
    daemon_thread_list = list(
        filter(lambda thread: thread.daemon is True, threading.enumerate())
    )
    self.assertLen(daemon_thread_list, 1)

  def testDaemonThreadNotRunningWhenCollectStackTraceFalse(self):
    debug_config = debug_configuration.DebugConfig(
        stack_trace_config=stack_trace_configuration.StackTraceConfig(
            collect_stack_trace=False,
            stack_trace_to_cloud=False,
        ),
    )
    start_debugging(debug_config)
    self.assertEqual(threading.active_count(), 1)
    daemon_thread_list = list(
        filter(lambda thread: thread.daemon is True, threading.enumerate())
    )
    self.assertLen(daemon_thread_list, 0)


if __name__ == '__main__':
  absltest.main()
