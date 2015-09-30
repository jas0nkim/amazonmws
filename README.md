# amazonmws

How to run Selenium server
===================================

java -jar ./selenium-server-standalone-2.47.1.jar


Python requirements
===================================

$ pip list

boto (2.38.0)
cffi (1.2.1)
characteristic (14.3.0)
cryptography (1.0.1)
cssselect (0.9.1)
EasyProcess (0.1.9)
ebaysdk (2.1.2)
enum34 (1.0.4)
graypy (0.2.12)
idna (2.0)
ipaddress (1.0.14)
lxml (3.4.4)
MySQL-python (1.2.5)
pip (7.1.2)
pipdeptree (0.4.3)
pyasn1 (0.1.8)
pyasn1-modules (0.0.7)
pycparser (2.14)
pyOpenSSL (0.15.1)
PyVirtualDisplay (0.1.5)
queuelib (1.4.2)
requests (2.7.0)
Scrapy (1.0.3)
selenium (2.47.1)
service-identity (14.0.0)
setuptools (0.9.8)
six (1.9.0)
storm (0.20)
Twisted (15.4.0)
w3lib (1.12.0)
zope.interface (4.1.2)


$ pipdeptree -fl

Warning!!! Possible confusing dependencies found:
* Scrapy==1.0.3 -> pyOpenSSL [installed: 0.15.1]
  service-identity==14.0.0 -> pyOpenSSL [required: >=0.12, installed: 0.15.1]
* Scrapy==1.0.3 -> six [required: >=1.5.2, installed: 1.9.0]
  w3lib==1.12.0 -> six [required: >=1.4.1, installed: 1.9.0]
  pyOpenSSL==0.15.1 -> six [required: >=1.5.2, installed: 1.9.0]
  cryptography==1.0.1 -> six [required: >=1.4.1, installed: 1.9.0]
* pyasn1-modules==0.0.7 -> pyasn1 [required: >=0.1.8, installed: 0.1.8]
  service-identity==14.0.0 -> pyasn1 [installed: 0.1.8]
  cryptography==1.0.1 -> pyasn1 [required: >=0.1.8, installed: 0.1.8]
------------------------------------------------------------------------
boto==2.38.0
ebaysdk==2.1.2
    lxml==3.4.4
    requests==2.7.0
graypy==0.2.12
MySQL-python==1.2.5
PyVirtualDisplay==0.1.5
    EasyProcess==0.1.9
Scrapy==1.0.3
    cssselect==0.9.1
    queuelib==1.4.2
    pyOpenSSL==0.15.1
      six==1.9.0
      cryptography==1.0.1
        idna==2.0
        pyasn1==0.1.8
        six==1.9.0
        setuptools
        enum34==1.0.4
        ipaddress==1.0.14
        cffi==1.2.1
          pycparser==2.14
    w3lib==1.12.0
      six==1.9.0
    lxml==3.4.4
    Twisted==15.4.0
      zope.interface==4.1.2
        setuptools
    six==1.9.0
    service-identity==14.0.0
      pyOpenSSL==0.15.1
        six==1.9.0
        cryptography==1.0.1
          idna==2.0
          pyasn1==0.1.8
          six==1.9.0
          setuptools
          enum34==1.0.4
          ipaddress==1.0.14
          cffi==1.2.1
            pycparser==2.14
      characteristic==14.3.0
      pyasn1-modules==0.0.7
        pyasn1==0.1.8
      pyasn1==0.1.8
selenium==2.47.1
storm==0.20