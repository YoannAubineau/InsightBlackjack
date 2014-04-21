# InsightBlackjack

InsightBlackjack is a text-based blackjack game written in Python.

[![Build Status](https://travis-ci.org/yaubi/InsightBlackjack.svg?branch=master)](https://travis-ci.org/yaubi/InsightBlackjack)
[![Coverage Status](https://coveralls.io/repos/yaubi/InsightBlackjack/badge.png?branch=master)](https://coveralls.io/r/yaubi/InsightBlackjack?branch=master)

![Screenshot](https://raw.githubusercontent.com/yaubi/InsightBlackjack/master/screenshot.png)

## Installation

InsightBlackjack is written in Python. It has successfully been tested with
lastest versions of Python 3.4 and Python 3.3.

The source code is hosted on a public GitHub repository. In order to play this
game, you must first checkout the source code from GitHub and install all
package dependencies.

InsightBlackjack currently depends on one external Python package only:
[`termcolor`](https://pypi.python.org/pypi/termcolor/). As its name suggests,
this package is used for printing colored text on the terminal.

Here are the required commands you need to run in order to install
InsightBlackjack:

```sh
git clone https://github.com/yaubi/InsightBlackjack.git
cd InsightBlackjack
pip install -U -r requirements.txt
```

### Virtualenv

Be sure to activate the right virtualenv, if you use any, before installing
package dependencies. Alternatively, you can also create a brand new virtualenv
for the only purpose of testing this game.

If you choose to go without a virtualenv — which I don't recommand – you should
install packages dependencies system-wide, using the following command instead
of the previous one:

```sh
sudo pip install -U -r requirements.txt
```

## Usage

Once installed, the quickest way to enjoy the game is to run the following
command:

```sh
./blackjack.py Stuey
```

You can replace *Stuey* by your real name.

Stuey Ungar, also called *Stu, the Kid* because of his childish face, is
probably one of the greatest blackjack player of all time. If you want to know
more about him, read the dedicated [Wikipedia
page](http://en.wikipedia.org/wiki/Stu_Ungar). It is really stunning!

### Help

For more command-line options, let's have a look at the help page:
```sh
./blackjack.py --help

usage: blackjack.py [-h] [--ruleset {basic,european,american,insight}]
                    NAME [NAME ...]


Text-based blackjack card game.

positional arguments:
  NAME                  Give each players's name as arguments. There must be
                        at least 1 player. Maximum number of players depends
                        on choosen ruleset.

optional arguments:
  -h, --help            show this help message and exit
  --ruleset {basic,european,american,insight}
                        Use this option to select the ruleset to be used while
                        playing. Possible choices are "basic", "european",
                        "american" or "insight". If this option is not set, it
                        defaults to "insight."
```

### Select a ruleset

InsightBlackjack comes with 4 slightly differents rulesets:

* basic
* european
* american
* insight

**Basic** ruleset is single player only. It uses only one deck of 52 cards.
Minimum bet is 1 chip and Blackjack payout ratio is 2:1. It is the most simple
ruleset used by beginners.

**European** ruleset is multi-player with up to 7 concurrent players. It uses
5 decks of 52 cards. Minimum bet is 5 chips and Blackjack payout ratio is 3:2.
It is the most common ruleset you would encounter in casinos in Europe.

**American** ruleset is multi-player with up to 7 concurrent players. It uses
8 decks of 52 cards with an auto-shuffling shoe. Minimum bet is 2 chips and
Blackjack payout ratio is 3:2. It is the most common ruleset you would
encounter in casinos in the USA.

**Insight** ruleset is a custom ruleset specifically design for Insight Coding
Challenge. It plays with only one player, using 5 decks of 52 cards with an
auto-shuffling shoe. Minimum bet is 1 chip and Blackjack payout ratio is 3:2.

The default ruleset is **insight**. To choose a different ruleset, use the
`--ruleset` option. For example:

```sh
./blackjack.py --ruleset american Stuey
```

This command starts a new game with one player called *Stuey*, following
**american** ruleset.

In any case, each player starts with 100 chips and is allowed to play as long
as he owns enough chips to honnor the minimum bet.

### Multi-player game

In order for multiple players to play on the same table, each player's name has
to be given on the command line.

The maximum number of names that can be given at the same time depends on the
selected ruleset (see above for details). Note that, currently, only the
**european** and **american** rulesets allow multiple players to play on the
same table.

For example, if I want to play on the same table as Stuey, here is how I would
launch the game:

```sh
./blackjack.py --ruleset american Stuey Yoann
```

## Improvements

### Bugs

In the unlikely even you do encounter a bug, please report it promptly
by creating an new entry in the Github issue tracker for InsightBlackjack. Here
is the direct link:

https://github.com/yaubi/InsightBlackjack/issues/new

Be sure I will do my best to correct any bug you find as soon as possible. You
will also be notified when the bug you reported is fixed.

### Feature requests

If you feel a very important feature is missing, please consider it a bug and
report it as such by creating a new entry in the GitHub issue tracker for
InsightBlackjack, following this link:

https://github.com/yaubi/InsightBlackjack/issues/new

### Contributions

External contributions are most welcome! The prefered way of submitting a
contribution for reviewing is through GitHub pull-request mechanism. Please,
make sure all unit-tests pass before requesting a review of your branch.

Every single contribution will be reviewed, whithout exception. Don't take it
personnaly, however, if I ever ask you change some part of your code before I
can merge it into the main banch. That's exactly what pull-requests are for.

For some ideas on what to contribute to, please have a look at the currently
open issues, they crave for love:

https://github.com/yaubi/InsightBlackjack/issues

## Development

### Unit-tests

InsightBlackjack is currently covered by exactly 100 unit-tests. All those
tests can be run at once, in less that a second, with the following command:

```sh
python setup.py test
```

Alternatively, if you have [`nose`](https://nose.readthedocs.org) installed and
prefer to use it as your testing tool, you can run instead:

```sh
nosetests
```

In any case, make sure all tests pass. If a test fails, then it is a bug.  In
that case, please report the bug as described above.

### Continuous integration

Unit-tests are run automatically on any change made on master branch as well as
any other branches and pull-requests.

The following badges show the results of the last tests. The first badge tells
if all tests pass. It should be green and tell 'build: passing'. The second
badge indicates the amount of code covered by unit-tests. It should be as
close as possible to 100%.

[![Build Status](https://travis-ci.org/yaubi/InsightBlackjack.svg?branch=master)](https://travis-ci.org/yaubi/InsightBlackjack)
[![Coverage Status](https://coveralls.io/repos/yaubi/InsightBlackjack/badge.png?branch=master)](https://coveralls.io/r/yaubi/InsightBlackjack?branch=master)

Things seem to be going well so far. :)

### Source code architecture

Apart from `blackjack/test` sub-package where the unit-tests are to be found,
here is a commented list of all modules involved in InsightBlackjack. Their are
located in the root directory of the
[`blackjack`](https://github.com/yaubi/InsightBlackjack/blob/master/blackjack/)
package.

* [`card.py`](https://github.com/yaubi/InsightBlackjack/blob/master/blackjack/card.py): Card, Desk, Shoe and Hand object definitions.
* [`player.py`](https://github.com/yaubi/InsightBlackjack/blob/master/blackjack/player.py): Player, Dealer and Table object definitions.
* [`score.py`](https://github.com/yaubi/InsightBlackjack/blob/master/blackjack/score.py): Everything about counting points.
* [`game.py`](https://github.com/yaubi/InsightBlackjack/blob/master/blackjack/game.py): Rulesets and gameplay implementation.
* [`ui.py`](https://github.com/yaubi/InsightBlackjack/blob/master/blackjack/ui.py): Text-based user-interface.
* [`cli.py`](https://github.com/yaubi/InsightBlackjack/blob/master/blackjack/cli.py): Command-line interface for setting-up and starting a game.

I suggest you to read the code in that order so that you progressively build a
mental image of own things work together. The code is documented and should
also be self-explanatory. Better yet, commit history has been built as a kind
of source code discovery tour.

## Have fun!

In any case, I hope you guys will have great fun playing InsightBlackjack!
:smile:

