#!/bin/sh

# Run the (modified) CLIFF-up bootstrap.sh
apt-get update
echo "Installing basic packages..."
apt-get install git <<-EOF
yes
EOF
apt-get install curl <<-EOF
yes
EOF
apt-get install vim <<-EOF
yes
EOF
apt-get install unzip htop <<-EOF
yes
EOF
echo "Installing Java and JDK"
apt-get install openjdk-7-jre <<-EOF
yes
EOF
apt-get install openjdk-7-jdk <<-EOF
yes
EOF
apt-get install wget <<-EOF
yes
EOF

echo "Configuring Java and things"

set JRE_HOME=/usr/lib/jvm/java-7-openjdk-amd64

#cd /root
#wget https://raw.githubusercontent.com/ahalterman/CLIFF-up/master/bashrc
#rm .bashrc
#mv bashrc .bashrc
#source .bashrc
## SKIP ALL THAT AND JUST EXPORT CATALINA_HOME
export CATALINA_HOME=/root/apache-tomcat-7.0.59

cd /usr/lib/jvm/ 
chmod 777 /usr/lib/jvm/java-7-openjdk-amd64

cd /usr/lib/jvm/java-7-openjdk-amd64
chmod 777 -R *

echo "Install Maven"
# Why does stupid Maven install Java 6?
apt-get install maven <<-EOF
yes
EOF

# tell it again that we do indeed want Java 7
set JRE_HOME=/usr/lib/jvm/java-7-openjdk-amd64

update-alternatives --config java  <<-EOF
2
EOF

echo "Download Tomcat"
cd /root
wget
http://archive.apache.org/dist/tomcat/tomcat-7/v7.0.59/bin/apache-tomcat-7.0.59.tar.gz
tar -xvzf apache-tomcat-7.0.59.tar.gz
# rm apache-tomcat-7.0.59.tar.gz

# get tomcat users set up correctly
cd /root/apache-tomcat-7.0.59/conf
rm tomcat-users.xml
wget
https://raw.githubusercontent.com/ahalterman/CLIFF-up/master/tomcat-users.xml

echo "Boot Tomcat"
$CATALINA_HOME/bin/startup.sh

echo "Downloading CLAVIN..."
cd /root
git clone https://github.com/Berico-Technologies/CLAVIN.git
cd CLAVIN
echo "Downloading placenames file from Geonames..."
wget http://download.geonames.org/export/dump/allCountries.zip
unzip allCountries.zip
rm allCountries.zip

echo "Compiling CLAVIN"
mvn compile

echo "Building Lucene index of placenames--this is the slow one"
MAVEN_OPTS="-Xmx8g" mvn exec:java
-Dexec.mainClass="com.bericotech.clavin.index.IndexDirectoryBuilder"

mkdir /etc/cliff2
ln -s /root/CLAVIN/IndexDirectory /etc/cliff2/IndexDirectory

cd /root
cd .m2
rm settings.xml
wget https://raw.githubusercontent.com/ahalterman/CLIFF-up/master/settings.xml

echo "Download CLIFF"
cd /root
# most recent is different and breaks stuff
#git clone https://github.com/c4fcm/CLIFF
# Do this instead:
wget https://github.com/c4fcm/CLIFF/archive/v2.0.0.tar.gz
tar -xvzf v2.0.0.tar.gz
mv CLIFF-2.0.0/ CLIFF
cd CLIFF
rm pom.xml 
wget https://raw.githubusercontent.com/ahalterman/CLIFF-up/master/pom.xml
# mv /home/root/CLIFF-up/pom.xml /home/root/CLIFF

mvn tomcat7:deploy -DskipTests

echo "Move files around and redeploy"
mv /root/CLIFF/target/CLIFF-2.0.0.war /root/apache-tomcat-7.0.59/webapps/
/root/apache-tomcat-7.0.59/bin/shutdown.sh
/root/apache-tomcat-7.0.59/bin/startup.sh
echo "Installation Complete"
echo "If you need to manually start the Tomcat server type 'sudo /home/root/apache-tomcat-7.0.59/bin/startup.sh' to start the server"
