import { Injectable } from '@angular/core';
import { Observable, of } from 'rxjs';
import { catchError } from 'rxjs/operators';
import { HttpClient, HttpHeaders } from '@angular/common/http';


@Injectable({
  providedIn: 'root'
})
export class LoginService {
  private baseUrl = 'http://0.0.0.0:5000/';

  constructor(
    private http: HttpClient
    ) { }

  login(loginForm: any) {
    const url = this.baseUrl + 'users/login';
    return this.http.post(url, loginForm, httpOptions)
    .pipe(
      catchError(this.handleError<any>(`login`))
    )
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