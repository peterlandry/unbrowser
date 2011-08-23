group { "puppet": 
    ensure => present, 
} 

include python
include phantomjs

class unbrowser {
  package {
    "git-core": ensure => latest;
    "binutils": ensure => latest;
    "vim": ensure => latest;
  }
  exec { "install_requirements":
    command => "pip install -r /vagrant/requirements.txt",
    path => "/usr/local/bin:/usr/bin:/bin",
    require => Class["python"],
  }

}

include unbrowser 

