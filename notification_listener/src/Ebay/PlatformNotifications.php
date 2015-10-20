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
		if ($this->debug) { error_log("$me: $string"); }
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
