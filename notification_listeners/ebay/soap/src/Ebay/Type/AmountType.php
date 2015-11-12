<?php

namespace Ebay\Type;

class AmountType {
	public function __toString() {
		return (string) $this->_;
	}
}