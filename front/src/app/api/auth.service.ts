import { Injectable } from '@angular/core';
import { Observable, of } from 'rxjs';
import { catchError, tap } from 'rxjs/operators';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import * as moment from 'moment';
import * as jwt_decode from 'jwt-decode';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private baseUrl = 'http://localhost:5000/';

  constructor(
    private http: HttpClient
    ) { }

  login(email: string, password: string) {
    const url = this.baseUrl + 'users/login';
    return this.http.post(url, {email, password}, httpOptions) // POST localhost:5000/users/login
    .pipe(
      tap(res => this.setAccessToken(res)), 
      catchError(this.handleError<any>(`login`))
    )
  }

  signup(form: object) {
    const url = this.baseUrl + 'users/signup';
    return this.http.post(url, form, httpOptions)
    .pipe(
      catchError(this.handleError(`signup`))
    )
  }

  private setAccessToken(authResult) {

    const token = localStorage.getItem('access_token');
    console.log(jwt_decode(token));
    
    // current time + expires period
    const expiresAt = moment().add(authResult.expiresIn, 'second')
    // set token and expire date
    localStorage.setItem('access_token', authResult.access_token);
    localStorage.setItem('expires_at', JSON.stringify(expiresAt.valueOf()))
  }

  private handleError<T> (operation = 'operation', result?: T) {
    return (error: any): Observable<T> => {

      // TODO: send the error to remote logging infrastructure
      console.error(error); // log to console instead

      // Let the app keep running by returning an empty result.
      return of(result as T);
    };
  }
}

const httpOptions = {
  headers: new HttpHeaders({ 'Content-Type': 'application/json' }),
  withCredentials: true,
};