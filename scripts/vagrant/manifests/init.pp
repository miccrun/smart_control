
import 'system.pp'

node default {

    include system

    class { 'mysql::bindings':
        python_enable => 1
    }
    class { 'mysql::server':
        root_password => 'root_password'
    }

    mysql::db {
        'db':
            user     => 'db_user',
            password => 'db_pwd',
            host     => 'localhost',
            grant    => ['ALL'];
    }

    package { "nginx":
        ensure => installed,
        require => Exec["apt-update"]
    }

    service { "nginx":
        require => Package["nginx"],
        ensure => running,
        enable => true;
    }

    file { "/etc/nginx/sites-available/default":
        require => Package["nginx"],
        ensure  => present,
        source  => "/vagrant/files/nginx.conf",
        notify  => Service["nginx"];
    }

    file { "/etc/nginx/sites-enabled/default":
        require => File["/etc/nginx/sites-available/default"],
        ensure => "link",
        target => "/etc/nginx/sites-available/default",
        notify => Service["nginx"];
    }

    exec {
        "pip-install":
            command => "/usr/bin/pip install -r /vagrant/requirements.txt",
            require => Package[python-pip, python-mysqldb, python-dev];
    }

    package { "supervisor":
        ensure => installed,
        require => Exec["apt-update", "pip-install"]
    }

    service { "supervisor":
        require => Package["supervisor"],
        ensure => running,
        enable => true;
    }

    file { "/etc/supervisor/conf.d/django.conf":
        require => Package["supervisor"],
        ensure  => present,
        source  => "/vagrant/files/django_supervisor.conf",
        notify  => Service["supervisor"];
    }

}
