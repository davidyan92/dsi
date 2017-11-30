# ![](https://ga-dash.s3.amazonaws.com/production/assets/logo-9f88ae6c9c3871690e33280fcf557f33.png) Installing PostgreSQL

PostgreSQL is a database, similar to MySQL, that we'll be using in class. Install Postgres with the following steps:

Follow the instructions for your operating system below:

#### Mac Users

  * Download Postgres.app from [www.postgresapp.com](http://postgresapp.com)
  * Move the Postgres.app to your 'Applications' folder.
  * Open the Postgres.app (using "right-click + open" since it is an application that isn't from the Mac App Store)
  * Look for the elephant in the the menu bar.

#### Linux Users
  * [Download Postgres](http://www.postgresql.org/download/linux/ubuntu/)
  * On Ubuntu, you can also [install Postgres](https://help.ubuntu.com/community/PostgreSQL) from the package manager:

  ```bash
  $ sudo apt-get install postgresql postgresql-contrib postgresql-client
  ```

Test that this works by typing `psql`. You should be presented with the postgres shell. To exit type `\q`.

If this does not work, try the following:

```bash
$ cd ~
$ cd ../..
$ ls
```
At this point, you should see Applications, Library, Network, etc.
```bash
$ cd Library
$ cd PostgreSQL
$ cd 9.6
$ cd bin
```
If this runs without error and you find yourself in the `bin` folder, excellent.
```bash
$ cd ~
$ export PATH=/Library/PostgreSQL/9.6/bin:$PATH
$ psql -h dsi.c20gkj5cvu3l.us-east-1.rds.amazonaws.com -p 5432 -U dsi_student northwind
Password for user dsi_student: gastudents
```
