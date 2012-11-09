class casperjs {
    exec { "install_casperjs":
        command => 'cd /home/vagrant/ && git clone git://github.com/n1k0/casperjs.git && cd /home/vagrant/casperjs && git checkout tags/1.0.0-RC4 && sudo ln -sf `pwd`/bin/casperjs /usr/local/bin/casperjs',
        path => '/usr/local/bin:/usr/bin:/bin',
        unless => 'test -x /usr/local/bin/casperjs',
        require => [Package['git-core'],],
        user => "vagrant",
        provider => "shell"
    }
}
