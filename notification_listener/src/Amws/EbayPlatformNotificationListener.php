<?php

namespace Amws;

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
		(new Logger())->debug("$me: $string");
	}


	public function GetItem($Timestamp, $Ack, $CorrelationID,
			$Version, $Build, $NotificationEventName, 
			$RecipientUserID, $Item) {
		// $price = $Item->BuyItNowPrice;

		switch ($NotificationEventName) {
			case "ItemSold":

				(new Logger())->debug("TEST TEST");

				$url = 'http://localhost:8090/test';
				$data = array(
					'Timestamp' => $Timestamp,
					'Ack' => $Ack,
					'CorrelationID' => $CorrelationID,
					'Version' => $Version,
					'Build' => $Build,
					'NotificationEventName' => $NotificationEventName,
					'RecipientUserID' => $RecipientUserID,
					'Item' => json_encode((array) $Item),
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

				var_dump($result);
				break;

			default:
				break;
		}

       return $Ack;
	}


}
