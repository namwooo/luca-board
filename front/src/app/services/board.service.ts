import { Injectable } from '@angular/core';
import { Observable, of, Subject } from 'rxjs';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { catchError, map, tap } from 'rxjs/operators';

import { Board } from '../models/board';


@Injectable({
  providedIn: 'root'
})
export class BoardService {
  private boardsUrl = 'http://0.0.0.0:5000/boards';
  private boardSource = new Subject<Board>();

  board$ = this.boardSource.asObservable();

  constructor(
    private http: HttpClient
  ) { }

  getBoards(): Observable<Board[]> {
    return this.http.get<Board[]>(this.boardsUrl)
    .pipe(catchError(this.handleError('getBoards', [])))
  }

  getBoard(id: number): Observable<Board> {
    return this.http.get<Board>(this.boardsUrl + `/${id}`)
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