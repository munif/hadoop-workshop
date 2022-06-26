# Instalasi Hadoop Standalone

Software yang diperlukan:
- VirtualBox <https://www.virtualbox.org/>
- Multipass <https://multipass.run/install>

    Multipass digunakan untuk mempercepat pembuatan _virtual machine_ berbasis Ubuntu.

- Terminal

Referensi:

1. [Install and Configure Apache Hadoop on Ubuntu 20.04](https://www.vultr.com/docs/install-and-configure-apache-hadoop-on-ubuntu-20-04/)

---
## Membuat Virtual Machine untuk Server

1. Jalankan terminal.
2. Buatlah sebuah virtual machine baru dengan perintah berikut.
    ```bash
    multipass launch focal -c 2 -d 10G -m 4G -n hadoop --network "Wi-Fi 2"
    ```
    Sesuaikan nama network dengan network yang ada. <br>
    Untuk mengecek nama network dapat menggunakan perintah ```multipass networks```.
3. Jika server sudah berhasil dibuat, masuklah ke dalam sistem dengan menggunakan ```multipass shell```.
    ```bash
    multipass shell hadoop
    ```
4. Lakukan update repository.
    ```
    $ sudo apt update
    ```
---
## Install Java
Install Java versi terbaru.
```
$ sudo apt install default-jdk default-jre -y
```

Verifikasi Java yang telah terinstal.
```
$ java -version
```
---
## Membuat User ```hadoop```

Tambahkan user baru ```hadoop```.
```
$ sudo adduser hadoop
```

Tambahkan ```hadoop``` ke dalam grup sudo.
```
$ sudo usermod -aG sudo hadoop
```

Login sebagai user ```hadoop```
```
$ sudo su - hadoop
```

Buat key pairs public dan private.
```
$ ssh-keygen -t rsa
```

Tambahkan public key yang dibuat dari ```id_rsa.pub``` ke ```authorized_keys```.
```
$ sudo cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
```

Ubah permission dari file ```authorized_keys```.
```
$ sudo chmod 640 ~/.ssh/authorized_keys
```

Verifikasi bahwa sekarang sudah bisa melakukan password-less SSH.
```
$ ssh localhost
```

---
## Install Apache Hadoop

Login dengan user ```hadoop``` (jika belum).
```
$ sudo su - hadoop
```

Download Hadoop versi stabil terbaru (Hadoop 3.3.3). Kunjungi situs [Apache Hadoop](https://downloads.apache.org/hadoop/common/stable/).
```
$ wget https://downloads.apache.org/hadoop/common/stable/hadoop-3.3.3.tar.gz
```

Ekstrak file yang telah didownload.
```
$ tar -xvzf hadoop-3.3.3.tar.gz
```

Pindahkan direktori hasil ekstraksi ke dalam direktori ```/usr/local```.
```
$ sudo mv hadoop-3.3.3 /usr/local/hadoop
```

Buatlah direktori untuk menyimpan log sistem.
```
$ sudo mkdir /usr/local/hadoop/logs
```

Ubah ownership dari direktori hadoop.
```
$ sudo chown -R hadoop:hadoop /usr/local/hadoop
```

---
## Konfigurasi Hadoop

Edit file ```~/.bashrc``` untuk mengonfigurasi Hadoop environment variables.
```
$ sudo nano ~/.bashrc
```

Tambahkan baris berikut di bagian paling bawah file. Simpan dan tutup filenya.
```
export HADOOP_HOME=/usr/local/hadoop
export HADOOP_INSTALL=$HADOOP_HOME
export HADOOP_MAPRED_HOME=$HADOOP_HOME
export HADOOP_COMMON_HOME=$HADOOP_HOME
export HADOOP_HDFS_HOME=$HADOOP_HOME
export YARN_HOME=$HADOOP_HOME
export HADOOP_COMMON_LIB_NATIVE_DIR=$HADOOP_HOME/lib/native
export PATH=$PATH:$HADOOP_HOME/sbin:$HADOOP_HOME/bin
export HADOOP_OPTS="-Djava.library.path=$HADOOP_HOME/lib/native"
```

Aktifkan environment variables.
```
$ source ~/.bashrc
```

---

## Konfigurasi Java Environment Variables

Temukan path Java.
```
$ which javac
```

Temukan direktori OpenJDK.
```
$ readlink -f /usr/bin/javac
```

Edit file ```hadoop-env.sh```.
```
$ sudo nano $HADOOP_HOME/etc/hadoop/hadoop-env.sh
```

Tambahkan baris berikut ke dalam file.
```
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
export HADOOP_CLASSPATH+=" $HADOOP_HOME/lib/*.jar"
```

Pindah ke dalam direktori ```lib```.
```
$ cd /usr/local/hadoop/lib
```

Download file Javax activation.
```
$ sudo wget https://jcenter.bintray.com/javax/activation/javax.activation-api/1.2.0/javax.activation-api-1.2.0.jar
```

Verifikasi versi Hadoop.
```
$ hadoop version
```

Edit file konfigurasi ```core-site.xml``` untuk menentukan URL NameNode.
```
$ sudo nano $HADOOP_HOME/etc/hadoop/core-site.xml
```

Tambahkan baris berikut. Simpan dan tutup file-nya.
```
<configuration>
   <property>
      <name>fs.default.name</name>
      <value>hdfs://0.0.0.0:9000</value>
      <description>The default file system URI</description>
   </property>
</configuration>
```

Buat direktori untuk menyimpan metadata node dan ubah ownershipnya ke user ```hadoop```.
```
$ sudo mkdir -p /home/hadoop/hdfs/{namenode,datanode}
$ sudo chown -R hadoop:hadoop /home/hadoop/hdfs
```

Edit file konfigurasi ```hdfs-site.xml``` untuk menentukan lokasi penyimpanan metadata node, dan file fs-image.
```
$ sudo nano $HADOOP_HOME/etc/hadoop/hdfs-site.xml
```

Tambahkan konfigurasi berikut. Simpan dan tutup file-nya.
```
<configuration>
   <property>
      <name>dfs.replication</name>
      <value>1</value>
   </property>

   <property>
      <name>dfs.name.dir</name>
      <value>file:///home/hadoop/hdfs/namenode</value>
   </property>

   <property>
      <name>dfs.data.dir</name>
      <value>file:///home/hadoop/hdfs/datanode</value>
   </property>
</configuration>
```

Edit file konfigurasi ```mapred-site.xml``` untuk menentukan konfigurasi MapReduce.
```
$ sudo nano $HADOOP_HOME/etc/hadoop/mapred-site.xml
```

Tambahkan baris berikut. Simpan dan tutup file-nya.
```
<configuration>
    <property>
      <name>mapreduce.framework.name</name>
      <value>yarn</value>
    </property>
    <property>
        <name>yarn.app.mapreduce.am.env</name>
        <value>HADOOP_MAPRED_HOME=$HADOOP_HOME</value>
    </property>
    <property>
        <name>mapreduce.map.env</name>
        <value>HADOOP_MAPRED_HOME=$HADOOP_HOME</value>
    </property>
    <property>
        <name>mapreduce.reduce.env</name>
        <value>HADOOP_MAPRED_HOME=$HADOOP_HOME</value>
    </property>
    <property>
        <name>mapreduce.application.classpath</name>
        <value>$HADOOP_MAPRED_HOME/share/hadoop/mapreduce/*:$HADOOP_MAPRED_HOME/share/hadoop/mapreduce/lib/*</value>
    </property>
</configuration>


```

Edit file konfigurasi ```yarn-site.xml``` untuk mendefinisikan setting berkaitan dengan YARN.
```
$ sudo nano $HADOOP_HOME/etc/hadoop/yarn-site.xml
```

Tambahkan baris kode berikut. Simpan dan tutup file-nya.
```
<configuration>
   <property>
      <name>yarn.nodemanager.aux-services</name>
      <value>mapreduce_shuffle</value>
   </property>
   <property>
        <name>yarn.nodemanager.env-whitelist</name>
        <value>JAVA_HOME,HADOOP_COMMON_HOME,HADOOP_HDFS_HOME,HADOOP_CONF_DIR,CLASSPATH_PREPEND_DISTCACHE,HADOOP_YARN_HOME,HADOOP_HOME,PATH,LANG,TZ,HADOOP_MAPRED_HOME</value>
    </property>
</configuration>
```

Validasi konfigurasi Hadoop dan format HDFS NameNode.
```
$ hdfs namenode -format
```

---
## Menjalankan Apache Hadoop Cluster

Start NameNode dan DataNode.
```
$ start-dfs.sh
```

Start YARN resource dan node managers.
```
$ start-yarn.sh
```

Verifikasi semua komponen berjalan dengan baik.
```
$ jps
```

Akses Apache Hadoop Web Interface menggunakan browser dengan alamat ```http://IP-server:9870```.<br>
Akses YARN Manager Web Interface pada alamat ```http://IP-server:8088```.

---
## Operasi Hadoop File System
Membuat folder baru.
```
$ hdfs dfs -mkdir /user
$ hdfs dfs -mkdir /user/hadoop
$ hdfs dfs -mkdir input
```

Mengupload file ke dalam Hadoop.
```
$ hdfs dfs -put $HADOOP_HOME/etc/hadoop/*.xml input
```

Menjalankan contoh script yang disediakan.
```
$ hadoop jar /usr/local/hadoop/share/hadoop/mapreduce/hadoop-mapreduce-examples-3.3.3.jar grep input output 'dfs[a-z.]+'
```

Meng-copy file dari Hadoop ke dalam folder lokal. Kemudian Melihat isi file hasil yang telah di-copy.
```
$ hdfs dfs -get output output
$ cat output/*
```

Melihat output di dalam HDFS.
```
$ hdfs dfs -cat output/*
```

Mematikan Hadoop.
```
$ stop-dfs.sh
$ stop-yarn.sh
```
