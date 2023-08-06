#
# Copyright 2021 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Unit tests exercising `fhir_errors.py` functionality."""

from absl.testing import absltest
from google.fhir.core import fhir_errors


class ListErrorReporterTests(absltest.TestCase):
  """Makes assertions against `ListErrorReporter` behavior."""

  def setUp(self):
    super(ListErrorReporterTests, self).setUp()
    self.error_reporter = fhir_errors.ListErrorReporter()

  def testListErrorReporter_reportConversionError_succeeds(self):
    with self.assertLogs() as logs:
      self.error_reporter.report_conversion_error('some.element.path',
                                                  'Some error message.')
    self.assertLen(self.error_reporter.errors, 1)
    self.assertRegex(logs.output[0], r'some.element.path; Some error message.')

  def testListErrorReporter_reportValidationError_succeeds(self):
    with self.assertLogs() as logs:
      self.error_reporter.report_validation_error('some.element.path',
                                                  'Some error message.')
    self.assertLen(self.error_reporter.errors, 1)
    self.assertRegex(logs.output[0], r'some.element.path; Some error message.')

  def testListErrorReporter_reportValidationWarning_succeeds(self):
    with self.assertLogs() as logs:
      self.error_reporter.report_validation_warning('some.element.path',
                                                    'Some validation warning.')
    self.assertLen(self.error_reporter.warnings, 1)
    self.assertRegex(logs.output[0],
                     r'some.element.path; Some validation warning.')

  def testListErrorReporter_reportFhirPathError_succeeds(self):
    with self.assertLogs() as logs:
      self.error_reporter.report_fhir_path_error('some.element.path',
                                                 'foo.bar = bats',
                                                 'Some FHIRPath error.')
    self.assertLen(self.error_reporter.errors, 1)
    self.assertRegex(logs.output[0], r'foo.bar = bats; Some FHIRPath error.')

  def testListErrorReporter_reportFhirPathWarning_succeeds(self):
    with self.assertLogs() as logs:
      self.error_reporter.report_fhir_path_warning('some.element.path',
                                                   'foo.bar = bats',
                                                   'Some FHIRPath warning.')
    self.assertLen(self.error_reporter.warnings, 1)
    self.assertRegex(logs.output[0], r'foo.bar = bats; Some FHIRPath warning.')

  def testListErrorReporter_aggregateErrors_succeeds(self):

    # Add errors.
    self.error_reporter.report_fhir_path_error('some.element.path',
                                               'foo.bar = bats',
                                               'Some FHIRPath error.')
    self.error_reporter.report_fhir_path_error('some.element.path',
                                               'foo.bar = bats',
                                               'Some FHIRPath error.')
    self.error_reporter.report_fhir_path_error('other', 'other = bats',
                                               'Some other FHIRPath error.')

    # Add warning.
    self.error_reporter.report_fhir_path_warning('some.element.path',
                                                 'foo.bar = bats',
                                                 'Some FHIRPath warning.')
    self.error_reporter.report_fhir_path_warning('', 'foo.baz = buzz',
                                                 'Another FHIRPath warning.')

    self.assertEqual(
        fhir_errors.aggregate_events(self.error_reporter.errors),
        [(('FHIR Path Error: some.element.path; foo.bar = bats; Some FHIRPath '
           'error.'), 2),
         ('FHIR Path Error: other; other = bats; Some other FHIRPath error.', 1)
        ])

    self.assertEqual(
        fhir_errors.aggregate_events(self.error_reporter.warnings),
        [(('FHIR Path Warning: foo.baz = buzz; Another FHIRPath'
           ' warning.'), 1),
         (('FHIR Path Warning: some.element.path; foo.bar = bats; Some FHIRPath'
           ' warning.'), 1)])

  def testListErrorReporter_getErrorReport_succeeds(self):

    # Add errors.
    self.error_reporter.report_fhir_path_error('some.element.path',
                                               'foo.bar = bats',
                                               'Some FHIRPath error.')
    self.error_reporter.report_fhir_path_error('other', 'other = bats',
                                               'Some other FHIRPath error.')

    # Add warning.
    self.error_reporter.report_fhir_path_warning('some.element.path',
                                                 'foo.bar = bats',
                                                 'Some FHIRPath warning.')

    self.assertEqual(self.error_reporter.get_error_report(),
                     ("""Encountered 2 errors:
FHIR Path Error: other; other = bats; Some other FHIRPath error.        :   1
FHIR Path Error: some.element.path; foo.bar = bats; Some FHIRPath error.:   1

Encountered 1 warnings:
FHIR Path Warning: some.element.path; foo.bar = bats; Some FHIRPath warning.:   1\
"""))


if __name__ == '__main__':
  absltest.main()
