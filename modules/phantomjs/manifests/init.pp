class phantomjs {
    package {
        'libqt4-dev': ensure => latest;
        'qt4-qmake': ensure => latest;
        'xvfb': ensure => latest; # necessary for headless X server
    }

    exec { "build_phantomjs":
        command => 'cd /home/vagrant/ && wget http://phantomjs.googlecode.com/files/phantomjs-1.7.0-linux-i686.tar.bz2 && tar xvjf phantomjs-1.7.0-linux-i686.tar.bz2 && sudo ln -s /home/vagrant/phantomjs-1.7.0-linux-i686/bin/phantomjs /usr/local/bin/phantomjs',
        path => '/usr/local/bin:/usr/bin:/bin',
        require => [Package['libqt4-dev'],Package['qt4-qmake']],
        unless => 'test -x /usr/local/bin/phantomjs',
        user => "vagrant",
        provider => "shell"
    }
}
