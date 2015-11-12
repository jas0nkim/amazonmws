<?php

namespace Ebay;

// General utility class. Currently not used.
class Utils {
	static public function findByName($values, $name) {
		foreach($values as $value) {
			if ($value->Name == $name) {
				return $value;
			}
		}
	}
}