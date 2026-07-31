import http from 'k6/http';
import { check, sleep } from 'k6';

// Performance Testing & Load Testing Configuration
export let options = {
    stages: [
        { duration: '30s', target: 50 },  // Ramp up to 50 users
        { duration: '1m', target: 50 },   // Sustain 50 users
        { duration: '30s', target: 200 }, // Spike to 200 users
        { duration: '1m', target: 200 },  // Sustain peak load
        { duration: '30s', target: 0 },   // Scale down
    ],
    thresholds: {
        http_req_duration: ['p(95)<500'],  // 95% of requests must complete below 500ms
        http_req_failed: ['rate<0.01'],    // Error rate must be less than 1%
    },
};

export default function () {
    // Replace with your actual application endpoint
    const BASE_URL = 'http://localhost:8000';
    
    // Simulate user behavior: API request
    let res = http.get(`${BASE_URL}/api/users/profile`, {
        headers: { 'Content-Type': 'application/json' },
    });
    
    // Validate response and ensure system constraints
    check(res, {
        'status is 200': (r) => r.status === 200,
        'transaction time OK': (r) => r.timings.duration < 200,
    });
    
    // Simulate human interaction delay
    sleep(1);
}
