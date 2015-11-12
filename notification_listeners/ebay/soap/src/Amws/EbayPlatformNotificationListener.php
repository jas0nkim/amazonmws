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
			APP_HOST, 
			APP_PORT_RESTFUL, 
			APP_EBAY_NOTIFICATION_ENDPOINT_URL,
			'/GetItem');

		(new Core\Logger())->debug("$NotificationEventName (GetItem) - Timestamp -- $Timestamp");
		(new Core\Logger())->debug("$NotificationEventName (GetItem) - Ack -- $Ack");
		(new Core\Logger())->debug("$NotificationEventName (GetItem) - CorrelationID -- $CorrelationID");
		(new Core\Logger())->debug("$NotificationEventName (GetItem) - Version -- $Version");
		(new Core\Logger())->debug("$NotificationEventName (GetItem) - Build -- $Build");
		(new Core\Logger())->debug("$NotificationEventName (GetItem) - NotificationEventName -- $NotificationEventName");
		(new Core\Logger())->debug("$NotificationEventName (GetItem) - RecipientUserID -- $RecipientUserID");
		(new Core\Logger())->debug("NotificationEventName (GetItem) - Item -- " . $this->_encode($Item));

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
			APP_HOST, 
			APP_PORT_RESTFUL, 
			APP_EBAY_NOTIFICATION_ENDPOINT_URL,
			'/GetItemTransactions');

		(new Core\Logger())->debug("$NotificationEventName (GetItemTransactions) - Timestamp -- $Timestamp");
		(new Core\Logger())->debug("$NotificationEventName (GetItemTransactions) - Ack -- $Ack");
		(new Core\Logger())->debug("$NotificationEventName (GetItemTransactions) - CorrelationID -- $CorrelationID");
		(new Core\Logger())->debug("$NotificationEventName (GetItemTransactions) - Version -- $Version");
		(new Core\Logger())->debug("$NotificationEventName (GetItemTransactions) - Build -- $Build");
		(new Core\Logger())->debug("$NotificationEventName (GetItemTransactions) - NotificationEventName -- $NotificationEventName");
		(new Core\Logger())->debug("$RecipientUserID (GetItemTransactions) - RecipientUserID -- $RecipientUserID");
		(new Core\Logger())->debug("$EIASToken (GetItemTransactions) - EIASToken -- $EIASToken");
		(new Core\Logger())->debug("$NotificationEventName (GetItemTransactions) - PaginationResult -- " . $this->_encode($PaginationResult));
		(new Core\Logger())->debug("$NotificationEventName (GetItemTransactions) - HasMoreTransactions -- " . $this->_encode($HasMoreTransactions));
		(new Core\Logger())->debug("$NotificationEventName (GetItemTransactions) - TransactionsPerPage -- " . $this->_encode($TransactionsPerPage));
		(new Core\Logger())->debug("$NotificationEventName (GetItemTransactions) - PageNumber -- " . $this->_encode($PageNumber));
		(new Core\Logger())->debug("$NotificationEventName (GetItemTransactions) - ReturnedTransactionCountActual -- " . $this->_encode($ReturnedTransactionCountActual));
		(new Core\Logger())->debug("$NotificationEventName (GetItemTransactions) - Item -- " . $this->_encode($Item));
		(new Core\Logger())->debug("$NotificationEventName (GetItemTransactions) - TransactionArray -- " . $this->_encode($TransactionArray));
		(new Core\Logger())->debug("$NotificationEventName (GetItemTransactions) - PayPalPreferred -- " . $this->_encode($PayPalPreferred));

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
