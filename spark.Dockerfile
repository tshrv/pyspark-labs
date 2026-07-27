FROM apache/spark:4.0.1

USER root
RUN pip install pandas==2.3.3 pyarrow==25.0.0 numpy==2.2.6

ARG HADOOP_AWS_VERSION=3.4.1
ARG AWS_SDK_VERSION=2.24.6

RUN curl -fsSL -o /opt/spark/jars/hadoop-aws-${HADOOP_AWS_VERSION}.jar \
      https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-aws/${HADOOP_AWS_VERSION}/hadoop-aws-${HADOOP_AWS_VERSION}.jar \
 && curl -fsSL -o /opt/spark/jars/bundle-${AWS_SDK_VERSION}.jar \
 https://repo1.maven.org/maven2/software/amazon/awssdk/bundle/${AWS_SDK_VERSION}/bundle-${AWS_SDK_VERSION}.jar
 
COPY spark-defaults.conf /opt/spark/conf/

RUN pip install pyspark==4.0.1 pandas==2.3.3 numpy==2.2.6 faker==40.36.0

USER spark