<?php

namespace Ebay\Type;

class PictureDetailsType implements IteratorAggregate {
	public function getIterator() {
		// put this in __wakeUp()
		if (!is_array($this->PictureURL)) {
			$this->PictureURL = array($this->PictureURL);
		}

        return new ArrayObject($this->PictureURL);
    }
}
