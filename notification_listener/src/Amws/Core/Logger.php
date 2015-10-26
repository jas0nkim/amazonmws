<?php

namespace Amws\Core;

class Logger {

    protected $_logger;

    public function __construct() {
        $_env = APP_ENV == 'stage' ? 'staging' : 'production';
        $_logger = new \Monolog\Logger($_env);

        try {
            $_logger->pushHandler(
                new \Monolog\Handler\GelfHandler(GelfHelper::singleton()->getPublisher(), APP_LOG_LEVEL));
        } catch (\RuntimeException $e) {
            // couldn't connect to graylog, so switch to normal log
            $_logger->pushHandler(
                new \Monolog\Handler\StreamHandler(ini_get('error_log'), APP_LOG_LEVEL));
        }

        $_logger->pushProcessor(new \Monolog\Processor\WebProcessor());
        $_logger->pushProcessor(new AmwsLogProcessor($_env, 'php_soap'));

        $this->_logger = $_logger;
    }

    public function debug($message) {
        return $this->_logger->addDebug($message);
    }

    public function info($message) {
        return $this->_logger->addInfo($message);
    }

    public function notice($message) {
        return $this->_logger->addNotice($message);        
    }

    public function warning($message) {
        return $this->_logger->addWarning($message);        
    }

    public function error($message) {
        return $this->_logger->addError($message);
    }

    public function critical($message) {
        return $this->_logger->addCritical($message);
    }
    
    public function exception(\Exception $e) {
        $message = sprintf("%s\n%s\n", $e->getMessage(), $e->getTraceAsString());
        return $this->_logger->addError($message);
    }
}