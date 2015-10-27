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

	public function GetItem($Timestamp, $Ack, $CorrelationID, $Version, 
		$Build, $NotificationEventName, $RecipientUserID, $Item) {
		// $price = $Item->BuyItNowPrice;

		$url = sprintf('http://%s:%d%s%s', 
			APP_HOST, 
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
			'Item' => is_array($Item) ? $Item : (array) $Item,
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
		$Build, $NotificationEventName, $PaginationResult, $HasMoreTransactions,
		$TransactionsPerPage, $PageNumber, $ReturnedTransactionCountActual, $Item,
		$TransactionArray, $PayPalPreferred) {

		$url = sprintf('http://%s:%d%s%s', 
			APP_HOST, 
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
			'PaginationResult' => 
				is_array($PaginationResult) ? $PaginationResult : (array) $PaginationResult,
			'HasMoreTransactions' => $HasMoreTransactions,
			'TransactionsPerPage' => $TransactionsPerPage,
			'PageNumber' => $PageNumber,
			'ReturnedTransactionCountActual' => $ReturnedTransactionCountActual,
			'Item' => is_array($Item) ? $Item : (array) $Item,
			'TransactionArray' => 
				is_array($TransactionArray) ? $TransactionArray : (array) $TransactionArray,
			'PayPalPreferred' => $PayPalPreferred,
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
