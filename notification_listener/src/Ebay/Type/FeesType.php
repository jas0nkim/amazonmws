<?php

namespace Ebay\Type;

// The following classes are used in the classmap array
// Right now, they are largely experiments to see how I can make it easier to use the API
class FeesType implements ArrayAccess {
	public function offsetExists($offset) {
		foreach ($this->Fee as $value) {
			if ($value->Name == $offset) {
				return true;
			}
		}

		return false;
	}

	public function offsetGet($offset) {
		foreach ($this->Fee as $value) {
			if ($value->Name == $offset) {
				return $value;
			}
		}
	}

	public function offsetSet($offset, $value) {
		return true;
	}

	public function offsetUnset($offset) {
		return true;
	}

}