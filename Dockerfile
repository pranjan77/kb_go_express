FROM kbase/kbase:sdkbase.latest
MAINTAINER KBase Developer
# -----------------------------------------
# In this section, you can install any system dependencies required
# to run your App.  For instance, you could place an apt-get update or
# install line here, a git checkout to download code, or run any other
# installation scripts.



# RUN apt-get update

# Here we install a python coverage tool and an
# https library that is out of date in the base image.

RUN pip install coverage

# update security libraries in the base image
RUN pip install cffi --upgrade \
    && pip install pyopenssl --upgrade \
    && pip install ndg-httpsclient --upgrade \
    && pip install pyasn1 --upgrade \
    && pip install requests --upgrade \
    && pip install 'requests[security]' --upgrade



RUN mkdir /kb/deployment/bin/rlibs

#RUN sudo apt-get remove r-base && \
#	sudo apt-get remove r-base-devel && \
#	sudo apt-get remove r-base-core && \
#	sudo apt-get clean && \
#	sudo apt-get autoclean && \
#	sudo apt-get install r-base=3.0.2-1precise0



RUN CODENAME=`grep CODENAME /etc/lsb-release | cut -c 18-` && \
    echo "deb http://cran.rstudio.com/bin/linux/ubuntu $CODENAME/" >> /etc/apt/sources.list && \
    sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys E084DAB9 && \
    sudo apt-get update && \
    yes '' | sudo apt-get -y install r-base && \
	 echo 'install.packages(c("devtools", "optparse", "gplots"), lib="/kb/deployment/lib", repos="http://cran.rstudio.com")\n \
	 .libPaths( c( .libPaths(), "/kb/deployment/lib") ) \n \
	 library(devtools) \n \
	 install_github("kevinrue/GOexpress")\n' > /kb/deployment/bin/rlibs/packages.R && \
	Rscript /kb/deployment/bin/rlibs/packages.R


#RUN wget https://cran.r-project.org/src/base/R-3/R-3.4.1.tar.gz && \
#    tar -zxf R-3.4.1.tar.gz && cd R-3.4.1 && \
#    ./configure --with-libpng --with-jpeglib --with-x=no && \
#    make && make pdf && make info && make install && make install-info && make install-pdf &&\
#    echo 'install.packages(c("gplots", "optparse", ""), lib="/kb/deployment/lib", repos="http://cran.rstudio.com", dependencies=TRUE)\nsource("http://bioconductor.org/biocLite.R")\nbiocLite(c("GOexpress", "Biobase"), dependencies = TRUE)' > /kb/deployment/bin/rlibs/packages.R && \
#	Rscript /kb/deployment/bin/rlibs/packages.R




# -----------------------------------------

COPY ./ /kb/module
RUN mkdir -p /kb/module/work
RUN chmod -R a+rw /kb/module

WORKDIR /kb/module

RUN make all

ENTRYPOINT [ "./scripts/entrypoint.sh" ]

CMD [ ]
