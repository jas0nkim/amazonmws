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

		ob_start();
		var_dump($PaginationResult);
		$PaginationResult_dump = ob_get_clean();

		// TransactionsPerPage causes error
		ob_start();
		var_dump($TransactionsPerPage);
		$TransactionsPerPage_dump = ob_get_clean();

		ob_start();
		var_dump($Item);
		$Item_dump = ob_get_clean();

		ob_start();
		var_dump($TransactionArray);
		$TransactionArray_dump = ob_get_clean();

		(new Core\Logger())->debug("GetItemTransactions - Timestamp -- " . $Timestamp);
		(new Core\Logger())->debug("GetItemTransactions - Ack -- " . $Ack);
		(new Core\Logger())->debug("GetItemTransactions - CorrelationID -- " . $CorrelationID);
		(new Core\Logger())->debug("GetItemTransactions - Version -- " . $Version);
		(new Core\Logger())->debug("GetItemTransactions - Build -- " . $Build);
		(new Core\Logger())->debug("GetItemTransactions - NotificationEventName -- " . $NotificationEventName);
		(new Core\Logger())->debug("GetItemTransactions - PaginationResult -- " . $PaginationResult_dump);
		(new Core\Logger())->debug("GetItemTransactions - HasMoreTransactions -- " . $HasMoreTransactions);
		(new Core\Logger())->debug("GetItemTransactions - TransactionsPerPage -- " . $TransactionsPerPage_dump);
		(new Core\Logger())->debug("GetItemTransactions - PageNumber -- " . $PageNumber);
		(new Core\Logger())->debug("GetItemTransactions - ReturnedTransactionCountActual -- " . $ReturnedTransactionCountActual);
		(new Core\Logger())->debug("GetItemTransactions - Item -- " . $Item_dump);
		(new Core\Logger())->debug("GetItemTransactions - TransactionArray -- " . $TransactionArray_dump);
		(new Core\Logger())->debug("GetItemTransactions - PayPalPreferred -- " . $PayPalPreferred);

		$data = array(
			'Timestamp' => $Timestamp,
			'Ack' => $Ack,
			'CorrelationID' => $CorrelationID,
			'Version' => $Version,
			'Build' => $Build,
			'NotificationEventName' => $NotificationEventName,
			'PaginationResult' => json_encode($PaginationResult_dump),
			'HasMoreTransactions' => $HasMoreTransactions,
			'TransactionsPerPage' => $TransactionsPerPage,
			'PageNumber' => $PageNumber,
			'ReturnedTransactionCountActual' => $ReturnedTransactionCountActual,
			'Item' => json_encode($Item_dump),
			'TransactionArray' => json_encode($TransactionArray_dump),
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
