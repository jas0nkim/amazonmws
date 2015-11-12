<?php

mb_internal_encoding("UTF-8");

$master = realpath(dirname(__FILE__));

defined('EBNL_MASTER_PATH') or define('EBNL_MASTER_PATH', $master);
defined('EBNL_PUBLIC_PATH') or define('EBNL_PUBLIC_PATH', realpath($master . '/web'));
defined('EBNL_SRC_PATH') or define('EBNL_SRC_PATH', realpath($master . '/src'));
defined('EBNL_VENDOR_PATH') or define('EBNL_VENDOR_PATH', realpath($master . '/vendor'));
defined('EBNL_ROOT_PATH') or define('EBNL_ROOT_PATH', realpath($master . '/../../..'));
defined('EBNL_CONFIG_PATH') or define('EBNL_CONFIG_PATH', realpath(EBNL_ROOT_PATH . '/config'));
defined('EBNL_AMWS_PATH') or define('EBNL_AMWS_PATH', realpath(EBNL_ROOT_PATH. '/amazonmws'));

require_once(EBNL_VENDOR_PATH . '/autoload.php');

// app config
$app_config = \Symfony\Component\Yaml\Yaml::parse(file_get_contents(EBNL_CONFIG_PATH . '/app.yaml'));
defined('APP_ENV') or define('APP_ENV', $app_config['env']);
defined('APP_HOST') or define('APP_HOST', $app_config['host']);
defined('APP_PORT_SOAP') or define('APP_PORT_SOAP', $app_config['port']['soap']);
defined('APP_PORT_RESTFUL') or define('APP_PORT_RESTFUL', $app_config['port']['restful']);
defined('APP_LOG_SERVER_HOST') or define('APP_LOG_SERVER_HOST', $app_config['log_server']['host']);
defined('APP_LOG_SERVER_PORT') or define('APP_LOG_SERVER_PORT', $app_config['log_server']['port']);
defined('APP_LOG_LEVEL') or define('APP_LOG_LEVEL', APP_ENV == "stage" ? \Monolog\Logger::DEBUG : \Monolog\Logger::DEBUG);
defined('APP_EBAY_NOTIFICATION_ENDPOINT_URL') or define('APP_EBAY_NOTIFICATION_ENDPOINT_URL', $app_config['ebay']['notification_endpoint_url']);

// log php errors
function log_errors($severity, $message, $file, $line) {
	if (!(error_reporting() & $severity)) {
        // This error code is not included in error_reporting
        (new \Amws\Core\Logger())->error($message);
    }
    (new \Amws\Core\Logger())->exception(new \ErrorException($message, 0, $severity, $file, $line));
}
set_error_handler('log_errors');

// routing starts
\NoahBuscher\Macaw\Macaw::post(APP_EBAY_NOTIFICATION_ENDPOINT_URL, function() {
	// ebay config
	$ebay_config = \Symfony\Component\Yaml\Yaml::parse(file_get_contents(EBNL_CONFIG_PATH . '/ebay.yaml'));
	$site = APP_ENV == "stage" ? "api.sandbox.ebay.com" : "api.ebay.com";
	$devid = $ebay_config[$site]['devid'];
	$appid = $ebay_config[$site]['appid'];
	$certid = $ebay_config[$site]['certid'];

	// Create and configure session
	$session = new \Ebay\Session($devid, $appid, $certid);
	// error_log(serialize(apache_request_headers()));
	// error_log("trying to listen");
	$stdin = file_get_contents('php://input');
	(new \Amws\Core\Logger())->debug("ebay Platform Notification - RAW XML REQUEST\n\n$stdin");
	//file_put_contents('GetItemRequest.xml', $stdin);
	// error_log($stdin);

	try {
		$server = new \SOAPServer(null, array('uri' => 'urn:ebay:apis:eBLBaseComponents'));
		$server->setClass('\\Amws\\EbayPlatformNotificationListener', $session);
		$server->handle();
	} catch (\Ebay\PlatformNotificationException $e) {
		(new \Amws\Core\Logger())->exception($e);
	}
});

\NoahBuscher\Macaw\Macaw::dispatch();
