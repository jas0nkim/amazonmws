<?php

namespace Amws\Core;

class AmwsLogProcessor {
    /**
     * @var array
     */
    protected $extraFields = array(
        'environment' => 'production',
        'task' => 'general',
    );

    /**
     * @param array|\ArrayAccess $serverData  Array or object w/ ArrayAccess that provides access to the $_SERVER data
     * @param array|null         $extraFields Extra field names to be added (all available by default)
     */
    public function __construct($environment = 'production', $task = 'general') {
        $this->extraFields['environment'] = $environment;
        $this->extraFields['task'] = $task;
    }

    /**
     * @param  array $record
     * @return array
     */
    public function __invoke(array $record)
    {
        $record['extra'] = $this->extraFields;
        return $record;
    }
}
