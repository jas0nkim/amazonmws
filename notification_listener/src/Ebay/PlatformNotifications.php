<?php

namespace Ebay;

class PlatformNotifications {
	protected $session = null;
	protected $debug;
	public function __construct(Session $session, $debug = false) {
		$this->session = $session;
		$this->debug = $debug;
	}
	protected function carp($string) {
		$me = get_class($this);
		if ($this->debug) {

			$logger = new \Monolog\Logger('phpsoap_platform_notification');

            try {
				// setup gelf/graylog2 connection
				$gelf_transport = new \Gelf\Transport\UdpTransport($site_settings["graylog_server"], 12201, \Gelf\Transport\UdpTransport::CHUNK_SIZE_LAN);
				$gelf_publisher = new \Gelf\Publisher();
				$gelf_publisher->addTransport($gelf_transport);

				$log->pushHandler(new \Monolog\Handler\GelfHandler($gelf_publisher, $min_log_level));
				error_log("$me: $string");

            } catch (\RuntimeException $e) {
                // couldn't connect to graylog, so switch to normal log
                $logger->pushHandler(new \Monolog\Handler\StreamHandler($this->trace_file, $min_log_level));
            }
		}
	}
	protected function CalculateSignature($Timestamp) {
		$DevID = $this->session->dev;
		$AppID = $this->session->app;
		$Cert  = $this->session->cert;
		$hash = "{$Timestamp}{$DevID}{$AppID}{$Cert}";
		$this->carp($hash);
		// Not quite sure why we need the pack('H*'), but we do
		$Signature = base64_encode(pack('H*', md5($hash)));
		return $Signature;
	}
}
