
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

    class { 'python':
        version    => 'system',
        dev        => true,
        pip        => true,
        virtualenv => true,
    }

    python::virtualenv { '/var/www/smartcontrol/env':
        ensure       => present,
        version      => 'system',
        requirements => '/vagrant/requirements.txt',
        distribute   => true,
        owner        => 'vagrant',
        group        => 'vagrant',
        cwd          => '/var/www/smartcontrol',
        timeout      => 0,
    }

    python::requirements { '/vagrant/requirements.txt':
      virtualenv => '/var/www/smartcontrol/env',
      owner      => 'vagrant',
      group      => 'vagrant',
    }

    service { "supervisor":
        require => Package["supervisor"],
        ensure => running,
        enable => true;
    }

    file { "/etc/supervisor/conf.d/smartcontrol.conf":
        require => Package["supervisor"],
        ensure  => present,
        source  => "/vagrant/files/smartcontrol.conf",
        notify  => Service["supervisor"];
    }

}
