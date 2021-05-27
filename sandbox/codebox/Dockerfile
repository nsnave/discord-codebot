# Creates a base image containing all needed packages and libraries

FROM ubuntu

# Sets timezone
# From: https://askubuntu.com/a/1098881/1023149
ENV TZ=UTC
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update -y

# Installs python3 and supported libraries
RUN apt-get install -y python3
RUN apt-get install -y python3-pip
RUN pip3 install numpy
RUN pip3 install pandas
RUN pip3 install scikit-learn
RUN pip3 install qiskit

# Installs Node.js to run JavaScript
RUN apt-get install -y nodejs
RUN apt-get install -y npm

# Installs JDK to run Java
RUN apt-get install -y default-jdk

# Installs GCC and G++ to run C and C++
RUN apt-get install -y build-essential

# Installs GCC and G++ packages for cross-compilation to 32-bit architectures
RUN apt-get install -y gcc-multilib g++-multilib

# Installs SML/NJ and adds it to PATH
COPY ./lib/sml.tar.gz ./sml.tar.gz
RUN tar -xf sml.tar.gz
RUN rm ./sml.tar.gz
ENV PATH="/sml/bin:${PATH}"