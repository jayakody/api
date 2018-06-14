# Code.BigSwitch.com

Automation example repository for Big Switch

![Base template screenshot](https://www.bigswitch.com/sites/default/files/automationimage.jpeg)


## Features

* Getting started guides on how to setup Python/Ansible
* Python Code Examples
* Ansible Examples
* Advanced Use cases.

## Setup

1. Refer to ([Setup](https://jayakody.github.io/api/category/1-getting-started/)

## Develop

Develop with Python ([Pyhon](https://jayakody.github.io/api/category/2-python/)
Develop with Ansible ([Ansible](https://jayakody.github.io/api/big-ansible/)


~~~bash
$ bundle install
~~~

Run `jekyll` commands through Bundler to ensure you're using the right versions:

~~~bash
$ bundle exec jekyll serve
~~~

## Editing

Base is already optimised for adding, updating and removing tutorials, navigation, footer and FAQ information in CloudCannon.

The sticky sidebar in tutorials in populated by pulling out `<h2>` elements from the content.

### Posts

* Add, update or remove a post in the *Posts* collection.
* The tutorials page is organised by categories.
* Change the defaults when new posts are created in `_posts/_defaults.md`.

### Post Series
To create a new series:

* Add a new document to the `sets` collection.
* Set the `title` and `description`.

To add a tutorial/post to a series:
* Add a `set` field to the tutorial front matter which points to the file name of the desired set without the `.md` extention. e.g. If I have a set at `_sets/getting-started.md` I would use this in my tutorial front matter: `set: getting-started`.
* Add a `set_order` field to the tutorial front matter and specify a number. This is the tutorials order in the set.

### Navigation

* Exposed as a data file to give clients better access.
* Set in the *Data* / *Navigation* section.

### Footer

* Exposed as a data file to give clients better access.
* Set in the *Data* / *Footer* section.
