# Phase 3 CLI Project Template

## Learning Goals

- Discuss the basic directory structure of a CLI.
- Outline the first steps in building a CLI.

***

## Introduction

You now have a basic idea of what constitutes a CLI, but you (understandably!)
likely don't have the best idea of where to start. Fork and clone this lesson
for a template for your CLI. Take a look at the directory structure before we
begin:

```console
.
├── Pipfile
├── Pipfile.lock
├── README.md
└── lib
    ├── cli.py
    ├── db
    │   ├── models.py
    │   └── seed.py
    ├── debug.py
    └── helpers.py
```

> **Note: You may already know some or all of the material covered in this
> lesson. We hope that having it all in one place will help you in designing
> and developing your project, regardless of where you're starting off.**

***

## Where Do I Start?

This project will likely be one of the biggest projects you've undertaken so
far. Your first task should be creating a Git repository to keep track of your
work and roll back any undesired changes.

### Removing Existing Git Configuration

If you're using this template, start off by removing the existing metadata for
Github and Canvas. Run the following command to carry this out:

```console
$ rm -rf .git .github .canvas
```

The `rm` command removes files from your computer's memory. The `-r` flag tells
the console to remove _recursively_, which allows the command to remove
directories and the files within them. `-f` removes them permanently.

`.git` contains this directory's configuration to track changes and push to
Github (you want to track and push _your own_ changes instead), and `.github`
and `.canvas` contain the metadata to create a Canvas page from your Git repo.
You don't have the permissions to edit our Canvas course, so it's not worth
keeping them around.

### Creating Your Own Git Repo

First things first- rename this directory! Once you have an idea for a name,
move one level up with `cd ..` and run `mv python-p3-cli-project-template
<new-directory-name>` to change its name.

> **Note: `mv` actually stands for "move", but your computer interprets this
> rename as a move from a directory with the old name to a directory with
> a new name.**

`cd` back into your new directory and run `git init` to create a local git
repository. Add all of your local files to version control with `git add --all`,
then commit them with `git commit -m'initial commit'`. (You can change the
message here- this one is just a common choice.)

Navigate to [GitHub](https://github.com). In the upper-right corner of the page,
click on the "+" dropdown menu, then select "New repository". Enter the name of
your local repo, choose whether you would like it to be public or private, make
sure "Initialize this repository with a README" is unchecked (you already have
one), then click "Create repository".

Head back to the command line and enter `git remote add <project name> <github
url>`. This will map the remote repository to your local repository. Finally,
push your first commit with `git push -u origin main`.

Your project is now version-controlled locally and online. This will allow you
to create different versions of your project and pick up your work on a
different machine if the need arises.

***

## Generating Your Pipenv

You might have noticed in the file structure- there's already a Pipfile! That
being said, we haven't put much in there- just Python version 3.8 and ipdb.

Install any dependencies you know you'll need for your project, like SQLAlchemy
and Alembic, before you begin. You can do this straight from the command line:

```console
$ pipenv install sqlalchemy alembic
```

From here, you should run your second commit:

```console
$ git add Pipfile Pipfile.lock
$ git commit -m'add sqlalchemy and alembic to pipenv'
$ git push
```

Now that your environment is set up, run `pipenv shell` to enter it.

***




