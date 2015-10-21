<?php

mb_internal_encoding("UTF-8");

defined('APP_ENV') or define('APP_ENV', 'stage');
// defined('APP_ENV') or define('APP_ENV', 'prod');

$master = realpath(dirname(__FILE__));

defined('EBNL_MASTER_PATH') or define('EBNL_MASTER_PATH', $master);
defined('EBNL_ROOT_PATH') or define('EBNL_ROOT_PATH', realpath($master . '/..'));
defined('EBNL_PUBLIC_PATH') or define('EBNL_PUBLIC_PATH', realpath($master . '/soap'));
defined('EBNL_SRC_PATH') or define('EBNL_SRC_PATH', realpath($master . '/src'));
defined('EBNL_VENDOR_PATH') or define('EBNL_VENDOR_PATH', realpath($master . '/vendor'));
defined('EBNL_AMWS_PATH') or define('EBNL_AMWS_PATH', realpath($master . '/../amazonmws'));

require_once(EBNL_VENDOR_PATH . '/autoload.php');

$ebay_config = Symfony\Component\Yaml\Yaml::parse(file_get_contents(EBNL_AMWS_PATH . '/ebay.yaml'));
$site = APP_ENV == "stage" ? "api.sandbox.ebay.com" : "api.ebay.com";

$devid = $ebay_config[$site]['devid'];
$appid = $ebay_config[$site]['appid'];
$certid = $ebay_config[$site]['certid'];

// Create and configure session
$session = new \Ebay\Session($devid, $appid, $certid);
// error_log(serialize(apache_request_headers()));
error_log("trying to listen");
$stdin = file_get_contents('php://input');
//file_put_contents('GetItemRequest.xml', $stdin);
// error_log($stdin);

$server = new \SOAPServer(null, array('uri' => 'urn:ebay:apis:eBLBaseComponents'));
$server->setClass('\\Amws\\EbayPlatformNotificationListener', $session, true);
$server->handle();
