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

		(new Core\Logger())->debug("GetItem - Timestamp -- " . $Timestamp);
		(new Core\Logger())->debug("GetItem - Ack -- " . $Ack);
		(new Core\Logger())->debug("GetItem - CorrelationID -- " . $CorrelationID);
		(new Core\Logger())->debug("GetItem - Version -- " . $Version);
		(new Core\Logger())->debug("GetItem - Build -- " . $Build);
		(new Core\Logger())->debug("GetItem - NotificationEventName -- " . $NotificationEventName);
		(new Core\Logger())->debug("GetItem - RecipientUserID -- " . $RecipientUserID);
		(new Core\Logger())->debug("GetItem - Item -- " .  print_r($Item, true));

		$data = array(
			'Timestamp' => $Timestamp,
			'Ack' => $Ack,
			'CorrelationID' => $CorrelationID,
			'Version' => $Version,
			'Build' => $Build,
			'NotificationEventName' => $NotificationEventName,
			'RecipientUserID' => $RecipientUserID,
			'Item' => json_encode($Item),
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

		(new Core\Logger())->debug("GetItemTransactions - Timestamp -- " . $Timestamp);
		(new Core\Logger())->debug("GetItemTransactions - Ack -- " . $Ack);
		(new Core\Logger())->debug("GetItemTransactions - CorrelationID -- " . $CorrelationID);
		(new Core\Logger())->debug("GetItemTransactions - Version -- " . $Version);
		(new Core\Logger())->debug("GetItemTransactions - Build -- " . $Build);
		(new Core\Logger())->debug("GetItemTransactions - NotificationEventName -- " . $NotificationEventName);
		(new Core\Logger())->debug("GetItemTransactions - PaginationResult -- " . print_r($PaginationResult, true));
		(new Core\Logger())->debug("GetItemTransactions - HasMoreTransactions -- " . $HasMoreTransactions);
		(new Core\Logger())->debug("GetItemTransactions - TransactionsPerPage -- " . $TransactionsPerPage);
		(new Core\Logger())->debug("GetItemTransactions - PageNumber -- " . $PageNumber);
		(new Core\Logger())->debug("GetItemTransactions - ReturnedTransactionCountActual -- " . $ReturnedTransactionCountActual);
		(new Core\Logger())->debug("GetItemTransactions - Item -- " . print_r($Item, true));
		(new Core\Logger())->debug("GetItemTransactions - TransactionArray -- " . print_r($TransactionArray, true));
		(new Core\Logger())->debug("GetItemTransactions - PayPalPreferred -- " . $PayPalPreferred);

		$data = array(
			'Timestamp' => $Timestamp,
			'Ack' => $Ack,
			'CorrelationID' => $CorrelationID,
			'Version' => $Version,
			'Build' => $Build,
			'NotificationEventName' => $NotificationEventName,
			'PaginationResult' => json_encode($PaginationResult),
			'HasMoreTransactions' => $HasMoreTransactions,
			'TransactionsPerPage' => $TransactionsPerPage,
			'PageNumber' => $PageNumber,
			'ReturnedTransactionCountActual' => $ReturnedTransactionCountActual,
			'Item' => json_encode($Item),
			'TransactionArray' => json_encode($TransactionArray),
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
