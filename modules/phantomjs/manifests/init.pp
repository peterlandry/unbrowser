class phantomjs {
    package {
        'libqt4-dev': ensure => latest;
        'qt4-qmake': ensure => latest;
        'xvfb': ensure => latest; # necessary for headless X server
    }

    exec { "build_phantomjs":
        command => 'git clone git://github.com/ariya/phantomjs.git /tmp/phantomjs && cd /tmp/phantomjs && git checkout 1.2 && qmake-qt4 && make && mv /tmp/phantomjs/bin/phantomjs /usr/local/bin/ && rm /tmp/phantomjs',
        path => '/usr/local/bin:/usr/bin:/bin',
        require => [Package['libqt4-dev'],Package['qt4-qmake']],
        unless => 'test -x /usr/local/bin/phantomjs'
    }
}
