<?php

namespace Amws;

use \Amws\Core;

class EbayPlatformNotificationListener extends \Ebay\PlatformNotificationListener {

	public function __construct(\Ebay\Session $session) {
		parent::__construct($session);
	}

	/**
	 * override
	 * @param  [type] $string [description]
	 * @return [type]         [description]
	 */
	protected function carp($string) {
		$me = get_class($this);
		(new Core\Logger())->debug("$me: $string");
	}

	protected function _encode($value) {
		return $value instanceof \stdClass || is_array($value) ? json_encode($value) : $value;
	}

	public function GetItem($Timestamp, $Ack, $CorrelationID, $Version, 
		$Build, $NotificationEventName, $RecipientUserID, $Item) {
		// $price = $Item->BuyItNowPrice;

		$url = sprintf('http://%s:%d%s%s', 
			APP_HOST_ORDERING, 
			APP_PORT_RESTFUL, 
			APP_EBAY_NOTIFICATION_ENDPOINT_URL,
			'/GetItem');

		$data = array(
			'Timestamp' => $Timestamp,
			'Ack' => $Ack,
			'CorrelationID' => $CorrelationID,
			'Version' => $Version,
			'Build' => $Build,
			'NotificationEventName' => $NotificationEventName,
			'RecipientUserID' => $RecipientUserID,
			'Item' => $this->_encode($Item),
			'raw' => file_get_contents('php://input'),
		);

		// use key 'http' even if you send the request to https://...
		$options = array(
		    'http' => array(
		        'header'  => "Content-type: application/x-www-form-urlencoded\r\n",
		        'method'  => 'POST',
		        'content' => http_build_query($data),
		    ),
		);
		$context  = stream_context_create($options);
		$result = file_get_contents($url, false, $context);
		return $Ack;
	}

	public function GetItemTransactions($Timestamp, $Ack, $CorrelationID, $Version,
		$Build, $NotificationEventName, $RecipientUserID, $EIASToken, $PaginationResult, $HasMoreTransactions, $TransactionsPerPage, $PageNumber, $ReturnedTransactionCountActual, $Item, $TransactionArray, $PayPalPreferred) {

		$url = sprintf('http://%s:%d%s%s', 
			APP_HOST_ORDERING, 
			APP_PORT_RESTFUL, 
			APP_EBAY_NOTIFICATION_ENDPOINT_URL,
			'/GetItemTransactions');

		$data = array(
			'Timestamp' => $Timestamp,
			'Ack' => $Ack,
			'CorrelationID' => $CorrelationID,
			'Version' => $Version,
			'Build' => $Build,
			'NotificationEventName' => $NotificationEventName,
			'RecipientUserID' => $RecipientUserID,
			'EIASToken' => $EIASToken,
			'PaginationResult' => $this->_encode($PaginationResult),
			'HasMoreTransactions' => $this->_encode($HasMoreTransactions),
			'TransactionsPerPage' => $this->_encode($TransactionsPerPage),
			'PageNumber' => $this->_encode($PageNumber),
			'ReturnedTransactionCountActual' => $this->_encode($ReturnedTransactionCountActual),
			'Item' => $this->_encode($Item),
			'TransactionArray' => $this->_encode($TransactionArray),
			'PayPalPreferred' => $this->_encode($PayPalPreferred),
			'raw' => file_get_contents('php://input'),
		);

		// use key 'http' even if you send the request to https://...
		$options = array(
		    'http' => array(
		        'header'  => "Content-type: application/x-www-form-urlencoded\r\n",
		        'method'  => 'POST',
		        'content' => http_build_query($data),
		    ),
		);
		$context  = stream_context_create($options);
		$result = file_get_contents($url, false, $context);
		return $Ack;
	}
}
