# Instalasi Hadoop Cluster

Referensi:
1. [Apache Hadoop Installation on Ubuntu](https://sparkbyexamples.com/hadoop/apache-hadoop-installation/)

---

## Membuat Server Hadoop

Buatlah tiga buah server baru dengan nama ```namenode```, ```datanode1```, ```datanode2```.
```
multipass launch focal -c 2 -d 10G -m 4G -n namenode --network "Wi-Fi 2"
multipass launch focal -c 2 -d 10G -m 4G -n datanode1 --network "Wi-Fi 2"
multipass launch focal -c 2 -d 10G -m 4G -n datanode2 --network "Wi-Fi 2"
```

---

## Melakukan Instalasi Hadoop pada ```namenode```

Lakukan instalasi Hadoop pada server namenode dan datanode sampai dengan verifikasi versi Hadoop.

Copy-kan isi file ```authorized_keys``` dari ```namenode``` ke dalam kedua server datanode.

```
namenode:$ cat .ssh/authorized_keys
datanode1:$ sudo nano .ssh/authorized_keys
datanode2:$ sudo nano .ssh/authorized_keys
```

Tes login dari namenode ke datanode menggunakan perintah berikut.
```
namenode:$ ssh hadoop@IP-datanode1
namenode:$ ssh hadoop@IP-datanode2
```

---

## Mengedit File Konfigurasi

Edit file ```core-site.xml``` seperti berikut.
```
<configuration>
    <property>
        <name>fs.default.name</name>
        <value>hdfs://<IP-Namenode>:9000</value>
    </property>
</configuration>
```

Edit file ```hdfs-site.xml``` seperti berikut.
```

<configuration>
    <property>
        <name>dfs.replication</name>
        <value>3</value>
    </property>
    <property>
        <name>dfs.namenode.name.dir</name>
        <value>file:///usr/local/hadoop/hdfs/data</value>
    </property>
    <property>
        <name>dfs.datanode.data.dir</name>
        <value>file:///usr/local/hadoop/hdfs/data</value>
    </property>
</configuration>
```

Edit file ```yarn-site.xml``` seperti berikut.
```
<configuration>
    <property>
        <name>yarn.nodemanager.aux-services</name>
        <value>mapreduce_shuffle</value>
    </property>
    <property>
        <name>yarn.nodemanager.aux-services.mapreduce.shuffle.class</name>
        <value>org.apache.hadoop.mapred.ShuffleHandler</value>
    </property>
    <property>
       <name>yarn.resourcemanager.hostname</name>
       <value>192.168.0.175</value>
    </property>
</configuration>
```

Edit file ```mapred-site.xml``` seperti berikut.
```
<configuration>
    <property>
        <name>mapreduce.jobtracker.address</name>
        <value>192.168.0.175:54311</value>
    </property>
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

Buat data folder dengan menggunakan perintah berikut di semua server.
```
sudo mkdir -p /usr/local/hadoop/hdfs/data
sudo chown hadoop:hadoop -R /usr/local/hadoop/hdfs/data
chmod 700 /usr/local/hadoop/hdfs/data
```

---

## Menambahkan Master dan Worker

Buka file ```/usr/local/hadoop/etc/hadoop/masters``` dan tambahkan IP dari namenode.

Buka file ```/usr/local/hadoop/etc/hadoop/workers``` dan tambahkan IP dari semua datanode.

---

## Menjalankan Hadoop Cluster

Format namenode
```
namenode:$ hdfs namenode -format
```

Menjalankan Hadoop Cluster
```
start-dfs.sh
```

Mematikan Hadoop Cluster
```
stop-dfs.sh
```