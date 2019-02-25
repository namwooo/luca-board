import { Injectable } from '@angular/core';
import { Observable, of } from 'rxjs';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { catchError, map, tap } from 'rxjs/operators';

import { Comment } from '../models/comment';

@Injectable({
  providedIn: 'root'
})
export class CommentService {
  private baseUrl = 'api/comments';

  constructor(
    private http: HttpClient,
  ) { }

  getCommentsInPost(idPost: number): Observable<Comment[]> {
    const url = this.baseUrl + `/?idPost=${idPost}`;
    return this.http.get<Comment[]>(url)
    .pipe(
      catchError(this.handleError<Comment[]>(`getPostsInBoard`))
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