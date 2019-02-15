import { Injectable } from '@angular/core';
import { Observable, of } from 'rxjs';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { catchError, map, tap } from 'rxjs/operators';

import { Board } from '../models/board';


@Injectable({
  providedIn: 'root'
})
export class BoardService {
  private boardsUrl = 'api/boards';

  constructor(
    private http: HttpClient
  ) { }

  getBoards(): Observable<Board[]> {
    return this.http.get<Board[]>(this.boardsUrl)
    .pipe(catchError(this.handleError('getBoards', [])))
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
  headers: new HttpHeaders({ 'Content-Type': 'application/json' })
};