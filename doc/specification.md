Ansible&reg; Role Templates Testing Specification
=================================================

Version 0.1

Introduction
------------

[Ansible&reg;][Ansible] is a tool for automation of software deployment and
configuration management. Ansible uses [Jinja][Jinja] templates to manage
configuration files. Development of complex templates requires testing tools.

The more variables are used to parametrise a template, the more test cases
should be run to order to check template rendering for all the practical
combinations of inputs (the variable values). Therefore, the feature of
template tests is a significant number of test cases.

While some tools for testing Ansible roles are available, they are not suitable
for running a big number test cases. For example [Molecule][Molecule] framework
creates and provisions a new container or virtual machine before each test
scenario. This test setup process is too slow and CPU/memory consuming to run
many short and simple template tests.

This document defines a specification for testing Ansible templates. The testing
approach, that lacks the above limitations of the existing tools, is described.
The specification of test definitions is provided in order to facilitate the
development of interoperable test runners that implement the described apporach.

[Ansible]: https://github.com/ansible/ansible
[Jinja]: https://jinja.palletsprojects.com/
[Molecule]: https://github.com/ansible-community/molecule

Test Runner Operation
---------------------

This specfication assumes that the tested templates are located in the
`templates/` subdirectory of an Ansible role directory.

A new subdirectory named `templates_tests/` is added to the role directory. This
directory contains definitions of Ansible role template tests. Each test
definition specifies:

- a role template to be tested
- a set of template rendering inputs (variable values)
- an expected result of template rendering

A test runner performs the following actions:

1. discovers test definitions located in `templates_tests/` directory
2. instantiates test cases from the discovered test definitions
3. runs the instantiated test suite
4. provdes the outcome to the user

For each test case in the suite the runner:

1. renders the tested template with the variable values from the test definition
2. compares the rendering result with the expected result

This approach doesn't have a complex test environment setup/provisioning phase
(comparing to Molecule framework). All test cases are independent and may be
executed in parallel.

Test Definitions Format
-----------------------

Test definitions are stored in `templates_tests/` subdirectory of a role
directory.

The `templates_tests/` directory must contain `meta.yml` file. This file is a
YAML document with a single `version` attribute. This attribue specifies a
version of the specification. The version of the current specification is 0.1.

In order to facilitate an automated test discovery, test definition file names
have to match a common pattern. This specification defines it as `test*.yml`
glob. Therefore, test discovery may be implemented as a recursive search in the
`templates_tests/` directory of all files, whose name matches the specified
pattern.

Test definition file is a YAML document with a single attribute named `tests`,
that specifies a test suite. The test suite is specified as a list of test
definitions. Each test definition has the following attributes.

`name` gives a short description of the test.

`template` specifies a path to the tested template. The path must be specified
relative to `templates/` role directory.

`variables` is an optional dictionary with the following optional attributes:

- `inventory` -- path to file with variables, that mocks Ansible inventory
  variables
- `extra` -- path to file with variables, that mocks Ansible extra vars

Paths to files with variables must be relative to the parent directory of the
test definition file. These files contain YAML documents with format similar to
role defaults and vars (defined in `role/defaults/main.yml` and
`role/vars/main.yml` role files accordingly).

A test runner merges template variables according to their precedence. Variables
with greater precedence override variables with lower precedence. Here is the
order of precedence from the least to the greatest:

1. role defaults (defined in `role/defaults/main.yml`)
2. variables defined in a file referenced by the `inventory` attribute
3. role vars (defined in `role/vars/main.yml`)
4. variables defined in a file referenced by the `extra` attribute

`expected_result` specifies a path to the expected result of template
rendering. The path must be specified relative to the parent directory of the
test definition file.

Example
-------

An example role directory structure is provided bellow. The role directories
that are ignored by test runners (for example, `tasks/`) are omitted in sake of
simplicity.

```
defaults/
    main.yml
vars/
    main.yml
templates/
    index.html.j2
    home.html.j2
templates_tests/
    meta.yml
    test.yml
    inventory.yml
    extra.yml
    index.html
    foo/
        test-suite.yml
        default/
            home.html
        custom/
            inventory.yml
            home.html
```

The `templates_tests/meta.yml` file content:

```yaml
---
version: "0.1"
```

The `templates_tests/test.yml` file content:

```yaml
---
tests:
  - name: test index page rendering
    template: index.html.j2
    variables:
      inventory: inventory.yml
      extra: extra.yml
    expected_result: index.html
```

This test definition states that the result of `templates/index.html.j2`
template rendering with variables found in the following files:

- `defaults/main.yml`
- `templates_tests/inventory.yml`
- `vars/main.yml`
- `templates_tests/extra.yml`

must match the content of the `templates_tests/index.html` file.

The `templates_tests/foo/test-suite.yml` content:

```yaml
---
tests:
  - name: test default home page rendering
    template: home.html.j2
    expected_result: default/home.html

  - name: test customized home page rendering
    template: home.html.j2
    variables:
      inventory: custom/inventory.yml
    expected_result: custom/home.html
```

This file contains two test definitions. The former states that the result of
rendering `templates/home.html.j2` template with variables found in the
following files:

- `defaults/main.yml`
- `vars/main.yml`

must match the content of the `templates_tests/foo/default/home.html` file.

The latter states that the result of rendering `templates/home.html.j2` template
with variables found in the following files:

- `defaults/main.yml`
- `templates_tests/foo/custom/inventory.yml`
- `vars/main.yml`

must match the content of the `templates_tests/foo/custom/home.html` file.

Copyright Statement
-------------------

Copyright (c) 2021 Alexey Busygin

This work is licensed under the Creative Commons Attribution-ShareAlike 4.0
International License. To view a copy of this license, visit
http://creativecommons.org/licenses/by-sa/4.0/ or send a letter to Creative
Commons, PO Box 1866, Mountain View, CA 94042, USA.

Ansible is a registered trademark of Red Hat, Inc. in the United States and
other countries.
