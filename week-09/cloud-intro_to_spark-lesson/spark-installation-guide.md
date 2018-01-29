# Spark Installation Guide

Spark is:

- Distributed computing
- A Framework
- Machine learning methods
- Stream processing

For our future lessons we will be exploring the applications of Apache Spark in the big data ecosystem.  


## OSX

For OSX, we will be using the "brew" version of Spark.

## 1.0 - Install Hadoop/Java via Brew

```
brew install hadoop
```
*Hadoop will be installed at path /usr/local/Cellar/hadoop*

> **If Brew complains about java not being installed**
> ```
> brew cask install java
> ```
> Then attempt to install the Hadoop package again

**If you get the "cask command not found".**
Follow these directions to fix your issue, then try again:
https://github.com/caskroom/homebrew-cask/blob/master/doc/reporting_bugs/error_unknown_command_cask.md

## Hadoop Configuration
### 2.1 - Configure Hadoop Environment Script

Edit the file: `nano /usr/local/Cellar/hadoop/2.7.3/libexec/etc/hadoop/hadoop-env.sh`

*Note the version installed, which may be newer than 2.7.3, and update your path accordingly*

Change the line with `HADOOP_OPTS` from:
```bash
export HADOOP_OPTS="$HADOOP_OPTS -Djava.net.preferIPv4Stack=true"
```

To:
```bash
export HADOOP_OPTS="$HADOOP_OPTS -Djava.net.preferIPv4Stack=true -Djava.security.krb5.realm= -Djava.security.krb5.kdc="
```

### 2.2 - Configure Hadoop filesystem core

Edit the core site configuration file like so:

```bash
nano /usr/local/Cellar/hadoop/2.7.3/libexec/etc/hadoop/core-site.xml
```

Add the following code between the `<configuration></configuration>` tags:

```xml
<property>
<name>hadoop.tmp.dir</name>
<value>/usr/local/Cellar/hadoop/hdfs/tmp</value>
<description>A base for other temporary directories.</description>
</property>
<property>
<name>fs.default.name</name>
<value>hdfs://localhost:9000</value>
</property>
```

These parameters setup the default HDFS storage directory (/usr/local/Cellar/hadoop/hdfs/tmp) and site service name (hdfs://localhost:9000).

### 2.3 - Configure Hadoop

Create a new file called **mapred-site.xml** here:
```bash
nano /usr/local/Cellar/hadoop/2.7.3/libexec/etc/hadoop/mapred-site.xml
```

Paste the following contents into this new file:

```bash
<configuration>
 <property>
  <name>mapred.job.tracker</name>
  <value>localhost:9010</value>
 </property>
</configuration>
```

This sets up the job tracker name which is used to observe jobs in progress.

### 2.4 - Configure Hadoop site HDFS

Edit the following:

```bash
nano /usr/local/Cellar/hadoop/2.7.3/libexec/etc/hadoop/hdfs-site.xml
```

Between `<configuration></configuration>` tags, add the following:

```bash
 <property>
  <name>dfs.replication</name>
  <value></value>
 </property>
```

*IE: the actual end of the file should look something like this after you've added your edits:*

```xml
<!-- Put site-specific property overrides in this file. -->

<configuration>
 <property>
  <name>dfs.replication</name>
  <value></value>
 </property>
</configuration>
```

### 2.5 - Configure Hadoop startup scripts

If you are using bash shell (which is default), you should add these lines to your bash profile file `~/.bash_profile`:

```bash
alias hstart="/usr/local/Cellar/hadoop/2.7.3/sbin/start-dfs.sh;/usr/local/Cellar/hadoop/2.7.3/sbin/start-yarn.sh"
alias hstop="/usr/local/Cellar/hadoop/2.7.3/sbin/stop-yarn.sh;/usr/local/Cellar/hadoop/2.7.3/sbin/stop-dfs.sh"
```

Then reload your bash profile by typing:

```bash
source ~/.bash_profile
```

### 2.6 - Format / Init Hadoop HDFS

If you setup everything correctly, this following command will format your default HDFS system:

```bash
hdfs namenode -format
```

Also, if you want to blow your HDFS system away and start fresh, you can always rerun this command.


### 2.7 - Check SSH key is setup

In order for your localhost to accept incoming connections through the HDFS service, we need to make sure SSH is setup with the proper keys.  These will likely be setup already.  You can check by typing:

`ssh-keygen -t rsa`

If the keygen script asks you to overwrite your existing keys, there's no need to overwrite your existing keys.  Abort the script by hitting **ctrl-c**.

*Note the prompt to "Overwrite (y/n)?". Hit ctrl-c in this case.  Else, just keep hitting enter, accepting all defaults *WITHOUT* typing any passwords.*
```
(auto) Davids-MacBook-Pro-3:random_forest_run davidyerrington$ ssh-keygen -t rsa
Generating public/private rsa key pair.
Enter file in which to save the key (/Users/davidyerrington/.ssh/id_rsa):
/Users/davidyerrington/.ssh/id_rsa already exists.
Overwrite (y/n)?
```

Also **Enable Remote Login:** “System Preferences” -> “Sharing”.
- Check “Remote Login”

![](https://snag.gy/w4QTKm.jpg)

**Authorize SSH Keys**
<br>
**ONLY DO THIS IF YOU DIDN'T HAVE THE id_rsa FILE IN THE PRIOR STEP**

To allow your system to accept login, we have to make it aware of the keys that will be used:
```cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys```

You should be able to login remotely.  Test this this by typing:

```
ssh localhost
```

### 2.8 - Start Hadoop

```
hstart
```

Once you start the HDFS daemon, you may get prompted multiple times for sudo access for the startup script.  Enter your user password to allow these operations.

Also, whenever you want to stop this service, you can type `hstop`.  This sometimes takes a little while but it will stop.  You may also be prompted for passwords.  This is ok.

### 2.9 - Get Some Coffee

Hadoop has an intense configuration prerequisite.  Congratulations you are done configuring Hadoop!  Take a break, or not.  It's a free country ;)

## ~~3.0 - Install Spark via Brew~~

```
~~brew install apache-spark~~
```

> installs Spark to directory /usr/local/Cellar/apache-spark/2.*

~~Add this to your ~/.bash_profile~~
```
alias jupyter-spark='PYSPARK_DRIVER_PYTHON=jupyter PYSPARK_DRIVER_PYTHON_OPTS="notebook" pyspark'
export SPARK_HOME='/usr/local/Cellar/apache-spark/2.0.0/libexec/'
```

~~Then reload your bash_profile:~~

```
source ~/.bash_profile
```

~~Then run jupyter notebook again using `jupyter-spark`, which is the alias you just created!  Check in a new notebook that the variable "sc" exists".~~

## 3.1 - Manually install Spark

*First: Actually read all of this first before you begin.  There are some important details and options available.*

> First and foremost, remove the brew version of Spark if you've installed it on OSX:

> `brew uninstall apache-spark`

To install / configure Apache Spark, we will do the following:

1. Navigate to the Apache Spark download page.
1. Download the latest version to `/usr/local/`
1. Unarchive Spark.
1. Set an environment variable called `SPARK_HOME` in your `.bash_profile` that other applications on your system will use to determine where Spark is installed.  We put it in `.bash_profile` because we want the environment variable to persist to every terminal session we use in the future.

### 1+2. Download the latest version of Spark.

Take note of the version that you download (use the pre-build for Hadoop version):
http://spark.apache.org/downloads.html

Download your version to your `/usr/local` directory.  You can click the download link and move the file or you can copy the download link, **or** use `wget` while you are in `/usr/local` from the terminal / bash to download the latest vesrion.

![](https://snag.gy/MAvKIH.jpg)
_The download link is listed here as #4_

*Alternatively, download with wget*
_The actual version and link may differ than what's listed in the example below so if the link is broken by the time you're reading this, go to the Apache Spark downloads page and get an updated link / version of Spark there._
```
cd /usr/local
wget http://d3kbcqa49mib13.cloudfront.net/spark-2.1.0-bin-hadoop2.7.tgz
```

### 3. Unarchive Apache Spark
The file you downloaded is compressed so you will need to unarchive and decompress it.  Use the following command, with respect to your file.  If the file / version has updated since the writing of this article, please adjust for your version.

```
tar -xzvf spark-2.1.0-bin-hadoop2.7.tgz # or the filename corresponding to the one you downloaded
```
_You should have this file in `/usr/local` if you followed step 1.  If not, return to the beginning and double check._

This command should expand Spark into `/usr/local/spark-2.1.0-bin-hadoop2.7`.  If you downloaded a newer version, then this directory will reflect the newer version.

To make our lives easier in the future, we are going to do what is called symbolically linking our Spark directory to one called just `/usr/local/spark`.  We want to do this because in the future we might want to download and install a newer version of Spark, or use different versions of Spark without having to refer to a complicated looking directory like `/usr/local/spark-2.1.0-bin-hadoop2.7`.  Instead, we can reference `/usr/local/spark`, and while it's symbolically linked to `/usr/local/spark-2.1.0-bin-hadoop2.7` or perhaps a future version like `/usr/local/spark-2.1.1345-bin-hadoop2.7`, we only need to update the symbolic link and we never have to update anything else that refers to `/usr/local/spark`.

*Symlink Spark*
Now we only need to refer to spark as `/usr/local/spark`.
`ln -s /usr/local/spark-2.1.0-bin-hadoop2.7 /usr/local/spark`

### 4. Configure environmental variable

Now that we have our symbolic link to `/usr/local/spark`, we need to set the `SPARK_HOME` environmental variable to point to that as well as add `/usr/local/spark/bin` to our system $PATH variable so we can type "pyspark" from anywhere and it will run.

**Edit your `~/.bash_profile`**

`nano ~/.bash_profile`

**Add these lines to the end of of your `.bash_profile`**

```
SPARK_HOME="/usr/local/spark"
PATH="/usr/local/spark/bin:$PATH"
```

**Update your environment with these settings**

```
source ~/.bash_profile
```
