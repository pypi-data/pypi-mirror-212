# Pashword

> What does it mean?

The name "Pashword" comes from the contraction of "hash" and "password".

> What is it for?

Pashword is a Python package for password management.

> Is it hard to use?

Simply create a configuration file and execute one of the available commands.

## Background

Password management is a subject that we often prefer to ignore.
And for good reason, it's usually a headache.
Do you have to write everything down in a notebook that you risk losing or having stolen?
Should everything be stored in plain text?
Or encrypt it?
How to keep it all easy to use and portable from one machine to another?
The goal here is to settle all these issues once and for all by proposing, in open source, a very simple system based on a light and innovative mechanism.

## Features

With this Python package, your passwords become virtual.
They are not stored, neither in clear, nor in encrypted form.
They are generated from a configuration file, exist only in RAM for the period you want to view them, then disappear.
To make it work you only have to remember one secret key.
The main features offered by Pashword are identified by the following commands:

* `read`: To temporarily display the passwords generated from a configuration file.
* `sort`: To sort in alphabetical order the accounts contained in your configuration file.

## Installation

You can find how to install the package in the [installation section](https://dustils.gitlab.io/pashword/practice/installation/index.html) of the documentation.

## Usage

You can find how to use the package in the [examples section](https://dustils.gitlab.io/pashword/practice/examples/index.html) of the documentation.

## Credits

* Dunstan Becht

## License

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>.
