import { Injectable } from '@angular/core';
import { Observable, of } from 'rxjs';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { catchError, map, tap } from 'rxjs/operators';

import { Post } from '../models/post';

@Injectable({
  providedIn: 'root'
})
export class PostService {
  private postsUrl = 'api/posts';

  constructor(
    private http: HttpClient
  ) { }

  getPostsInBoard(board_id: number): Observable<Post[]> {
    const url = `api/posts?board_id=${board_id}`;
    return this.http.get<Post[]>(url)
    .pipe(
      catchError(this.handleError<Post[]>(`getPostsInBoard`))
      )
  }

  private handleError<T> (operation = 'operation', result?: T) {
    return (error: any): Observable<T> => {

      // TODO: send the error to remote logging infrastructure
      console.error('error'); // log to console instead

      // Let the app keep running by returning an empty result.
      return of(result as T);
    };
  }
}

const httpOptions = {
  headers: new HttpHeaders({ 'Content-Type': 'application/json' })
};