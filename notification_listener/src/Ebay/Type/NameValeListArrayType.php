<?php

namespace Ebay\Type;

class NameValueListArrayType implements \IteratorAggregate, \ArrayAccess {
	public function getIterator() {
		// put this in __wakeUp()
		if (!is_array($this->NameValueList)) {
			$this->NameValueList = array($this->NameValueList);
		}

        return new \ArrayObject($this->NameValueList);
    }

	public function offsetExists($offset) {
		foreach ($this as $NameValueList) {
			if ($NameValueList->Name == $offset) {
				return true;
			}
		}
		
		return false;
	}

	public function offsetGet($offset) {
		/* 
		  May need is_object check because we can get:
			 <NameValueList xsi:nil="true"/>
		  Instead of normal:
			  <NameValueList>
			   <Name>Year</Name>
			   <Value>19000000</Value>
			  </NameValueList>
		
		  ext/soap will create an empty array element for the nilled out element.
		  I think that's actually correct, but it would be better for eBay not to return anything here.
		  However, I am not 100% sure. This is tricky.
		  Note: nilled out elements can have attributes.
		  Also, I'm unsure if an element has to be explicitly labled as nillable in the schema if you want to nil it out.
		*/

		foreach ($this as $NameValueList) {
			if ($NameValueList->Name == $offset) {
				if ($NameValueList->Name == 'Year') {
					// eBay returns this as YYYYMMDD, but MMDD is always 0000
					// Because cars come out in 2006, not 20060000
					// So, trim off stupid 0000 at end
					$value = substr($NameValueList->Value, 0, 4); 
				} else {
					$value = $NameValueList->Value;
				}

				return $value;
			}
		}
		
		return null;
	}

	public function offsetSet($offset, $value) {
		return true;
	}

	public function offsetUnset($offset) {
		return true;
	}

}