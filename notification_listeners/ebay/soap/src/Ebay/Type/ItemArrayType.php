<?php

namespace Ebay\Type;

class ItemArrayType implements \IteratorAggregate {
	public function getIterator( ) {
        return new ArrayObject($this->Item);
    }
	
}