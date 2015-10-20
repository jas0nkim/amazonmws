<?php

namespace Ebay\Type;

class SearchResultItemArrayType implements IteratorAggregate {
	public function getIterator() {
		// put this in __wakeUp()
		if (!is_array($this->SearchResultItem)) {
			$this->SearchResultItem = array($this->SearchResultItem);
		}

        return new ArrayObject($this->SearchResultItem);
    }
}