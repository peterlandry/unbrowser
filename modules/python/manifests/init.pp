class python {
    package {
        "build-essential": ensure => latest;
        "python": ensure => latest;
        "python-dev": ensure => latest;
        "python-setuptools": ensure => installed;
    }

    exec { "install_pip":
        command => "easy_install pip",
        path => "/usr/local/bin:/usr/bin:/bin",
        refreshonly => true,
        require => Package["python-setuptools"],
        subscribe => Package["python-setuptools"],
    }
}
