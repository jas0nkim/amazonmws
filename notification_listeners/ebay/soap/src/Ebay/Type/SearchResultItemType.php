<?php

namespace Ebay\Type;

class SearchResultItemType {
	public function __toString() {
		return $this->Item->Title;
	}
}