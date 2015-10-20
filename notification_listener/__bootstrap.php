<?php

mb_internal_encoding("UTF-8");

$master = realpath(dirname(__FILE__));

define('EBNL_ROOT_PATH', $master);
define('EBNL_PUBLIC_PATH', realpath($master . '/soap' ) );
define('EBNL_SRC_PATH', realpath($master . '/src'));
define('EBNL_VENDOR_PATH', realpath($master . '/vendor'));

require_once(EBNL_VENDOR_PATH . '/autoload.php');


$config = parse_ini_file('ebay.ini', true);

$site = 'sandbox';

// need to change to yaml
$dev = $config[$site]['devId'];
$app = $config[$site]['appId'];
$cert = $config[$site]['cert'];
// Create and configure session

$session = new \Ebay\Session($dev, $app, $cert);
error_log(serialize(apache_request_headers()));
//error_log("trying to listen");
$stdin = $GLOBALS['HTTP_RAW_POST_DATA'];
//file_put_contents('GetItemRequest.xml', $stdin);
error_log($stdin);

$server = new \SOAPServer(null, array('uri'=>'urn:ebay:apis:eBLBaseComponents'));
$server->setClass('\\Listener\\EbayPlatformNotificationListener', $session, true);
$server->handle();
