<?php

namespace Ebay\Type;

class FeeType {
	public function __toString() {
		return (string) $this->Fee->_;
	}
}