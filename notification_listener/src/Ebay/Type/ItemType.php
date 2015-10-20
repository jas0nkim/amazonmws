<?php

namespace Ebay\Type;

class ItemType {
	public function __toString() {
		return (string) $this->Title;
	}
}
