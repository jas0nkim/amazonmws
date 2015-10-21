<?php

namespace Ebay;

class PlatformNotificationListener extends PlatformNotifications {
	protected $NotificationSignature;
	// Dispatch method to ensure signature validation
	public function __call($method, $args) {
		$s = "Called with $method";
		$this->carp($s);
		// if ($this->ValidateSignature($args[0])) {
			// strip off trailing "Response"
			$method = substr($method, 0, -8);
			if (method_exists($this, $method)) {
				return call_user_func_array(array($this, $method), $args);
			}
		// } else {
		// 	throw new PlatformNotificationException("Invalid signature");
		// }
		
		// Today is a good day to die.
		die("Death");
	}
	// Extract Signature for validation later
	// Can't validate here because we don't have access to the Timestamp
	public function RequesterCredentials($RequesterCredentials) {
		$this->NotificationSignature = $RequesterCredentials->NotificationSignature;
	}
	protected function ValidateSignature($Timestamp) {
		// Check for Signature Match
		$CalculatedSignature = $this->CalculateSignature($Timestamp);
		$NotificationSignature = $this->NotificationSignature;
		if ($CalculatedSignature != $NotificationSignature) {
			$this->carp("Sig Mismatch: Calc: $CalculatedSignature, Note: $NotificationSignature");
			return false;
		} else {
			$this->carp("Sig Match: $NotificationSignature");
		}
		// Check that Timestamp is within 10 minutes of now
		$tz = date_default_timezone_get();
		date_default_timezone_set('UTC');
		$then = strtotime($Timestamp);
		$now = time();
		date_default_timezone_set($tz);
		$drift = $now - $then;
		$ten_minutes = 60 * 10;
		if ($drift > $ten_minutes) {
			$this->carp("Time Drift is too large: $drift seconds");
			return false;
		} else {
			$this->carp("Time Drift is okay: $drift seconds");
		}
		return true;
	}
	// Arg order is brittle, assumes constant return ordering from eBay
	// 
	// OVERRIDE this method
	public function GetMemberMessages($Timestamp, $Ack, $CorrelationID,
						$Version, $Build, $NotificationEventName, 
						$RecipientUserID, $MemberMessage, 
						$PaginationResult, $HasMoreItems) {
		// Extract some data to prove this is working
		$UserID = $MemberMessage->MemberMessageExchange->Item->Seller->UserID;
		$this->carp($UserID);
		return $UserID;
	}

	// OVERRIDE this method
	public function GetItem($Timestamp, $Ack, $CorrelationID,
				$Version, $Build, $NotificationEventName, 
				$RecipientUserID, $Item) {
	       $ItemID = $Item->ItemID;
	       return "OutBid: $ItemID";
	}
}
