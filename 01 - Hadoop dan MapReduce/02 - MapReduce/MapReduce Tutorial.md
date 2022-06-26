# MapReduce Tutorial

Referensi:
1. [MapReduce Tutorial](https://hadoop.apache.org/docs/stable/hadoop-mapreduce-client/hadoop-mapreduce-client-core/MapReduceTutorial.html)

---

## Mengedit Environment Variables

Tambahkan environment variables berikut ke dalam file ```~/.bashrc```.
```
$ sudo nano .bashrc
```

```
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
export PATH=${JAVA_HOME}/bin:${PATH}
export HADOOP_CLASSPATH=${JAVA_HOME}/lib/tools.jar
```

Reload environment variable.
```
$ source .bashrc
```

---

## Menyiapkan Kode Program Java

Download file ```WordCount.java```.

Letakkan ke dalam virtual machine **menggunakan Windows Terminal** dengan menggunakan perintah berikut.
```
$ multipass transfer WordCount.java hadoop:/home/ubuntu/WordCount.java
```

Copy file ```WordCount.java``` dari folder ```/home/ubuntu/``` ke dalam folder ```/home/hadoop```.
```
$ cp /home/ubuntu/WordCount.java .
```

Lakukan kompilasi dan build file ```.jar```.
```
$ hadoop com.sun.tools.javac.Main WordCount.java
$ jar cf wc.jar WordCount*.class
```

---

## Menyiapkan File Input

Buat file ```file01```.
```
$ nano file01
```

Isi dengan konten sebagai berikut.
```
Hello World Bye World
```

Buat file ```file02```.
```
$ nano file02
```

Isi dengan konten sebagai berikut.
```
Hello Hadoop Goodbye Hadoop
```

Buat folder di HDFS.
```
$ hdfs dfs -mkdir /user/hadoop/wordcount
$ hdfs dfs -mkdir /user/hadoop/wordcount/input
```

Upload file ke dalam HDFS.
```
$ hdfs dfs -put file* /user/hadoop/wordcount/input
```

---

## Menjalankan Aplikasi

Jalankan aplikasi menggunakan perintah berikut.
```
$ hadoop jar wc.jar WordCount /user/hadoop/wordcount/input /user/hadoop/wordcount/output
```

Cek output yang dihasilkan.
```
$ hadoop fs -cat /user/hadoop/wordcount/output/*
```