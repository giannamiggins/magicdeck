FROM centos:7
MAINTAINER Will Liu <will.liu@equinox.com>

WORKDIR /usr/local/magicdeck

# dependency install
    RUN yum -y install epel-release && \
    yum -y install python-pip && \
    yum -y install git && \
    yum -y install postgresql-devel && \
    yum -y install python-devel && \
    yum -y install gcc && \
    yum -y install libffi-devel && \
    yum -y install openssl-devel && \
    yum -y install libffi-devel openssl-devel

# Install aws-cli
    RUN pip install --upgrade pip && \
    pip install awscli

# build arguments
    ARG aws_access_key_id
    ARG aws_secret_access_key
    ARG git_username
    ARG git_password

# copy project
    ADD . /usr/local/magicdeck

# install requirements
    RUN echo https://$git_username:$git_password@bitbucket.org > /root/.git-credentials  && \
    git config --global credential.helper store
    RUN pip install -r /usr/local/magicdeck/requirements.txt  && \

# copy config file from s3
    mkdir /root/.aws/ && \
    echo [default] >> /root/.aws/credentials && \
    echo aws_access_key_id = $aws_access_key_id >> /root/.aws/credentials && \
    echo aws_secret_access_key = $aws_secret_access_key >> /root/.aws/credentials && \
    echo [default] >> /root/.aws/config && \
    echo region = us-east-1 >> /root/.aws/config && \
    aws s3 cp s3://eqxdl-prod-support/magicdeck/credentials.py /usr/local/magicdeck/credentials.py

# time zone setting
    RUN mv /etc/localtime /etc/localtime_UTC && \
    ln -s /usr/share/zoneinfo/America/New_York /etc/localtime

EXPOSE 5000

WORKDIR /usr/local/teletraan1
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--timeout", "120", "--workers", "2", "app:app"]
