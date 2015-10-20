<?php

namespace Ebay;

// Main class for communication with eBay Web services via SOAP
class Soap extends SoapClient {
	protected $headers = null;
	protected $session = null;

	public function __construct(Session $session) {
		$this->session = $session;
		$this->__setHeaders();
		parent::__construct($session->wsdl, $session->options);
	}

	protected function __setHeaders() {
		$eBayAuth = $this->__geteBayAuth($this->session);
		$header_body = new SoapVar($eBayAuth, SOAP_ENC_OBJECT);
		$headers = array(new SOAPHeader($this->session->ns, 'RequesterCredentials', $header_body));
	
		$this->headers = $headers;
	}

	protected function __geteBayAuth(Session $session) {
		$credentials = array();
		$eBayAuth = array();
		
		$credentials['AppId'] = new SoapVar($session->app, XSD_STRING, null, null, null, $session->ns);
		$credentials['DevId'] = new SoapVar($session->dev, XSD_STRING, null, null, null, $session->ns);
		$credentials['AuthCert'] = new SoapVar($session->cert, XSD_STRING, null, null, null, $session->ns);
		if (isset($session->userid) && ($session->userid != null)) {
			$credentials['Username'] = new SoapVar($session->userid, XSD_STRING, null, null, null, $session->ns);
		}
		if (isset($session->password) && ($session->password != null)) {
			$credentials['Password'] = new SoapVar($session->password, XSD_STRING, null, null, null, $session->ns);
		}

		if (isset($session->token)) {
			$eBayAuth['eBayAuthToken'] = new SoapVar($session->token, XSD_STRING, null, null, null, $session->ns);
		}
		$eBayAuth['Credentials'] = new SoapVar($credentials, SOAP_ENC_OBJECT, null, null, null, $session->ns);

		return $eBayAuth;
	}

 	public function __call($function, $args) {
		if (empty($args[0]['Version'])) {
			$args[0]['Version'] = $this->session->version;
		}

		$callname = $function;
		$siteid = $this->session->site;
		$version = $args[0]['Version'];
		$appid = $this->session->app;
		$Routing = 'default'; // XXX: hardcoded

		$query_string = http_build_query(array('callname' => $callname, 'siteid' => $siteid, 'version' => $version, 'appid' => $appid, 'Routing' => $Routing));
	 	$location = "{$this->session->location}?{$query_string}";

 		return $this->__soapCall($function, $args, array('location' => $location), $this->headers);
 	}
}