import { Injectable } from '@angular/core';
import * as jwt_decode from 'jwt-decode';

@Injectable({
    providedIn: 'root'
})
export class TokenService {

    constructor() { }

    getToken(): string {
        return localStorage.getItem('access_token');
    }

    setToken(token) {
        const payload = jwt_decode(token)
        const expiresAt = payload.exp

        // set token and expire date
        localStorage.setItem('access_token', token);
        localStorage.setItem('expires_at', JSON.stringify(expiresAt.valueOf()))
    }

    isTokenExpired(token) {
        const payload = jwt_decode(token)
        const expiresAt = localStorage.getItem('expries_at');

        return (payload.exp < expiresAt) ? false: true;
    }
}
