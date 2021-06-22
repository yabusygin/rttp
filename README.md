templtest
=========

[Ansible&reg;][Ansible] is a tool for automation of software deployment and
configuration management. Ansible uses [Jinja][Jinja] templates to manage
configuration files. Development of complex templates requires testing tools.

`templtest` is a tool for testing templates used by Ansible roles. Put your
tests in role's `templates_tests/` directory according to the
[specification][Spec] and run:

```sh
cd $ROLE_PATH
templtest
```

See [Ansible Role Templates Testing Specification][Spec] for details.

[Ansible]: https://github.com/ansible/ansible
[Jinja]: https://jinja.palletsprojects.com/
[Spec]: doc/specification.md

Ansible is a registered trademark of Red Hat, Inc. in the United States and
other countries.
