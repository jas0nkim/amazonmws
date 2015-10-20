<?php

namespace Ebay\Type;

class PaginatedItemArrayType implements IteratorAggregate {
	public function getIterator( ) {
        return $this->ItemArray;
    }
	
}