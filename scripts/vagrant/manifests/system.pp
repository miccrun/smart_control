
class system {

    exec {
        "apt-update":
            command => "/usr/bin/apt-get update";
    }

    package {
        [
            "vim",
            "curl",
            "exuberant-ctags",
            "git-core",
            "build-essential",
            "python-pip",
            "python-dev"
        ]:
            ensure  => "present",
            require => Exec["apt-update"];
    }

    file {
        "/etc/profile.d/bash_profile.sh":
            ensure  => present,
            source => "/vagrant/files/bash_profile.sh";
    }

    file {
        "/etc/localtime":
            ensure  => present,
            source => "/usr/share/zoneinfo/America/Chicago"
    }

}
