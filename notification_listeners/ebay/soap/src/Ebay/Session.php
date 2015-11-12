<?php

namespace Ebay;

class Session {
	protected $properties;
	const URL_PRODUCTION = 'https://api.ebay.com/wsapi';
	const URL_SANDBOX    = 'https://api.sandbox.ebay.com/wsapi';
 	public function __construct($dev, $app, $cert) {
		$this->properties = array(
			'dev'      => null,
			'app'      => null,
			'cert'     => null,
			'wsdl'     => null,
			'options'  => null,
			'token'    => null,
			'userid'   => null,
			'password' => null,
			'site'     => null,
			'location' => null,
			'ns'       => null,
			'version'  => null,
			'runame'   => null,
		);
		$this->dev = $dev;
		$this->app = $app;
		$this->cert = $cert;
	
		$this->wsdl = 'http://developer.ebay.com/webservices/latest/eBaySvc.wsdl';
#		$this->wsdl = './eBaySvc.wsdl';
		$this->options = array('trace' => true, 
		                       'exceptions' => false,
		                       'classmap' => array(/* 'UserType' => 'eBayUserType', */
		                                           'GetSearchResultsResponseType' => '\\EBay\\Type\\GetSearchResultsResponseType',
		                                           'SearchResultItemArrayType' => '\\Ebay\\Type\\SearchResultItemArrayType',
		                                           'SearchResultItemType' => '\\Ebay\\Type\\SearchResultItemType',
		                                           'AmountType' => '\\Ebay\\Type\\AmountType',
		                                           'FeeType' => '\\Ebay\\Type\\FeeType',
		                                           'FeesType' => '\\Ebay\\Type\\FeesType',
		                                           'PaginatedItemArrayType' => '\\Ebay\\Type\\PaginatedItemArrayType',
		                                           'ItemArrayType' => '\\Ebay\\Type\\ItemArrayType',
		                                           'ItemType' => '\\Ebay\\Type\\ItemType',
		                                           'NameValueListArrayType' => '\\Ebay\\Type\\NameValueListArrayType',
		                                           'NameValueListType' => '\\Ebay\\Type\\NameValueListType',
		                                           'PictureDetailsType' => '\\Ebay\\Type\\PictureDetailsType',
		                                          ),
#		                       'compression' => SOAP_COMPRESSION_ACCEPT,
		                      );
		$this->ns = 'urn:ebay:apis:eBLBaseComponents';
		$this->version = 501; // should pull this from the WSDL
	}
	public function __set($property, $value) {
		 if (array_key_exists($property, $this->properties)) {
		    $this->properties[$property] = $value;
		 }
	}
	public function __get($property) {
		 if (array_key_exists($property, $this->properties)) {
		    return $this->properties[$property];
		 } else {
		    return null;
		 }
	}
	public function __isset($property) {
		 return array_key_exists($property, $this->properties);
	}
}
