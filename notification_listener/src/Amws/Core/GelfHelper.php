<?php

namespace Amws\Core;

class GelfHelper {

    protected static $_instance = null;

    protected $_transport = null;
    protected $_publisher = null;

    /**
     * @return GraylogPublisher
     */
    public static function &singleton() {
        if (is_null(self::$_instance)) {
            self::$_instance = new self();
        }
        return self::$_instance;
    }

    public function destroy() {
        $this->_transport = null;
        $this->_publisher = null;
        self::$_instance = null;
    }

    public function __construct() {
        // graylog2 connection
        $this->_transport = new \Gelf\Transport\UdpTransport(APP_LOG_SERVER_HOST, APP_LOG_SERVER_PORT, \Gelf\Transport\UdpTransport::CHUNK_SIZE_LAN);
        $this->_publisher = new \Gelf\Publisher();
        $this->_publisher->addTransport($this->_transport);
    }

    public function getPublisher() {
        return $this->_publisher;
    }


}