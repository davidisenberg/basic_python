

https://hevodata.com/learn/install-kafka-on-windows/
use 7zip to untar 

I installed here:
C:\Users\david\Kafka

followed most instructions

Problem:  need to install java
need server directory in java: https://stackoverflow.com/questions/18123144/missing-server-jvm-java-jre7-bin-server-jvm-dll

Problem:  need to increase JVM memory
https://java2blog.com/could-not-reserve-enough-space-for-object-heap/
_JAVA_OPTIONS
-Xmx1024M


C:\Users\david\Kafka\kafka_2.13-3.3.1\bin\windows\zookeeper-server-start.bat c:\Users\david\Kafka\kafka_2.13-3.3.1\config\zookeeper.properties
C:\Users\david\Kafka\kafka_2.13-3.3.1\bin\windows\kafka-server-start.bat c:\Users\david\kafka\kafka_2.13-3.3.1\config\server.properties

Problem: somehow the kafka-topics.bat file was 0KB!!!! Needed to reextract it

Problem: needed to replace with --bootstrap-server localhost:9092

create topic:
C:\Users\david\Kafka\kafka_2.13-3.3.1\bin\windows\kafka-topics.bat --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic TestTopic

list topic:
C:\Users\david\Kafka\kafka_2.13-3.3.1\bin\windows\kafka-topics.bat --list --bootstrap-server localhost:9092