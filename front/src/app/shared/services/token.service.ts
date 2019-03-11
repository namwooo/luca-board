import { Injectable } from '@angular/core';
import * as jwt_decode from 'jwt-decode';
import * as moment from 'moment';

@Injectable({
    providedIn: 'root'
})
export class TokenService {

    constructor() { }

    getToken(): string {
        return localStorage.getItem('access_token');
    }

    setToken(authResult) {
        // current time + expires period
        const expiresAt = moment().add(authResult.expiresIn, 'second')
        // set token and expire date
        localStorage.setItem('access_token', authResult.access_token);
        localStorage.setItem('expires_at', JSON.stringify(expiresAt.valueOf()))
    }

    isTokenExpired(token) {
        const payload = jwt_decode(token)
        const expiresAt = localStorage.getItem('expries_at');

        return (payload.exp < expiresAt) ? false: true;
    }
}
