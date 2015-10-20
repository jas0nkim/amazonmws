<?php

namespace Ebay\Type;

class GetSearchResultsResponseType implements IteratorAggregate {
	public function getIterator( ) {
        return $this->SearchResultItemArray;
    }
	
}