"""
Circuit Breaker Pattern for Gmail API
Prevents cascading failures when Gmail API is down
"""

import logging
import time
from enum import Enum
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class CircuitState(Enum):
    CLOSED = "closed"  # Normal operation
    OPEN = "open"      # Too many failures, reject requests
    HALF_OPEN = "half_open"  # Testing if service recovered

class CircuitBreaker:
    """
    Circuit breaker to prevent cascading failures
    
    States:
    - CLOSED: Normal operation, requests go through
    - OPEN: Too many failures, reject requests immediately
    - HALF_OPEN: After timeout, allow one test request
    
    Configuration:
    - failure_threshold: Number of failures before opening circuit
    - timeout: Seconds to wait before trying again (half-open)
    - success_threshold: Successes needed in half-open to close circuit
    """
    
    def __init__(self, 
                 name: str,
                 failure_threshold: int = 5,
                 timeout: int = 60,
                 success_threshold: int = 2):
        self.name = name
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.success_threshold = success_threshold
        
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.success_count = 0
        self.last_failure_time = None
        self.opened_at = None
        
    def call(self, func, *args, **kwargs):
        """
        Execute function through circuit breaker
        """
        # Check if circuit is open
        if self.state == CircuitState.OPEN:
            # Check if timeout has passed
            if self.opened_at and (datetime.now() - self.opened_at).seconds >= self.timeout:
                logger.info(f"Circuit breaker '{self.name}': Timeout passed, entering HALF_OPEN state")
                self.state = CircuitState.HALF_OPEN
                self.success_count = 0
            else:
                logger.warning(f"Circuit breaker '{self.name}': OPEN - rejecting request")
                raise CircuitBreakerOpenError(f"Circuit breaker '{self.name}' is OPEN")
        
        # Try to execute the function
        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise
    
    def _on_success(self):
        """Handle successful request"""
        if self.state == CircuitState.HALF_OPEN:
            self.success_count += 1
            logger.info(f"Circuit breaker '{self.name}': Success in HALF_OPEN ({self.success_count}/{self.success_threshold})")
            
            if self.success_count >= self.success_threshold:
                logger.info(f"Circuit breaker '{self.name}': Closing circuit")
                self._close()
        elif self.state == CircuitState.CLOSED:
            # Reset failure count on success
            self.failure_count = 0
    
    def _on_failure(self):
        """Handle failed request"""
        self.failure_count += 1
        self.last_failure_time = datetime.now()
        
        logger.warning(f"Circuit breaker '{self.name}': Failure {self.failure_count}/{self.failure_threshold}")
        
        if self.state == CircuitState.HALF_OPEN:
            # Failed in half-open, go back to open
            logger.warning(f"Circuit breaker '{self.name}': Failed in HALF_OPEN, reopening circuit")
            self._open()
        elif self.failure_count >= self.failure_threshold:
            logger.error(f"Circuit breaker '{self.name}': Threshold reached, opening circuit")
            self._open()
    
    def _open(self):
        """Open the circuit"""
        self.state = CircuitState.OPEN
        self.opened_at = datetime.now()
        self.failure_count = 0
    
    def _close(self):
        """Close the circuit"""
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.success_count = 0
        self.opened_at = None
    
    def reset(self):
        """Manually reset the circuit breaker"""
        logger.info(f"Circuit breaker '{self.name}': Manual reset")
        self._close()
    
    def get_state(self):
        """Get current state"""
        return {
            "name": self.name,
            "state": self.state.value,
            "failure_count": self.failure_count,
            "success_count": self.success_count,
            "opened_at": self.opened_at.isoformat() if self.opened_at else None
        }

class CircuitBreakerOpenError(Exception):
    """Raised when circuit breaker is open"""
    pass

# Global circuit breakers for different services
_circuit_breakers = {}

def get_circuit_breaker(name: str, **kwargs) -> CircuitBreaker:
    """Get or create a circuit breaker"""
    if name not in _circuit_breakers:
        _circuit_breakers[name] = CircuitBreaker(name, **kwargs)
    return _circuit_breakers[name]

def reset_all_circuit_breakers():
    """Reset all circuit breakers (for testing)"""
    for cb in _circuit_breakers.values():
        cb.reset()
